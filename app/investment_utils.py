from typing import List, Dict
import logging
import os
from datetime import datetime
from pydantic import BaseModel, Field
from requests.exceptions import Timeout
from llama_index.core.tools import FunctionTool
from crawl4ai import AsyncWebCrawler, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import yfinance as yf
import json
import asyncio

from openai import OpenAI 

from config import MODEL_CONFIG

logger = logging.getLogger(__name__)

_ollama_client = None
_openai_client = None

def get_ollama_client() -> OpenAI:
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OpenAI(
            base_url=MODEL_CONFIG.ollama_base_url,
            api_key=MODEL_CONFIG.ollama_api_key
        )
    return _ollama_client

def get_openai_client() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client

class PageSummary(BaseModel):
    title: str = Field(..., description="The title of the page")
    summary: str = Field(..., description="The summary of the page")
    brief_summary: str = Field(..., description="The brief summary of the page")
    content: str = Field(..., description="The content of the page")
    keywords: list = Field(..., description="The keywords of the page")

async def crawl_page_summary_async(url):
    """Async version of crawl_page_summary using the new crawl4ai API."""
    if not url:
        return None
        
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                llm_config=LLMConfig(
                    provider=MODEL_CONFIG.ollama_summary_provider,
                    api_token=MODEL_CONFIG.ollama_api_key
                ),
                schema=PageSummary.model_json_schema(),
                extraction_type="schema",
                instruction="From the crawled content, extract the following information: "\
                "1. title: The title of the page "\
                "2. summary: A summary of the page, which is a concise overview of the page content "\
                "3. brief_summary: A brief summary of the page, which is paragraph-long summary of the page content less than 250 words"\
                "4. content: The content of the page "\
                "5. keywords: A list of keywords of the page. "\
                'The extracted JSON format should look exactly like this with only 5 keys:  '\
                '{\n'\
                '    "title": "Page Title",\n'\
                '    "summary": "Page Summary",\n'\
                '    "brief_summary": "Page Brief Summary",\n'\
                '    "content": "Page Content",\n'\
                '    "keywords": ["keyword1", "keyword2", "keyword3"]\n'\
                '}'
            ),
            bypass_cache=True,
        )
        
        # Check if extracted_content exists and is valid
        if not result or not result.extracted_content:
            return None
            
        try:
            page_summary = json.loads(result.extracted_content)
            return page_summary
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON from crawl result: %s", e)
            return None

def crawl_page_summary(url):
    """Synchronous wrapper for crawl_page_summary_async."""
    if not url:
        return None
        
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            # If there's already an event loop running (e.g., in Streamlit),
            # create a new loop in a separate thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, crawl_page_summary_async(url))
                return future.result()
        else:
            return loop.run_until_complete(crawl_page_summary_async(url))
    except Exception as e:
        logger.warning("Error crawling page summary for %s: %s", url, e)
        return None


