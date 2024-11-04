from typing import List, Dict
from datetime import datetime
from pydantic import BaseModel, Field
from requests.exceptions import Timeout
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer
from crawl4ai.chunking_strategy import *
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.crawler_strategy import *
from crawl4ai.web_crawler import WebCrawler
from crawl4ai import config
import yfinance as yf
import json

crawler = WebCrawler()
crawler.warmup()

from openai import OpenAI  # Ensure you have the OpenAI library installed

# Initialize the OpenAI client to use Ollama's local server
client = OpenAI(
    base_url='http://localhost:11434/v1',  # Ollama's local server
    api_key='ollama'  # Required but unused
)

class PageSummary(BaseModel):
    title: str = Field(..., description="The title of the page")
    summary: str = Field(..., description="The summary of the page")
    brief_summary: str = Field(..., description="The brief summary of the page")
    content: str = Field(..., description="The content of the page")
    keywords: list = Field(..., description="The keywords of the page")

def crawl_page_summary(url):
    result = crawler.run(
        url=url,
        word_count_threshold=1,
        extraction_strategy=LLMExtractionStrategy(
            # prompt= "openai/gpt-4o-mini",
            # api_token=os.environ["OPENAI_API_KEY"],
            provider="ollama/llama3.2",  # Use LLaMA 3 model
            api_token='ollama', 
            scheme=PageSummary.model_json_schema(),
            extraction_type="schema",
            apply_chunking=False,
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
    page_summary = json.loads(result.extracted_content)
    return page_summary

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
    
    # llm = OpenAI(model="gpt-4", temperature=0)
    # response = llm.complete(prompt)
    # return response.text.strip()
    response = client.chat.completions.create(
        model="llama3.2",  # Use LLaMA 3 model
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
        )
    return response.choices[0].message.content.strip()

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
        
        formatted_news = []
        for item in news[:num_news]:  # Limit to 3 news items per company
            publish_date = datetime.fromtimestamp(item['providerPublishTime']).strftime('%Y-%m-%d %H:%M:%S')
            formatted_item = {
                'title': item['title'],
                'link': item['link'],
                'published': publish_date
            }
            formatted_news.append(formatted_item)
        
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
                try:
                    print(f"Crawling summary for {item['title']}...")
                    summary = crawl_page_summary(item['link'])
                    if summary:
                        # all_news.append(f"  Summary: {summary[0]['summary']}; Content: {summary[0]['content']}")
                        all_news.append(f"  Summary: {summary[0]['summary']}")
                    else:
                        all_news.append("  Unable to fetch summary")
                except Exception as e:
                    all_news.append(f"  Unable to fetch summary: {str(e)}")
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
    # llm = OpenAI(model="gpt-4", temperature=0)
    prompt = f"""
    Based on the following news summaries for companies in the {industry} industry, 
    analyze the information and recommend the best company for investment. 
    Consider factors such as positive developments, growth potential, and market trends.
    Provide a brief explanation for your recommendation.

    News Summaries:
    {summaries}

    Recommendation:
    """
    
    # try:
    #     response = llm.complete(prompt, timeout=60)
    #     return response.text.strip()
    try:
        response = client.chat.completions.create(
            model="llama3.2",  # Use LLaMA 3 model
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Timeout:
        return "Timeout occurred while generating recommendation."
    except Exception as e:
        return f"Error occurred while generating recommendation: {str(e)}"

investment_recommendation_tool = FunctionTool.from_defaults(
    fn=recommend_investment,
    name="InvestmentRecommendation",
    description="Analyze news and recommend the best investment in a given industry."
)

