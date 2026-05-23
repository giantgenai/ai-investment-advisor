import streamlit as st
import time
import logging
import re
import html
from typing import Optional
from datetime import datetime
from streamlit_chat import message

from mock_responses import (
    get_mock_recommendation,
    get_mock_chat_response,
    get_mock_industry_tickers,
    get_mock_news_summaries,
    get_mock_stock_info,
    get_mock_stock_history,
    get_mock_stock_history_range,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

st.set_page_config(page_title="Investment Advisor Pro", page_icon="📈", layout="wide")

st.markdown(
    """
    <style>
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .highlight {
        background-color: #f3f4f6;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    .recommendation-line {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
        margin-bottom: 16px;
    }
    .recommendation-line .value {
        font-weight: 700;
    }
    .explanation-summary {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 18px 22px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 15px;
        line-height: 1.7;
        color: #1f2937;
        margin: 16px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        position: relative;
    }
    .explanation-summary::before {
        content: '💡 Key Insight';
        position: absolute;
        top: -10px;
        left: 16px;
        background: #2563eb;
        color: white;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 4px;
        letter-spacing: 0.03em;
    }
    .explanation-summary a {
        color: #2563eb;
    }
    .explanation-section-title {
        font-size: 13px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 18px 0 8px 0;
    }
    .explanation-list {
        list-style: none;
        padding-left: 0;
        margin: 0 0 4px 0;
    }
    .explanation-list li {
        margin-bottom: 8px;
        line-height: 1.55;
        padding-left: 18px;
        position: relative;
        color: #111827;
    }
    .explanation-list li * {
        color: #111827;
    }
    .explanation-list li a {
        color: #111827;
        text-decoration: none;
    }
    .explanation-list li::before {
        content: '\\2022';
        position: absolute;
        left: 2px;
        color: #2563eb;
    }
    .metrics-divider {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 0;
        padding: 0;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        align-items: baseline;
        font-size: 13px;
        margin-bottom: 0;
        padding: 2px 0;
    }
    /* Reduce Streamlit's default spacing for metric columns */
    [data-testid="column"] > div:has(.metric-row) {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div:has(> .metrics-divider) {
        margin-top: -28px !important;
        margin-bottom: -24px !important;
    }
    .metric-row .label {
        color: #374151;
        font-weight: 500;
    }
    .metric-row .value {
        color: #111827;
        font-weight: 700;
        font-size: 14px;
        text-align: right;
        white-space: nowrap;
    }
    .news-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 24px 0 0 0;
        padding-bottom: 4px;
        border-bottom: 1px solid #e5e7eb;
    }
    .news-header .card-title {
        margin: 0;
    }
    .news-card {
        border-bottom: 1px solid #e5e7eb;
        padding: 16px 0 0 0;
        display: block;
    }
    .news-title {
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 4px;
    }
    .news-title-link {
        font-weight: 600;
        font-size: 15px;
        color: #111827 !important;
        text-decoration: none !important;
    }
    .news-title-link:hover {
        color: #2563eb !important;
        text-decoration: none !important;
    }
    .news-title-link:visited {
        color: #111827 !important;
        text-decoration: none !important;
    }
    a.news-title-link {
        color: #111827 !important;
        text-decoration: none !important;
    }
    a.news-title-link:hover {
        color: #2563eb !important;
    }
    .news-meta {
        color: #6b7280;
        font-size: 12px;
    }
    .news-summary {
        background-color: #f8fafc;
        border-left: 4px solid #2563eb;
        border-radius: 0 6px 6px 0;
        padding: 10px 14px;
        color: #374151;
        font-size: 13px;
        line-height: 1.5;
        margin: 8px 0 16px 0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    .ref-link {
        color: #2563eb;
        text-decoration: none;
        font-weight: 600;
        padding: 0 2px;
    }
    .ref-link:hover {
        text-decoration: underline;
        color: #1d4ed8;
    }
    div[data-testid="stMarkdownContainer"] .news-header,
    div[data-testid="stMarkdownContainer"] .news-card {
        margin-bottom: 0;
    }
    .footer {
        color: #6b7280;
        font-size: 12px;
        margin-top: 16px;
        border-top: 1px solid #e5e7eb;
        padding-top: 12px;
    }
    .app-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #3b82f6 100%);
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .app-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .app-subtitle {
        font-size: 15px;
        color: rgba(255,255,255,0.85);
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    /* Sidebar Navigation Styles */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 10px 12px;
        margin: 2px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.15s ease;
        font-size: 14px;
        font-weight: 500;
        color: #374151;
        text-decoration: none;
    }
    .nav-item:hover {
        background-color: #f3f4f6;
    }
    .nav-item.active {
        background-color: #eff6ff;
        color: #2563eb;
    }
    .nav-item .nav-icon {
        margin-right: 10px;
        font-size: 16px;
        width: 20px;
        text-align: center;
    }
    .nav-section {
        font-size: 11px;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 16px 12px 6px 12px;
        margin-top: 8px;
    }
    .nav-section:first-child {
        margin-top: 0;
        padding-top: 8px;
    }
    .sidebar-logo {
        padding: 16px 12px;
        margin-bottom: 8px;
    }
    .model-selector {
        padding: 8px 12px;
        margin-top: 12px;
    }
    .model-selector label {
        font-size: 11px;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* Sidebar button styling */
    [data-testid="stSidebar"] button {
        background: transparent !important;
        border: none !important;
        color: #374151 !important;
        font-weight: 500 !important;
        justify-content: flex-start !important;
        padding: 6px 12px !important;
        font-size: 14px !important;
        margin: 0 !important;
        min-height: 36px !important;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #f3f4f6 !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #eff6ff !important;
        color: #2563eb !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        gap: 2px !important;
    }
    [data-testid="stSidebar"] .stButton {
        margin-bottom: 0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox {
        margin-top: 8px;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        font-size: 13px;
    }
    /* Industry Tiles Grid */
    .industry-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-top: 16px;
    }
    .industry-tile {
        aspect-ratio: 1.3;
        border-radius: 12px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        position: relative;
        overflow: hidden;
    }
    .industry-tile:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    .industry-tile .tile-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }
    .industry-tile .tile-name {
        font-size: 15px;
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        margin: 24px 0 8px 0;
    }
    .section-subtitle {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 16px;
    }
    /* Industry tile buttons */
    .industry-btn {
        border-radius: 12px !important;
        padding: 20px 16px !important;
        height: auto !important;
        min-height: 90px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        justify-content: flex-end !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: white !important;
        border: none !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .industry-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15) !important;
    }
    /* Tracker Button Styles - Inline sleek design */
    .tracker-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        background-color: #dcfce7;
        color: #166534;
        white-space: nowrap;
        margin-left: 8px;
    }
    .tracker-badge .tick {
        font-size: 11px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=3600, show_spinner=False)
def get_industry_data(industry):
    """Get mock industry data for testing."""
    tickers = get_mock_industry_tickers(industry)
    news_summaries = get_mock_news_summaries(tickers)
    return tickers, news_summaries

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_history(ticker: str, period: str = "1y", interval: str = "1d"):
    """Get mock stock history for testing."""
    if not ticker:
        return None
    try:
        return get_mock_stock_history(ticker, period=period, interval=interval)
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_history_range(ticker: str, start_date: str, end_date: Optional[str] = None):
    """Get mock stock history range for testing."""
    if not ticker or not start_date:
        return None
    try:
        return get_mock_stock_history_range(ticker, start_date=start_date, end_date=end_date)
    except Exception:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_info(ticker: str):
    """Get mock stock info for testing."""
    if not ticker:
        return {}
    try:
        return get_mock_stock_info(ticker)
    except Exception:
        return {}

def calculate_percentage_change(ticker: str, period: str, interval: str = "1d") -> Optional[float]:
    history = get_stock_history(ticker, period=period, interval=interval)
    if history is None or history.empty:
        return None
    try:
        start_price = history["Close"].iloc[0]
        end_price = history["Close"].iloc[-1]
        if start_price is None or end_price is None:
            return None
        if start_price != start_price or end_price != end_price:
            return None
        if start_price == 0:
            return None
        return ((end_price - start_price) / start_price) * 100
    except Exception:
        return None


def _calculate_return_from_history(history) -> Optional[float]:
    if history is None or history.empty:
        return None
    try:
        closes = history["Close"].dropna()
        if closes.empty:
            return None
        start_price = closes.iloc[0]
        end_price = closes.iloc[-1]
        if start_price == 0:
            return None
        return ((end_price - start_price) / start_price) * 100
    except Exception:
        return None


def _parse_tracker_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%b %d, %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None


def calculate_alpha_vs_sp500(ticker: str, start_date: Optional[datetime]) -> Optional[float]:
    if not start_date:
        return None
    start_str = start_date.strftime("%Y-%m-%d")
    stock_return = _calculate_return_from_history(
        get_stock_history_range(ticker, start_date=start_str)
    )
    sp_return = _calculate_return_from_history(
        get_stock_history_range("^GSPC", start_date=start_str)
    )
    if stock_return is None or sp_return is None:
        return None
    return stock_return - sp_return


def format_range(low, high):
    if low is None or high is None:
        return "—"
    try:
        return f"{low:.2f} - {high:.2f}"
    except Exception:
        return "—"

def format_percentage_change(value: Optional[float]) -> str:
    if value is None:
        return "—"
    css_class = "t-up" if value >= 0 else "t-down"
    arrow = "▲" if value >= 0 else "▼"
    return f"<span class='{css_class}'>{arrow} {abs(value):.2f}%</span>"

def format_number(value, suffix=""):
    if value is None:
        return "—"
    try:
        if isinstance(value, (int, float)):
            if abs(value) >= 1_000_000_000_000:
                return f"{value/1_000_000_000_000:.2f}T{suffix}"
            if abs(value) >= 1_000_000_000:
                return f"{value/1_000_000_000:.2f}B{suffix}"
            if abs(value) >= 1_000_000:
                return f"{value/1_000_000:.2f}M{suffix}"
            if abs(value) >= 1_000:
                return f"{value:,.0f}{suffix}"
            return f"{value:.2f}{suffix}"
        return str(value)
    except Exception:
        return "—"

def format_date(value):
    if value is None:
        return "—"
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value).strftime("%b %d, %Y")
        return str(value)
    except Exception:
        return "—"

def get_period_options():
    return {
        "1D": ("1d", "5m"),
        "5D": ("5d", "30m"),
        "1M": ("1mo", "1h"),
        "6M": ("6mo", "1d"),
        "YTD": ("ytd", "1d"),
        "1Y": ("1y", "1d"),
        "5Y": ("5y", "1wk"),
        "Max": ("max", "1mo"),
    }

def extract_recommended_ticker(recommendation_text: str) -> str:
    match = re.search(r"Recommendation:\s*([A-Z.\-]{1,10})", recommendation_text)
    return match.group(1) if match else ""

def _first_sentence(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0].strip() if sentences else text.strip()

# Domain to clean source name mapping
DOMAIN_TO_SOURCE = {
    'fool.com': 'Motley Fool',
    'reuters.com': 'Reuters',
    'bloomberg.com': 'Bloomberg',
    'wsj.com': 'WSJ',
    'cnbc.com': 'CNBC',
    'yahoo.com': 'Yahoo Finance',
    'finance.yahoo.com': 'Yahoo Finance',
    'marketwatch.com': 'MarketWatch',
    'seekingalpha.com': 'Seeking Alpha',
    'investopedia.com': 'Investopedia',
    'barrons.com': "Barron's",
    'ft.com': 'Financial Times',
    'nytimes.com': 'NY Times',
    'washingtonpost.com': 'Washington Post',
    'forbes.com': 'Forbes',
    'businessinsider.com': 'Business Insider',
    'thestreet.com': 'TheStreet',
    'investors.com': "Investor's Business Daily",
    'morningstar.com': 'Morningstar',
    'zacks.com': 'Zacks',
    'benzinga.com': 'Benzinga',
    '247wallst.com': '24/7 Wall St',
    'wardsauto.com': "Ward's Auto",
    'autoblog.com': 'Autoblog',
    'caranddriver.com': 'Car and Driver',
    'motortrend.com': 'MotorTrend',
    'electrek.co': 'Electrek',
    'techcrunch.com': 'TechCrunch',
    'theverge.com': 'The Verge',
    'arstechnica.com': 'Ars Technica',
}

def _extract_source_name(url: str) -> str:
    """Extract a clean source name from a URL."""
    if not url:
        return 'Source'
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # Remove www. prefix
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Check mapping first
        if domain in DOMAIN_TO_SOURCE:
            return DOMAIN_TO_SOURCE[domain]
        
        # Check if any key is contained in domain
        for key, name in DOMAIN_TO_SOURCE.items():
            if key in domain:
                return name
        
        # Fallback: clean up the domain name
        # Remove common TLDs and format nicely
        name = domain.split('.')[0]
        return name.title()
    except:
        return 'Source'

def _convert_references_to_links(text: str, references: dict[str, dict[str, str]], numbered_refs: dict[int, dict[str, str]] = None) -> str:
    """Convert [Source Name] or [1], [2] in text to clickable links."""
    
    # Remove placeholder references like [Relevant News] entirely
    text = re.sub(r'\s*\[Relevant News\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*\[Source\]', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*\[News\]', '', text, flags=re.IGNORECASE)
    
    # Normalize apostrophes in references keys for matching
    normalized_refs = {}
    for key, value in references.items():
        # Normalize all types of curly apostrophes to straight ones
        normalized_key = key.replace("'", "'").replace("'", "'").replace("\u2019", "'").replace("\u2018", "'")
        normalized_refs[normalized_key] = value
        normalized_refs[key] = value  # Keep original too
    
    # First, replace numbered references like [1], [2], [3]
    if numbered_refs:
        def replace_num_ref(match):
            ref_num = int(match.group(1))
            if ref_num in numbered_refs:
                url = numbered_refs[ref_num]['url']
                source_name = numbered_refs[ref_num].get('source_name', f'Source {ref_num}')
                title = numbered_refs[ref_num]['title'][:50] + '...' if len(numbered_refs[ref_num]['title']) > 50 else numbered_refs[ref_num]['title']
                return f'<a href="{html.escape(url)}" target="_blank" title="{html.escape(title)}" class="ref-link">[{html.escape(source_name)}]</a>'
            return match.group(0)
        
        text = re.sub(r'\[(\d+)\]', replace_num_ref, text)
    
    # Then, replace source name references like [Motley Fool], [24/7 Wall St], [Ward's Auto]
    def replace_source_ref(match):
        source_name = match.group(1)
        # Normalize all types of apostrophes to straight apostrophe for matching
        normalized_name = source_name.replace("'", "'").replace("'", "'").replace("\u2019", "'").replace("\u2018", "'").replace("`", "'").replace("\u0027", "'")
        
        # Try to find the source in references
        ref_data = None
        display_name = source_name
        if normalized_name in normalized_refs:
            ref_data = normalized_refs[normalized_name]
            display_name = normalized_name
        elif source_name in normalized_refs:
            ref_data = normalized_refs[source_name]
            display_name = source_name
        else:
            # Handle [Source 1] -> [Source] fallback (first source has no number)
            if normalized_name.endswith(' 1'):
                base_name = normalized_name[:-2]  # Remove " 1"
                if base_name in normalized_refs:
                    ref_data = normalized_refs[base_name]
                    display_name = base_name
        
        if ref_data:
            url = ref_data['url']
            title = ref_data['title'][:50] + '...' if len(ref_data['title']) > 50 else ref_data['title']
            return f'<a href="{html.escape(url)}" target="_blank" title="{html.escape(title)}" class="ref-link">[{html.escape(display_name)}]</a>'
        return match.group(0)
    
    # Match [Source Name] patterns - can start with letter or number, contain spaces, apostrophes (all variants), slashes, etc.
    # Include straight apostrophe ', left curly ', right curly ', backtick `, and common punctuation
    # Also handle HTML-encoded apostrophes that might slip through
    text = re.sub(r"&#39;|&#x27;|&apos;", "'", text)  # Decode any HTML-encoded apostrophes first
    text = re.sub(r"\[([A-Za-z0-9][A-Za-z0-9\s'''`\u2019\u2018\u0027./&-]+?)\]", replace_source_ref, text)
    
    return text

def _strip_leading_artifacts(text: str) -> str:
    cleaned = text.strip()
    # Remove invisible Unicode characters
    cleaned = re.sub(r"^[\u200B-\u200F\uFEFF]+", "", cleaned)
    # Remove leading bullets, dashes, and similar markers
    cleaned = re.sub(r"^[•·\-\u2010-\u2015\u2212\*]+\s*", "", cleaned)
    # Remove any remaining leading dash after whitespace
    cleaned = re.sub(r"^\s*-\s+", "", cleaned)
    return cleaned.strip()

def _format_point(point: str, references: dict[str, dict[str, str]] = None, numbered_refs: dict[int, dict[str, str]] = None) -> str:
    sentence = _strip_leading_artifacts(point)
    
    # Convert references to links BEFORE HTML escaping (so apostrophes aren't escaped)
    if references:
        sentence = _convert_references_to_links(sentence, references, numbered_refs)
    
    # Now we need to escape only the non-link parts
    # Split on link tags, escape non-tag parts, then rejoin
    if '<a href=' in sentence:
        # Protect existing link tags while escaping the rest
        parts = re.split(r'(<a href="[^"]*"[^>]*>\[[^\]]+\]</a>)', sentence)
        escaped_parts = []
        for part in parts:
            if part.startswith('<a href='):
                escaped_parts.append(part)  # Keep link as-is
            else:
                # Format with heading if there's a colon in this part
                escaped_parts.append(html.escape(part))
        formatted = ''.join(escaped_parts)
    else:
        # No links, just escape normally
        if ":" in sentence:
            colon_idx = sentence.index(":")
            heading = sentence[:colon_idx]
            remainder = sentence[colon_idx+1:]
            formatted = f"<strong>{html.escape(heading.strip())}:</strong> {html.escape(remainder.strip())}"
        else:
            formatted = html.escape(sentence)
    
    # Handle heading formatting for sentences with links
    if '<a href=' in formatted and ":" in formatted:
        # Check if the colon is before any link AND not inside a link
        first_link_idx = formatted.find("<a href=")
        text_before_link = formatted[:first_link_idx]
        # Only apply heading formatting if there's a colon in the text before the first link
        if ":" in text_before_link:
            colon_idx = text_before_link.index(":")
            heading = formatted[:colon_idx]
            remainder = formatted[colon_idx+1:]
            formatted = f"<strong>{heading.strip()}:</strong> {remainder.strip()}"
    
    return formatted

def _split_concatenated_points(points: list[str]) -> list[str]:
    """Split points that contain multiple sub-points separated by ' - ' patterns after source names."""
    result = []
    for point in points:
        # Pattern: source name like [Motley Fool] followed by "." then " - " then new sentence
        # Or just ". - " followed by capital letter (new sentence)
        # Use lookbehind to keep the ] with the first part
        pattern = r'(?<=\])\.?\s*-\s+(?=[A-Z])|(?<=\.)\s*-\s+(?=[A-Z])'
        
        if re.search(pattern, point):
            # Split and clean
            parts = re.split(pattern, point)
            cleaned_parts = []
            for part in parts:
                part = part.strip()
                if part:
                    cleaned_parts.append(part)
            result.extend(cleaned_parts)
        else:
            result.append(point)
    return result

# Common ticker to company name mapping
TICKER_TO_COMPANY = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft', 
    'GOOGL': 'Google',
    'GOOG': 'Google',
    'AMZN': 'Amazon',
    'META': 'Meta',
    'TSLA': 'Tesla',
    'NVDA': 'NVIDIA',
    'F': 'Ford',
    'GM': 'General Motors',
    'TM': 'Toyota',
    'HMC': 'Honda',
    'RIVN': 'Rivian',
    'NIO': 'NIO',
    'LCID': 'Lucid',
    'JPM': 'JPMorgan',
    'BAC': 'Bank of America',
    'WFC': 'Wells Fargo',
    'C': 'Citigroup',
    'GS': 'Goldman Sachs',
    'V': 'Visa',
    'MA': 'Mastercard',
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer',
    'UNH': 'UnitedHealth',
    'MRK': 'Merck',
    'ABBV': 'AbbVie',
    'LLY': 'Eli Lilly',
    'WMT': 'Walmart',
    'TGT': 'Target',
    'COST': 'Costco',
    'HD': 'Home Depot',
    'DIS': 'Disney',
    'NFLX': 'Netflix',
    'BA': 'Boeing',
    'LMT': 'Lockheed Martin',
    'XOM': 'ExxonMobil',
    'CVX': 'Chevron',
}

def _get_company_display(ticker: str) -> str:
    """Get display name for a ticker (Company Name (TICKER) or just TICKER)."""
    if ticker in TICKER_TO_COMPANY:
        return f"{TICKER_TO_COMPANY[ticker]} ({ticker})"
    return ticker

def _replace_tickers_with_names(text: str) -> str:
    """Replace standalone tickers at the start of sentences with Company Name (TICKER) format."""
    # Pattern: ticker at start of text or after period/newline, followed by space and more text
    def replace_ticker(match):
        prefix = match.group(1)  # The boundary before ticker (start, period+space, etc.)
        ticker = match.group(2)
        suffix = match.group(3)  # What comes after (space, 's, etc.)
        if ticker in TICKER_TO_COMPANY:
            return f"{prefix}{TICKER_TO_COMPANY[ticker]} ({ticker}){suffix}"
        return match.group(0)
    
    # Match ticker at start of string or after sentence boundary, followed by space or 's
    result = re.sub(r"(^|(?<=[.!?]\s))([A-Z]{1,5})(\s|'s)", replace_ticker, text)
    return result

def _extract_other_reasons(sections: list[str], recommended_ticker: Optional[str]) -> list[tuple[str, str]]:
    reasons: list[tuple[str, str]] = []
    for block in sections:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", block) if s.strip()]
        for sentence in sentences:
            sentence = _strip_leading_artifacts(sentence)
            if sentence.lower().startswith("the other"):
                continue
            ticker_match = re.match(r"([A-Z]{1,6})\s+(.+)", sentence)
            if ticker_match:
                ticker, remainder = ticker_match.groups()
                if recommended_ticker and ticker == recommended_ticker:
                    continue
                # Don't truncate to first sentence - keep full explanation
                trimmed = remainder.lstrip(":- ")
                reasons.append((ticker, trimmed))
            elif reasons:
                ticker, prev = reasons[-1]
                reasons[-1] = (ticker, prev + " " + sentence)
    return [(ticker, html.escape(reason.strip())) for ticker, reason in reasons if reason.strip()]

def _clean_other_reason_text(ticker: str, text: str) -> str:
    cleaned = re.sub(rf"^{ticker}\b[:,\s-]*", "", text, flags=re.IGNORECASE).strip()
    cleaned = re.sub(rf"^[A-Za-z\s]*\({ticker}\)\s*", "", cleaned).strip()
    cleaned = re.sub(
        r"^(was|is|remains)\s+(not\s+chosen|not\s+selected|excluded)\s*(due to|because of)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()
    return cleaned or text

def render_explanation(explanation: str, recommended_ticker: Optional[str] = None, references: dict[str, dict[str, str]] = None, numbered_refs: dict[int, dict[str, str]] = None):
    """Render explanation text with summary, key points, and competitor rationale."""

    if not explanation:
        return

    explanation = re.sub(
        r"(?m)^[\s•·\-\u2010-\u2015\u2212]*2(?=\S)",
        "",
        explanation,
    )

    sections = [sec.strip() for sec in explanation.strip().split("\n\n") if sec.strip()]
    if not sections:
        st.write(explanation)
        return

    # Get first sentence and strip leading artifacts for display
    first_section_cleaned = _strip_leading_artifacts(sections[0])
    original_summary = _first_sentence(first_section_cleaned)
    extra_detail = first_section_cleaned[len(original_summary):].strip() if first_section_cleaned.startswith(original_summary) else ""
    extra_sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", extra_detail) if s.strip()]
    # Replace standalone tickers with company names for clarity
    summary_text = _replace_tickers_with_names(original_summary)

    # Convert references to links in summary, then escape non-link parts
    summary_with_links = _convert_references_to_links(summary_text, references, numbered_refs)
    if '<a href=' in summary_with_links:
        # Protect existing link tags while escaping the rest
        parts = re.split(r'(<a href="[^"]*"[^>]*>\[[^\]]+\]</a>)', summary_with_links)
        escaped_parts = []
        for part in parts:
            if part.startswith('<a href='):
                escaped_parts.append(part)
            else:
                escaped_parts.append(html.escape(part))
        summary_html = ''.join(escaped_parts)
    else:
        summary_html = html.escape(summary_with_links)

    st.markdown(
        f"<div class='explanation-summary'>{summary_html}</div>",
        unsafe_allow_html=True,
    )

    key_points: list[str] = []
    other_blocks: list[str] = []

    for section in sections[1:]:
        lower_section = section.lower()
        if lower_section.startswith("key points"):
            lines = [line.strip() for line in section.splitlines() if line.strip()]
            for line in lines[1:]:
                if line[0].isdigit() and ". " in line:
                    _, remainder = line.split(". ", 1)
                    key_points.append(remainder)
                else:
                    key_points.append(line)
        elif lower_section.startswith("the other") or re.match(r"^[A-Z]{1,6}\s", section):
            other_blocks.append(section)
        else:
            key_points.append(section)

    if extra_sentences:
        key_points = extra_sentences + key_points

    extracted_other_from_points: list[tuple[str, str]] = []
    filtered_points: list[str] = []
    contrast_markers = [
        "not chosen",
        "not selected",
        "wasn't chosen",
        "excluded",
        "in contrast",
        "while ",
        "whereas",
        "however",
    ]

    for point in key_points:
        if not point:
            continue
        cleaned_point = _strip_leading_artifacts(point)
        lower_point = cleaned_point.lower()
        tickers_in_point = re.findall(r"\b([A-Z]{1,6})\b", cleaned_point)
        tickers_in_point = [t for t in tickers_in_point if not recommended_ticker or t != recommended_ticker]
        if tickers_in_point and any(phrase in lower_point for phrase in contrast_markers):
            ticker = tickers_in_point[0]
            sentence = _first_sentence(cleaned_point)
            cleaned_reason = _clean_other_reason_text(ticker, sentence) or sentence
            extracted_other_from_points.append((ticker, html.escape(cleaned_reason)))
        else:
            filtered_points.append(cleaned_point)

    key_points = filtered_points
    
    # Split any concatenated points into separate bullets
    key_points = _split_concatenated_points(key_points)

    rendered_any = False
    if key_points:
        rendered_points = ''.join(f"<li>{_format_point(point, references, numbered_refs)}</li>" for point in key_points)
        st.markdown(
            "<div class='explanation-section-title'>Why this company</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<ul class='explanation-list'>{rendered_points}</ul>",
            unsafe_allow_html=True,
        )
        rendered_any = True

    other_reasons = _extract_other_reasons(other_blocks, recommended_ticker)
    other_reasons.extend(extracted_other_from_points)

    deduped_other: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for ticker, reason in other_reasons:
        if not ticker or (recommended_ticker and ticker == recommended_ticker):
            continue
        key = (ticker, reason)
        if key in seen:
            continue
        deduped_other.append((ticker, reason))
        seen.add(key)

    if deduped_other:
        def format_other_reason(ticker: str, reason: str) -> str:
            formatted_reason = reason
            if references:
                formatted_reason = _convert_references_to_links(reason, references, numbered_refs)
            display_name = _get_company_display(ticker)
            return f"<li><strong>{html.escape(display_name)}:</strong> {formatted_reason}</li>"
        
        rendered_others = ''.join(
            format_other_reason(ticker, reason) for ticker, reason in deduped_other
        )
        st.markdown(
            "<div class='explanation-section-title'>Why not others</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<ul class='explanation-list'>{rendered_others}</ul>",
            unsafe_allow_html=True,
        )
        rendered_any = True

    if not rendered_any:
        st.write(explanation)
# Mock query engine for testing (replaces llama_index/faiss)
def get_relevant_news(industry: str, company: str) -> str:
    """Return mock relevant news for testing."""
    return f"Recent developments for {company} in the {industry} industry show positive momentum with strong market positioning and growth prospects."

def _parse_news_references(news_summaries: str) -> tuple[str, dict[str, dict[str, str]], dict[int, dict[str, str]]]:
    """Parse news summaries and create reference lists.
    
    Returns:
        tuple: (original news summaries, 
                reference dict mapping source name to {title, url},
                reference dict mapping number to {title, url, source_name})
    """
    references: dict[str, dict[str, str]] = {}
    numbered_refs: dict[int, dict[str, str]] = {}
    current_title = None
    current_url = None
    
    # First pass: collect all title-url pairs
    news_items = []
    for line in news_summaries.split('\n'):
        if line.startswith('- '):
            # Save previous item if exists
            if current_title:
                news_items.append({'title': current_title, 'url': current_url})
            # Start new item
            current_title = line[2:]
            current_url = None
        elif line.strip().startswith('Source:'):
            current_url = line.replace('Source:', '').strip()
    
    # Don't forget the last item
    if current_title:
        news_items.append({'title': current_title, 'url': current_url})
    
    # Build references dict keyed by source name (only items with URLs)
    ref_num = 1
    for item in news_items:
        if item['url']:
            title_only = item['title'].split(' (Published:')[0] if ' (Published:' in item['title'] else item['title']
            source_name = _extract_source_name(item['url'])
            
            # Handle duplicate sources
            final_source_name = source_name
            if source_name in references:
                i = 2
                while f"{source_name} {i}" in references:
                    i += 1
                final_source_name = f"{source_name} {i}"
            
            references[final_source_name] = {'title': title_only, 'url': item['url']}
            numbered_refs[ref_num] = {'title': title_only, 'url': item['url'], 'source_name': final_source_name}
            ref_num += 1
    
    return news_summaries, references, numbered_refs


def recommend_investment(industry: str, tickers: str, news_summaries: str, model_choice: str="gpt-4o-mini") -> tuple[str, dict[str, dict[str, str]], dict[int, dict[str, str]]]:
    """Return mock investment recommendation for testing."""
    return get_mock_recommendation(industry)


# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'recommendation' not in st.session_state:
    st.session_state['recommendation'] = ""
if 'tickers' not in st.session_state:
    st.session_state['tickers'] = ""
if 'news_summaries' not in st.session_state:
    st.session_state['news_summaries'] = ""
if 'news_references' not in st.session_state:
    st.session_state['news_references'] = {}
if 'numbered_references' not in st.session_state:
    st.session_state['numbered_references'] = {}
if 'last_duration' not in st.session_state:
    st.session_state['last_duration'] = None
# Performance tracker - stores tracked recommendations
if 'tracked_recommendations' not in st.session_state:
    st.session_state['tracked_recommendations'] = []


def is_ticker_tracked(ticker: str) -> bool:
    """Check if a ticker is already in the tracked recommendations."""
    for rec in st.session_state['tracked_recommendations']:
        if rec['ticker'] == ticker:
            return True
    return False


def add_to_tracker(ticker: str, industry: str, recommendation_date: str, 
                   recommendation_price: float, recommendation_text: str):
    """Add a stock recommendation to the performance tracker."""
    if not is_ticker_tracked(ticker):
        st.session_state['tracked_recommendations'].append({
            'ticker': ticker,
            'industry': industry,
            'recommendation_date': recommendation_date,
            'recommendation_price': recommendation_price,
            'recommendation_text': recommendation_text,
            'company_name': TICKER_TO_COMPANY.get(ticker, ticker)
        })
        return True
    return False


def remove_from_tracker(ticker: str):
    """Remove a stock from the performance tracker."""
    st.session_state['tracked_recommendations'] = [
        rec for rec in st.session_state['tracked_recommendations'] 
        if rec['ticker'] != ticker
    ]

def generate_response(prompt, recommendation, model_choice="gpt-4o-mini"):
    """Return mock chat response for testing."""
    st.session_state['messages'].append({"role": "user", "content": prompt})

    bot_response = get_mock_chat_response(prompt, recommendation)
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})

    return bot_response

def main():
    st.markdown(
        """
        <div class="app-header">
            <div>
                <div class="app-title">Investment Advisor Pro</div>
                <div class="app-subtitle">AI-powered investment insights from recent industry news</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # Main Navigation
        st.markdown("<div class='nav-section'>Navigate</div>", unsafe_allow_html=True)
        
        # Navigation state
        if 'nav_page' not in st.session_state:
            st.session_state['nav_page'] = 'search'
        
        # Navigation buttons
        col1, = st.columns(1)
        if st.button("⌕  Search", key="nav_search", use_container_width=True, 
                     type="primary" if st.session_state['nav_page'] == 'search' else "secondary"):
            st.session_state['nav_page'] = 'search'
            
        if st.button("⌂  Home", key="nav_home", use_container_width=True,
                     type="primary" if st.session_state['nav_page'] == 'home' else "secondary"):
            st.session_state['nav_page'] = 'home'
            
        # Show count of tracked recommendations
        tracked_count = len(st.session_state.get('tracked_recommendations', []))
        watchlist_label = f"☆  Tracker ({tracked_count})" if tracked_count > 0 else "☆  Tracker"
        if st.button(watchlist_label, key="nav_watchlist", use_container_width=True,
                     type="primary" if st.session_state['nav_page'] == 'watchlist' else "secondary"):
            st.session_state['nav_page'] = 'watchlist'
            
        if st.button("↺  History", key="nav_history", use_container_width=True,
                     type="primary" if st.session_state['nav_page'] == 'history' else "secondary"):
            st.session_state['nav_page'] = 'history'
        
        # Library Section
        st.markdown("<div class='nav-section'>Library</div>", unsafe_allow_html=True)
        
        if st.button("◎  Recommendations", key="nav_recent", use_container_width=True):
            st.session_state['nav_page'] = 'recent'
            
        if st.button("⊞  Industries", key="nav_industries", use_container_width=True):
            st.session_state['nav_page'] = 'industries'
            
        if st.button("☰  Saved News", key="nav_news", use_container_width=True):
            st.session_state['nav_page'] = 'news'
        
        # Settings Section
        st.markdown("<div class='nav-section'>Settings</div>", unsafe_allow_html=True)

        model_choice = st.selectbox(
            "Language Model",
            ["Mock Mode (Testing)"],
            help="Using mock responses for testing - no API calls",
            label_visibility="collapsed"
        )
        
        # Disclaimer at bottom
        st.markdown("<div style='flex-grow: 1; min-height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='font-size: 0.7rem; color: #9ca3af; line-height: 1.4; padding: 12px;'>"
            "<strong>Disclaimer:</strong> AI-generated insights. Not financial advice. "
            "Consult a qualified advisor."
            "</div>",
            unsafe_allow_html=True
        )

    # Industry tiles data
    INDUSTRY_TILES = [
        {"name": "Technology", "icon": "💻", "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
        {"name": "Healthcare", "icon": "🏥", "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"},
        {"name": "Finance", "icon": "💰", "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"},
        {"name": "Energy", "icon": "⚡", "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"},
        {"name": "Automotive", "icon": "🚗", "gradient": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"},
        {"name": "Retail", "icon": "🛒", "gradient": "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"},
        {"name": "Real Estate", "icon": "🏠", "gradient": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)"},
        {"name": "Airlines", "icon": "✈️", "gradient": "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)"},
        {"name": "Entertainment", "icon": "🎬", "gradient": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"},
        {"name": "Pharmaceuticals", "icon": "💊", "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"},
        {"name": "Banking", "icon": "🏦", "gradient": "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)"},
        {"name": "Semiconductors", "icon": "🔌", "gradient": "linear-gradient(135deg, #eb3349 0%, #f45c43 100%)"},
    ]

    # ============ PAGE ROUTING ============
    
    if st.session_state['nav_page'] == 'home':
        # HOME PAGE - Browse Industries
        st.markdown("<div class='section-title'>Browse Industries</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Click an industry to get AI-powered investment recommendations</div>", unsafe_allow_html=True)
        
        # Create industry tiles in rows of 4
        for row_start in range(0, len(INDUSTRY_TILES), 4):
            cols = st.columns(4)
            for col_idx, industry_data in enumerate(INDUSTRY_TILES[row_start:row_start+4]):
                with cols[col_idx]:
                    # Create a styled tile using markdown + button
                    st.markdown(f"""
                    <style>
                    div[data-testid="stButton"]:has(button[key="tile_{industry_data['name']}"]) button {{
                        background: {industry_data['gradient']} !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"{industry_data['icon']}  {industry_data['name']}", 
                               key=f"tile_{industry_data['name']}", 
                               use_container_width=True):
                        st.session_state['selected_industry'] = industry_data['name']
                        st.session_state['nav_page'] = 'search'
                        st.session_state['auto_search'] = True
                        st.rerun()
    
    elif st.session_state['nav_page'] == 'watchlist':
        # WATCHLIST PAGE - Show tracked recommendations
        st.markdown("<div class='section-title'>Performance Tracker</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Track how your AI-recommended stocks are performing</div>", unsafe_allow_html=True)
        
        tracked = st.session_state.get('tracked_recommendations', [])
        
        if not tracked:
            st.info("📊 No stocks being tracked yet. Get a recommendation and click 'Add to Tracker' to start tracking performance!")
        else:
            st.markdown(f"**{len(tracked)} stock(s) being tracked**")
            
            # Compact styling for the tracker table
            st.markdown("""
            <style>
            .compact-tracker [data-testid="stVerticalBlock"] { gap: 0 !important; }
            .compact-tracker [data-testid="stHorizontalBlock"] { align-items: center !important; gap: 0 !important; }
            .compact-tracker [data-testid="stVerticalBlock"] > div { margin: 0 !important; padding: 0 !important; }
            .compact-tracker [data-testid="column"] > div { padding: 0 !important; }
            .compact-tracker [data-testid="stMarkdownContainer"] { margin: 0 !important; padding: 0 !important; }
            .compact-tracker [data-testid="stMarkdownContainer"] > div { margin: 0 !important; padding: 0 !important; }
            .compact-tracker [data-testid="stMarkdownContainer"] p { margin: 0 !important; padding: 0 !important; }
            .compact-tracker [data-testid="stMarkdownContainer"] hr { margin: 0 !important; }
            .compact-tracker .stButton { margin: 0 !important; padding: 0 !important; }
            .compact-tracker .stButton > button {
                padding: 0 4px !important; min-height: 18px !important; height: 18px !important;
                font-size: 10px !important; line-height: 1 !important;
                background: transparent !important; border: none !important; color: #9ca3af !important;
            }
            .compact-tracker .stButton > button:hover { color: #dc2626 !important; background-color: #fee2e2 !important; }
            .t-cell { font-size: 13px; line-height: 1.2; padding: 4px 0; margin: 0; }
            .t-header { font-weight: 600; font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 0; margin: 0; }
            .t-header-lower { text-transform: none; }
            .t-stock { font-weight: 600; color: #111827; }
            .t-ticker { color: #6b7280; }
            .t-date { color: #6b7280; font-size: 12px; }
            .t-up { color: #16a34a; font-weight: 500; }
            .t-down { color: #dc2626; font-weight: 500; }
            .t-hr { border: none; border-top: 1px solid #f3f4f6; margin: 0 !important; padding: 0 !important; }
            .t-hr-header { border: none; border-top: 2px solid #e5e7eb; margin: 0 !important; padding: 0 !important; }
            </style>
            <div class="compact-tracker">
            """, unsafe_allow_html=True)
            
            # Column headers
            h1, h2, h3, h4, h5, h6, h7, h8, h9 = st.columns([3, 1.6, 1, 1.8, 1, 1, 1, 1, 0.4])
            h1.markdown("<p class='t-header'>Stock</p>", unsafe_allow_html=True)
            h2.markdown("<p class='t-header'>Added</p>", unsafe_allow_html=True)
            h3.markdown("<p class='t-header'>Entry</p>", unsafe_allow_html=True)
            h4.markdown("<p class='t-header'>Current / Change</p>", unsafe_allow_html=True)
            h5.markdown("<p class='t-header'>1 Week</p>", unsafe_allow_html=True)
            h6.markdown("<p class='t-header'>1 Month</p>", unsafe_allow_html=True)
            h7.markdown("<p class='t-header'>3 Months</p>", unsafe_allow_html=True)
            h8.markdown("<p class='t-header t-header-lower'>vs S&P 500</p>", unsafe_allow_html=True)
            h9.markdown("<p class='t-header'></p>", unsafe_allow_html=True)
            st.markdown("<hr class='t-hr-header'>", unsafe_allow_html=True)
            
            # Data rows
            for idx, rec in enumerate(tracked):
                ticker = rec['ticker']
                company_name = rec.get('company_name', ticker)
                rec_date = rec.get('recommendation_date', 'Unknown')
                rec_price = rec.get('recommendation_price', 0)
                
                current_info = get_stock_info(ticker)
                current_price = current_info.get('currentPrice') or current_info.get('regularMarketPrice') or 0
                
                if rec_price and rec_price > 0 and current_price:
                    pct_change = ((current_price - rec_price) / rec_price) * 100
                    if pct_change >= 0:
                        change_html = f"${current_price:.2f} <span class='t-up'>▲ {abs(pct_change):.2f}%</span>"
                    else:
                        change_html = f"${current_price:.2f} <span class='t-down'>▼ {abs(pct_change):.2f}%</span>"
                else:
                    change_html = "N/A"
                
                price_html = f"${rec_price:.2f}" if rec_price else "N/A"

                week_change = format_percentage_change(
                    calculate_percentage_change(ticker, period="5d")
                )
                month_change = format_percentage_change(
                    calculate_percentage_change(ticker, period="1mo")
                )
                quarter_change = format_percentage_change(
                    calculate_percentage_change(ticker, period="3mo")
                )
                alpha_change = format_percentage_change(
                    calculate_alpha_vs_sp500(ticker, _parse_tracker_date(rec_date))
                )
                
                c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([3, 1.6, 1, 1.8, 1, 1, 1, 1, 0.4])
                c1.markdown(f"<p class='t-cell'><span class='t-stock'>{company_name}</span> <span class='t-ticker'>({ticker})</span></p>", unsafe_allow_html=True)
                c2.markdown(f"<p class='t-cell t-date'>{rec_date}</p>", unsafe_allow_html=True)
                c3.markdown(f"<p class='t-cell'>{price_html}</p>", unsafe_allow_html=True)
                c4.markdown(f"<p class='t-cell'>{change_html}</p>", unsafe_allow_html=True)
                c5.markdown(f"<p class='t-cell'>{week_change}</p>", unsafe_allow_html=True)
                c6.markdown(f"<p class='t-cell'>{month_change}</p>", unsafe_allow_html=True)
                c7.markdown(f"<p class='t-cell'>{quarter_change}</p>", unsafe_allow_html=True)
                c8.markdown(f"<p class='t-cell'>{alpha_change}</p>", unsafe_allow_html=True)
                if c9.button("✕", key=f"del_{idx}", help="Remove"):
                    remove_from_tracker(ticker)
                    st.rerun()
                st.markdown("<hr class='t-hr'>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state['nav_page'] == 'history':
        # HISTORY PAGE
        st.markdown("<div class='section-title'>Search History</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Your recent searches will appear here</div>", unsafe_allow_html=True)
        st.info("🚧 Coming soon! Your search history will be saved here.")
    
    elif st.session_state['nav_page'] in ['recent', 'industries', 'news']:
        # LIBRARY PAGES (Coming Soon)
        page_names = {'recent': 'Recent Recommendations', 'industries': 'Saved Industries', 'news': 'Saved News'}
        st.markdown(f"<div class='section-title'>{page_names[st.session_state['nav_page']]}</div>", unsafe_allow_html=True)
        st.info("🚧 Coming soon!")
    
    else:
        # SEARCH PAGE (default)
        # Check for auto-search from tile click
        if st.session_state.get('auto_search') and st.session_state.get('selected_industry'):
            industry = st.session_state['selected_industry']
            st.session_state['auto_search'] = False
        else:
            industry = st.text_input("Enter an industry name:", help="e.g., Technology, Healthcare, Finance",
                                    value=st.session_state.get('selected_industry', ''))

        if st.button("Get Recommendation", key="recommend") or st.session_state.get('auto_search'):
            if industry:
                st.session_state['auto_search'] = False  # Reset flag
                with st.spinner(f"Analyzing the {industry} industry..."):
                    start_time = time.time()
                    
                    progress_bar = st.progress(0)
                    
                    # Fetch data
                    tickers, news_summaries = get_industry_data(industry)
                    progress_bar.progress(50)
                    
                    # Generate recommendation
                    recommendation, references, numbered_refs = recommend_investment(industry, tickers, news_summaries, model_choice=model_choice)
                    st.session_state['recommendation'] = recommendation
                    st.session_state['tickers'] = tickers
                    st.session_state['news_summaries'] = news_summaries
                    st.session_state['news_references'] = references
                    st.session_state['numbered_references'] = numbered_refs
                    progress_bar.progress(100)
                    
                    end_time = time.time()
                    st.session_state['last_duration'] = end_time - start_time
                
            else:
                st.warning("Please enter an industry name.")

        if st.session_state['recommendation']:
            recommendation_parts = st.session_state['recommendation'].split("Explanation:", 1)
            recommendation_text = recommendation_parts[0].strip()
            explanation = recommendation_parts[1].strip() if len(recommendation_parts) > 1 else ""
            recommended_ticker = extract_recommended_ticker(recommendation_text)

            display_value = recommended_ticker or ""
            if not display_value:
                stripped_text = recommendation_text.strip()
                if ":" in stripped_text:
                    display_value = stripped_text.split(":", 1)[1].strip()
                else:
                    display_value = stripped_text
            if display_value.lower().startswith("recommendation") and ":" in display_value:
                display_value = display_value.split(":", 1)[1].strip()
            if not display_value:
                display_value = "—"
            
            # Add company name to the display value
            if recommended_ticker:
                display_value = _get_company_display(recommended_ticker)

            # Track/Untrack button inline with recommendation
            if recommended_ticker:
                is_tracked = is_ticker_tracked(recommended_ticker)
                
                # Get current price for tracking
                current_info = get_stock_info(recommended_ticker)
                current_price = current_info.get('currentPrice') or current_info.get('regularMarketPrice') or 0
                
                if is_tracked:
                    # Show recommendation with tracking badge, and small untrack button
                    col_main, col_btn = st.columns([6, 1])
                    with col_main:
                        st.markdown(
                            f"<div class='recommendation-line'>Recommendation: <span class='value'>{display_value}</span><span class='tracker-badge'><span class='tick'>✓</span> Tracking</span></div>",
                            unsafe_allow_html=True
                        )
                    with col_btn:
                        if st.button("✕", key="untrack_btn", help="Stop tracking"):
                            remove_from_tracker(recommended_ticker)
                            st.rerun()
                else:
                    # Show recommendation with track button
                    col_main, col_btn = st.columns([6, 1])
                    with col_main:
                        st.markdown(
                            f"<div class='recommendation-line'>Recommendation: <span class='value'>{display_value}</span></div>",
                            unsafe_allow_html=True
                        )
                    with col_btn:
                        if st.button("+ Track", key="track_btn", help="Add to performance tracker"):
                            industry_name = st.session_state.get('selected_industry', 'Unknown')
                            add_to_tracker(
                                ticker=recommended_ticker,
                                industry=industry_name,
                                recommendation_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                                recommendation_price=current_price,
                                recommendation_text=explanation[:500] if explanation else ""
                            )
                            st.rerun()
            else:
                st.markdown(
                    f"<div class='recommendation-line'>Recommendation: <span class='value'>{display_value}</span></div>",
                    unsafe_allow_html=True
                )
            
            render_explanation(explanation, recommended_ticker, st.session_state.get('news_references', {}), st.session_state.get('numbered_references', {}))

            if recommended_ticker:
                info = get_stock_info(recommended_ticker)
                company_name = info.get("shortName") or info.get("longName") or recommended_ticker
                exchange = info.get("exchange") or ""
                st.markdown(
                    f"<div style='font-weight:600; font-size:18px; margin:16px 0 6px 0;'>"
                    f"{company_name} <span style='color:#6b7280;'>({recommended_ticker})</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                if exchange:
                    st.caption(f"{exchange}: {recommended_ticker}")

                period_options = get_period_options()
                period_label = st.radio(
                    "Period",
                    list(period_options.keys()),
                    horizontal=True,
                    label_visibility="collapsed",
                    index=5,
                    key="price_period_selector"
                )
                period, interval = period_options[period_label]
                history = get_stock_history(recommended_ticker, period=period, interval=interval)
                if history is not None and not history.empty:
                    st.line_chart(history["Close"], height=220)

                    latest = history.iloc[-1]
                    prev_close = history["Close"].iloc[-2] if len(history) > 1 else latest["Close"]
                    day_range = format_range(latest.get("Low"), latest.get("High"))
                    year_low = info.get("fiftyTwoWeekLow")
                    year_high = info.get("fiftyTwoWeekHigh")
                    year_range = format_range(year_low, year_high)

                    metrics = [
                        ("Previous Close", format_number(prev_close)),
                        ("Open", format_number(latest.get("Open"))),
                        ("Day's Range", day_range),
                        ("52 Week Range", year_range),
                        ("Volume", format_number(latest.get("Volume"))),
                        ("Avg. Volume", format_number(info.get("averageVolume"))),
                        ("Market Cap", format_number(info.get("marketCap"))),
                        ("Beta (5Y Monthly)", format_number(info.get("beta"))),
                        ("PE Ratio (TTM)", format_number(info.get("trailingPE"))),
                        ("EPS (TTM)", format_number(info.get("trailingEps"))),
                        ("Earnings Date", format_date(info.get("earningsDate"))),
                        ("Forward Dividend & Yield", format_number(info.get("dividendRate"), "") + (f" ({info.get('dividendYield')*100:.2f}%)" if info.get("dividendYield") else "")),
                        ("Ex-Dividend Date", format_date(info.get("exDividendDate"))),
                        ("1y Target Est", format_number(info.get("targetMeanPrice")))
                    ]

                    rows = [metrics[i:i+4] for i in range(0, len(metrics), 4)]
                    for idx, row in enumerate(rows):
                        cols = st.columns(4, gap="small")
                        for col, item in zip(cols, row):
                            label, value = item
                            col.markdown(
                                f"<div class='metric-row'><span class='label'>{label}</span><span class='value'>{value}</span></div>",
                                unsafe_allow_html=True
                            )
                        if idx < len(rows) - 1:
                            st.markdown("<hr class='metrics-divider' />", unsafe_allow_html=True)
                else:
                    st.info("Price chart unavailable for the recommended ticker.")

            if recommended_ticker:
                st.markdown(
                    f"<div class='news-header'><div class='card-title'>Recent News: {recommended_ticker}</div></div>",
                    unsafe_allow_html=True
                )

                target_block = ""
                for company_news in st.session_state['news_summaries'].split('\n\n'):
                    if company_news.strip().startswith(f"News for {recommended_ticker}:"):
                        target_block = company_news
                        break

                if target_block:
                    lines = target_block.split('\n')[1:]
                    current_title = None
                    current_date = None
                    current_source = None
                    current_summary = None

                    def flush_card():
                        if not current_title:
                            return
                        title_escaped = html.escape(current_title)
                        # Make title clickable if we have a source URL
                        if current_source:
                            title_html = f"<a href='{html.escape(current_source)}' target='_blank' class='news-title-link'>{title_escaped}</a>"
                        else:
                            title_html = title_escaped
                        meta_parts = []
                        if current_source:
                            source_name = _extract_source_name(current_source)
                            meta_parts.append(f"Source: {html.escape(source_name)}")
                        if current_date:
                            meta_parts.append(html.escape(current_date))
                        meta_html = f"<div class='news-meta'>{' • '.join(meta_parts)}</div>" if meta_parts else ""
                        summary_html = ""
                        if current_summary:
                            summary_text = html.escape(current_summary).replace("\n", "<br />")
                            summary_html = f"<div class='news-summary'>{summary_text}</div>"
                        meta_section = f"\n    {meta_html}" if meta_html else ""
                        summary_section = f"\n    {summary_html}" if summary_html else ""
                        card_html = (
                            f"<div class='news-card'>\n"
                            f"    <div class='news-title'>{title_html}</div>"
                            f"{meta_section}"
                            f"{summary_section}\n"
                            f"</div>"
                        )
                        st.markdown(card_html, unsafe_allow_html=True)

                    for line in lines:
                        if line.startswith('- '):
                            flush_card()
                            current_title = line[2:]
                            current_date = None
                            current_source = None
                            current_summary = None
                            if ' (Published:' in current_title:
                                title, date = current_title.rsplit(' (Published:', 1)
                                current_title = title
                                current_date = date.rstrip(')')
                        elif line.startswith('  Summary:'):
                            current_summary = line[10:].strip()
                        elif line.startswith('  Source:'):
                            current_source = line[9:].strip()

                    flush_card()
                else:
                    st.info("No recent news found for the recommended ticker.")


if __name__ == "__main__":
    main()