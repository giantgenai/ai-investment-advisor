import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
from urllib.parse import urljoin
import feedparser

# Create data directory if it doesn't exist
if not os.path.exists('../data'):
    os.makedirs('../data')

# Function to sanitize filename
def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()

# Function to save article
def save_article(title, content, source):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{sanitize_filename(title)[:50]}.txt"
    with open(os.path.join('../data', filename), 'w', encoding='utf-8') as f:
        f.write(f"Title: {title}\n")
        f.write(f"Source: {source}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(content)

# Function to scrape CNBC
def scrape_cnbc():
    url = "https://www.cnbc.com/business/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for article in soup.find_all('div', class_='Card-titleContainer'):
        title = article.find('a').text.strip()
        link = article.find('a')['href']
        
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        content = article_soup.find('div', class_='ArticleBody-articleBody').text.strip()
        
        save_article(title, content, "CNBC")
        time.sleep(2)  # Be nice to the server

# Function to scrape Yahoo Finance
def scrape_yahoo_finance():
    rss_url = "https://finance.yahoo.com/news/rssindex"
    
    try:
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                article_response = requests.get(link, headers=headers)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                
                content_div = article_soup.find('div', class_='caas-body')
                if not content_div:
                    print(f"Could not find content for Yahoo Finance article: {title}")
                    continue
                
                paragraphs = content_div.find_all('p')
                content = '\n'.join([p.text for p in paragraphs])
                
                save_article(title, content, "Yahoo Finance")
                print(f"Saved Yahoo Finance article: {title}")
                
            except requests.RequestException as e:
                print(f"Error fetching Yahoo Finance article {title}: {e}")
            
            time.sleep(2)  # Be nice to the server
        
    except Exception as e:
        print(f"Error fetching Yahoo Finance RSS feed: {e}")

# Main scraping function
def scrape_financial_news():
    print("Starting to scrape financial news...")
    scrape_cnbc()
    scrape_yahoo_finance()
    print("Finished scraping financial news.")

if __name__ == "__main__":
    scrape_financial_news()