def generate_summary_from_title(title: str, ticker: str) -> str:
    """
    Generate a brief summary using LLM based on the news title.
    This is a fallback when web crawling is not available.
    
    Args:
        title (str): The news article title.
        ticker (str): The stock ticker symbol.
    
    Returns:
        str: A brief generated summary based on the title.
    """
    if not title:
        return None
        
    prompt = f"""Based on this news headline about {ticker}, provide a brief 1-2 sentence summary of what this news likely means for investors:

Headline: {title}

Provide only the summary, no additional text or explanation."""

    messages = [
        {"role": "system", "content": "You are a financial news analyst. Provide brief, factual summaries."},
        {"role": "user", "content": prompt}
    ]

    # Try Ollama first
    try:
        response = get_ollama_client().chat.completions.create(
            model=MODEL_CONFIG.ollama_summary_model,
            messages=messages,
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("Ollama failed for summary generation: %s", e)
    
    # Fallback to OpenAI
    try:
        response = get_openai_client().chat.completions.create(
            model=MODEL_CONFIG.openai_chat_model,
            messages=messages,
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("OpenAI also failed for summary generation: %s", e)
        return None

def get_industry_tickers(industry: str) -> str:
    """
    Get the top 3 tickers for a given industry using OpenAI.
    
    Args:
        industry (str): The name of the industry.
    
    Returns:
        str: A comma-separated list of tickers.
    """
    
    prompt = f"""
    Please provide a comma-separated list of the top 3 stock tickers for companies in the {industry} industry.
    Only include the tickers, no additional text or explanation.
    Example format: AAPL, MSFT, GOOGL
    """
    
    messages = [
        {"role": "system", "content": "You are a financial assistant."},
        {"role": "user", "content": prompt}
    ]
    
    # Try Ollama first
    try:
        response = get_ollama_client().chat.completions.create(
            model=MODEL_CONFIG.ollama_chat_model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("Ollama failed for ticker generation: %s", e)
    
    # Fallback to OpenAI
    try:
        response = get_openai_client().chat.completions.create(
            model=MODEL_CONFIG.openai_chat_model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("OpenAI also failed for ticker generation: %s", e)
        return ""

# Create the LlamaIndex tool
industry_tickers_tool = FunctionTool.from_defaults(
    fn=get_industry_tickers,
    name="IndustryTickers",
    description="Get the top 3 stock tickers for a given industry."
)

def get_company_news(ticker: str, num_news: int=3) -> List[Dict[str, str]]:
    try:
        company = yf.Ticker(ticker)
        news = company.news
        
        if not news:
            logger.info("No news found for %s", ticker)
            return []
        
        formatted_news = []
        for item in news[:num_news]:  # Limit to 3 news items per company
            try:
                # Try new yfinance API structure first (v0.2.28+)
                if 'content' in item:
                    content = item['content']
                    title = content.get('title', 'No title')
                    
                    # Handle different link structures
                    if 'canonicalUrl' in content and isinstance(content['canonicalUrl'], dict):
                        link = content['canonicalUrl'].get('url', '')
                    else:
                        link = content.get('clickThroughUrl', {}).get('url', '') if isinstance(content.get('clickThroughUrl'), dict) else ''
                    
                    # Handle pubDate as ISO string
                    pub_date_str = content.get('pubDate', '')
                    if pub_date_str:
                        try:
                            # Parse ISO format date
                            publish_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                        except (ValueError, AttributeError):
                            publish_date = pub_date_str
                    else:
                        publish_date = 'Unknown'
                else:
                    # Fall back to old yfinance API structure
                    title = item.get('title', 'No title')
                    link = item.get('link', '')
                    
                    # Handle providerPublishTime as timestamp
                    if 'providerPublishTime' in item:
                        publish_date = datetime.fromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        publish_date = 'Unknown'
                
                formatted_item = {
                    'title': title,
                    'link': link,
                    'published': publish_date
                }
                formatted_news.append(formatted_item)
            except Exception as item_error:
                logger.warning("Error processing news item for %s: %s", ticker, item_error)
                continue
        
        return formatted_news
    except Exception as e:
        logger.warning("An error occurred for %s: %s", ticker, e)
        return []

def get_news_with_summary(tickers: str) -> str:
    """
    Get recent news with content for a list of company tickers.
    
    Args:
        tickers (str): A comma-separated list of stock tickers.
    
    Returns:
        str: A formatted string containing recent news and summaries for each company.
    """
    ticker_list = [ticker.strip() for ticker in tickers.split(',')]
    all_news = []

    for ticker in ticker_list:
        logger.info("Fetching news for %s...", ticker)
        company_news = get_company_news(ticker)
        if company_news:
            all_news.append(f"News for {ticker}:")
            for item in company_news:
                all_news.append(f"- {item['title']} (Published: {item['published']})")
                
                summary_text = None
                
                # Try to crawl the page for summary if link is available
                if item.get('link'):
                    try:
                        logger.info("Crawling summary for %s...", item['title'])
                        summary = crawl_page_summary(item['link'])
                        if summary:
                            # Handle different response structures
                            if isinstance(summary, list) and len(summary) > 0:
                                # Response is a list of dictionaries
                                summary_item = summary[0]
                                if isinstance(summary_item, dict) and 'summary' in summary_item:
                                    summary_text = summary_item['summary']
                                elif isinstance(summary_item, dict) and 'brief_summary' in summary_item:
                                    summary_text = summary_item['brief_summary']
                                else:
                                    summary_text = str(summary_item)[:500]
                            elif isinstance(summary, dict):
                                # Response is a single dictionary
                                if 'summary' in summary:
                                    summary_text = summary['summary']
                                elif 'brief_summary' in summary:
                                    summary_text = summary['brief_summary']
                                else:
                                    summary_text = str(summary)[:500]
                            else:
                                summary_text = str(summary)[:500]
                    except Exception as e:
                        logger.warning("Crawling failed for %s: %s", item['title'], e)
                
                # Fallback: Generate summary from title using LLM if crawling failed
                if not summary_text:
                    logger.info("Using fallback summary generation for %s...", item['title'])
                    try:
                        summary_text = generate_summary_from_title(item['title'], ticker)
                    except Exception as e:
                        logger.warning("Fallback summary generation failed: %s", e)
                
                if summary_text:
                    all_news.append(f"  Summary: {summary_text}")
                else:
                    all_news.append("  Summary: Summary not available")
                
                # Add source link
                if item.get('link'):
                    all_news.append(f"  Source: {item['link']}")
                    
            all_news.append("")  # Add a blank line between companies

    if all_news:
        return "\n".join(all_news)
    else:
        return "No news found for the provided tickers."

# Create the LlamaIndex tool
ticker_news_summary_tool = FunctionTool.from_defaults(
    fn=get_news_with_summary,
    name="TickerNewsSummary",
    description="Get recent news with content for a list of company stock tickers."
)

def recommend_investment(industry: str) -> str:
    logger.info("Generating investment recommendation for %s...", industry)
    tickers = get_industry_tickers(industry)
    if not tickers:
        return f"Unable to fetch tickers for {industry} industry."
    
    logger.info("Fetching news summaries for %s...", tickers)
    summaries = get_news_with_summary(tickers)
    
    logger.info("Analyzing news and generating recommendation...")
    prompt = f"""
    Based on the following news summaries for companies in the {industry} industry, 
    analyze the information and recommend the best company for investment. 
    Consider factors such as positive developments, growth potential, and market trends.
    Provide a brief explanation for your recommendation.

    News Summaries:
    {summaries}

    Recommendation:
    """
    
    messages = [
        {"role": "system", "content": "You are a financial analyst."},
        {"role": "user", "content": prompt}
    ]
    
    # Try Ollama first
    try:
        response = get_ollama_client().chat.completions.create(
            model=MODEL_CONFIG.ollama_chat_model,
            messages=messages,
            temperature=0,
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Timeout:
        return "Timeout occurred while generating recommendation."
    except Exception as e:
        logger.warning("Ollama failed for recommendation: %s", e)
    
    # Fallback to OpenAI
    try:
        response = get_openai_client().chat.completions.create(
            model=MODEL_CONFIG.openai_chat_model,
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error occurred while generating recommendation: {str(e)}"

investment_recommendation_tool = FunctionTool.from_defaults(
    fn=recommend_investment,
    name="InvestmentRecommendation",
    description="Analyze news and recommend the best investment in a given industry."
)

