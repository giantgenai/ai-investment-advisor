from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from requests.exceptions import Timeout
from llama_index.core.tools import FunctionTool
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
import yfinance as yf
import json
import asyncio

from openai import OpenAI 

# Initialize the OpenAI client to use Ollama's local server
ollama_client = OpenAI(
    base_url='http://localhost:11434/v1',  
    api_key='ollama'  
)

# Initialize OpenAI client (for fallback)
openai_client = OpenAI()

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
                provider="ollama/llama3.3:latest",  # Use LLaMA 3 model
                api_token='ollama', 
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
            print(f"Failed to parse JSON from crawl result: {e}")
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
        print(f"Error crawling page summary for {url}: {e}")
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
        response = ollama_client.chat.completions.create(
            model="llama3.2",
            messages=messages,
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ollama failed for summary generation: {e}")
    
    # Fallback to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI also failed for summary generation: {e}")
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
        response = ollama_client.chat.completions.create(
            model="llama3.2",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ollama failed for ticker generation: {e}")
    
    # Fallback to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI also failed for ticker generation: {e}")
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
            print(f"No news found for {ticker}")
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
                print(f"Error processing news item for {ticker}: {item_error}")
                continue
        
        return formatted_news
    except Exception as e:
        print(f"An error occurred for {ticker}: {e}")
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
        print(f"Fetching news for {ticker}...")
        company_news = get_company_news(ticker)
        if company_news:
            all_news.append(f"News for {ticker}:")
            for item in company_news:
                all_news.append(f"- {item['title']} (Published: {item['published']})")
                
                summary_text = None
                
                # Try to crawl the page for summary if link is available
                if item.get('link'):
                    try:
                        print(f"Crawling summary for {item['title']}...")
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
                        print(f"Crawling failed for {item['title']}: {e}")
                
                # Fallback: Generate summary from title using LLM if crawling failed
                if not summary_text:
                    print(f"Using fallback summary generation for {item['title']}...")
                    try:
                        summary_text = generate_summary_from_title(item['title'], ticker)
                    except Exception as e:
                        print(f"Fallback summary generation failed: {e}")
                
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
    print(f"Generating investment recommendation for {industry}...")
    tickers = get_industry_tickers(industry)
    if not tickers:
        return f"Unable to fetch tickers for {industry} industry."
    
    print(f"Fetching news summaries for {tickers}...")
    summaries = get_news_with_summary(tickers)
    
    print("Analyzing news and generating recommendation...")
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
        response = ollama_client.chat.completions.create(
            model="llama3.2",
            messages=messages,
            temperature=0,
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Timeout:
        return "Timeout occurred while generating recommendation."
    except Exception as e:
        print(f"Ollama failed for recommendation: {e}")
    
    # Fallback to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
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

