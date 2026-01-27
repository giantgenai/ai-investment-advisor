"""
Mock responses for testing the investment advisor app without OpenAI, Ollama, or crawl4ai.

This module provides mock data for:
- Industry tickers
- News summaries
- Investment recommendations
- Chat responses

Usage:
    Simply import and use the mock functions - no API calls will be made.
"""

# Mock industry tickers
MOCK_INDUSTRY_TICKERS = {
    "technology": "NVDA, AAPL, MSFT",
    "healthcare": "LLY, JNJ, PFE",
    "finance": "JPM, BAC, GS",
    "automotive": "TSLA, F, GM",
    "energy": "XOM, CVX, BP",
    "retail": "WMT, TGT, COST",
    "airlines": "DAL, UAL, AAL",
    "entertainment": "DIS, NFLX, WBD",
    "pharmaceuticals": "LLY, PFE, MRK",
    "banking": "JPM, BAC, WFC",
    "semiconductors": "NVDA, AMD, INTC",
    "real estate": "PLD, AMT, SPG",
}

# Mock news summaries by industry
MOCK_NEWS_SUMMARIES = {
    "technology": """News for NVDA:
- NVIDIA Reports Record Revenue Driven by AI Demand (Published: 2024-01-15 09:30:00)
  Summary: NVIDIA announced record quarterly revenue of $22.1 billion, up 265% year-over-year, driven by unprecedented demand for AI chips and data center products.
  Source: https://www.reuters.com/technology/nvidia-record-revenue/
- NVIDIA Unveils Next-Generation Blackwell GPU Architecture (Published: 2024-01-14 14:00:00)
  Summary: The new Blackwell architecture promises 4x performance improvement for AI training workloads, positioning NVIDIA for continued market leadership.
  Source: https://www.fool.com/investing/nvidia-blackwell-announcement/
- Major Cloud Providers Expand NVIDIA Partnership (Published: 2024-01-13 11:00:00)
  Summary: AWS, Azure, and Google Cloud announce expanded partnerships with NVIDIA for next-generation AI infrastructure deployments.
  Source: https://www.bloomberg.com/news/nvidia-cloud-partnerships/

News for AAPL:
- Apple Vision Pro Launches with Strong Pre-orders (Published: 2024-01-12 10:00:00)
  Summary: Apple's Vision Pro spatial computing headset sees strong initial demand, though supply constraints may limit near-term availability.
  Source: https://www.cnbc.com/apple-vision-pro-launch/
- iPhone Sales Show Signs of Recovery in China (Published: 2024-01-11 08:30:00)
  Summary: Apple reports improved iPhone sales in China following recent price adjustments and promotional campaigns.
  Source: https://www.reuters.com/technology/apple-china-sales/
- Apple Faces EU Regulatory Challenges (Published: 2024-01-10 15:00:00)
  Summary: The EU's Digital Markets Act requirements may force Apple to open its App Store to alternative payment systems.
  Source: https://www.bloomberg.com/news/apple-eu-regulation/

News for MSFT:
- Microsoft Cloud Revenue Surges on AI Demand (Published: 2024-01-14 12:00:00)
  Summary: Microsoft's Azure cloud platform sees accelerated growth as enterprises adopt Copilot AI tools across productivity suite.
  Source: https://www.fool.com/investing/microsoft-cloud-growth/
- OpenAI Partnership Strengthens Microsoft's AI Position (Published: 2024-01-13 09:00:00)
  Summary: Continued investment in OpenAI positions Microsoft as a leader in enterprise AI solutions.
  Source: https://www.reuters.com/technology/microsoft-openai/
- Microsoft Gaming Division Shows Strong Performance (Published: 2024-01-12 11:00:00)
  Summary: Xbox Game Pass subscriptions reach record levels following Activision Blizzard acquisition completion.
  Source: https://www.cnbc.com/microsoft-gaming/
""",

    "healthcare": """News for LLY:
- Eli Lilly's Weight Loss Drug Demand Exceeds Supply (Published: 2024-01-15 08:00:00)
  Summary: Mounjaro and Zepbound continue to see unprecedented demand, with Eli Lilly investing $5.3 billion in new manufacturing capacity.
  Source: https://www.fool.com/investing/eli-lilly-weight-loss/
- Lilly Alzheimer's Drug Shows Promising Trial Results (Published: 2024-01-14 10:00:00)
  Summary: Phase 3 trial data for donanemab shows significant cognitive decline reduction in early Alzheimer's patients.
  Source: https://www.reuters.com/healthcare/lilly-alzheimers/
- Eli Lilly Stock Reaches All-Time High (Published: 2024-01-13 14:00:00)
  Summary: Strong pipeline and GLP-1 drug sales drive market cap past $600 billion, making Lilly the most valuable healthcare company.
  Source: https://www.bloomberg.com/news/lilly-stock-high/

News for JNJ:
- Johnson & Johnson Completes Consumer Health Spinoff (Published: 2024-01-12 09:00:00)
  Summary: J&J focuses on pharmaceuticals and medical devices following Kenvue separation, streamlining operations.
  Source: https://www.cnbc.com/jnj-kenvue/
- J&J Faces Ongoing Talc Litigation Challenges (Published: 2024-01-11 11:00:00)
  Summary: Settlement negotiations continue for talc-related lawsuits, creating uncertainty for investors.
  Source: https://www.reuters.com/business/jnj-talc/
- J&J Cancer Drug Portfolio Shows Growth (Published: 2024-01-10 13:00:00)
  Summary: Oncology segment revenues increase 15% year-over-year driven by new treatment approvals.
  Source: https://www.fool.com/investing/jnj-cancer-drugs/

News for PFE:
- Pfizer Revenue Declines as COVID Products Normalize (Published: 2024-01-14 07:30:00)
  Summary: Post-pandemic normalization leads to significant revenue decline, prompting cost-cutting measures.
  Source: https://www.bloomberg.com/news/pfizer-revenue/
- Pfizer Acquires Seagen for Cancer Treatment Pipeline (Published: 2024-01-13 08:00:00)
  Summary: $43 billion Seagen acquisition strengthens Pfizer's oncology portfolio for long-term growth.
  Source: https://www.reuters.com/healthcare/pfizer-seagen/
- Pfizer RSV Vaccine Shows Strong Market Uptake (Published: 2024-01-12 10:00:00)
  Summary: Abrysvo RSV vaccine gains market share in first full season of availability.
  Source: https://www.cnbc.com/pfizer-rsv/
""",

    "automotive": """News for TSLA:
- Tesla Cybertruck Production Ramps Up (Published: 2024-01-15 10:00:00)
  Summary: Tesla increases Cybertruck production at Gigafactory Texas, targeting 125,000 units for 2024.
  Source: https://electrek.co/tesla-cybertruck-production/
- Tesla Energy Storage Business Sees Record Growth (Published: 2024-01-14 09:00:00)
  Summary: Megapack deployments surge 200% year-over-year, becoming a significant revenue contributor.
  Source: https://www.fool.com/investing/tesla-energy/
- Full Self-Driving Beta Expands Globally (Published: 2024-01-13 11:00:00)
  Summary: Tesla's FSD supervised autonomy feature receives regulatory approval in additional markets.
  Source: https://www.reuters.com/technology/tesla-fsd/

News for F:
- Ford F-150 Lightning Sales Slow (Published: 2024-01-12 08:00:00)
  Summary: Electric truck sales decline amid pricing pressure and charging infrastructure concerns.
  Source: https://www.cnbc.com/ford-lightning/
- Ford Invests in Hybrid Technology Expansion (Published: 2024-01-11 10:00:00)
  Summary: Ford pivots strategy to emphasize hybrids as EV adoption slower than expected.
  Source: https://www.bloomberg.com/news/ford-hybrid/
- Ford Pro Commercial Division Shows Strength (Published: 2024-01-10 14:00:00)
  Summary: Commercial vehicle and fleet services segment delivers strong margins and growth.
  Source: https://www.reuters.com/business/ford-pro/

News for GM:
- GM Cruise Autonomous Division Faces Setback (Published: 2024-01-14 12:00:00)
  Summary: Cruise pauses driverless operations following incidents, impacting GM's autonomous vehicle timeline.
  Source: https://www.fool.com/investing/gm-cruise/
- GM EV Production Delays Continue (Published: 2024-01-13 09:00:00)
  Summary: Ultium platform production ramp slower than planned, affecting EV delivery targets.
  Source: https://www.cnbc.com/gm-ev-delays/
- GM Traditional Vehicle Sales Remain Strong (Published: 2024-01-12 11:00:00)
  Summary: Full-size truck and SUV sales provide stable revenue while EV transition continues.
  Source: https://www.reuters.com/business/gm-trucks/
""",

    "finance": """News for JPM:
- JPMorgan Reports Record Annual Profit (Published: 2024-01-15 07:00:00)
  Summary: JPMorgan Chase posts record $49.6 billion annual profit, benefiting from higher interest rates.
  Source: https://www.reuters.com/business/jpm-earnings/
- JPM Investment Banking Shows Recovery Signs (Published: 2024-01-14 10:00:00)
  Summary: M&A advisory and IPO underwriting activity increases as market conditions improve.
  Source: https://www.bloomberg.com/news/jpm-investment-banking/
- Jamie Dimon Warns of Economic Headwinds (Published: 2024-01-13 08:00:00)
  Summary: CEO expresses caution about inflation, rates, and geopolitical risks despite strong results.
  Source: https://www.cnbc.com/jpm-dimon/

News for BAC:
- Bank of America Net Interest Income Peaks (Published: 2024-01-12 09:00:00)
  Summary: NII reaches highest level in company history but may decline as Fed cuts rates.
  Source: https://www.fool.com/investing/bac-interest-income/
- BofA Digital Banking Users Surpass 45 Million (Published: 2024-01-11 11:00:00)
  Summary: Strong digital engagement drives efficiency improvements and customer retention.
  Source: https://www.reuters.com/business/bac-digital/
- Bank of America Wealth Management Grows (Published: 2024-01-10 13:00:00)
  Summary: Merrill Lynch and private banking divisions see increased asset inflows.
  Source: https://www.bloomberg.com/news/bac-wealth/

News for GS:
- Goldman Sachs Exits Consumer Banking (Published: 2024-01-14 08:00:00)
  Summary: Goldman retreats from Marcus consumer lending, refocusing on core institutional business.
  Source: https://www.cnbc.com/goldman-marcus/
- Goldman Trading Revenue Beats Expectations (Published: 2024-01-13 10:00:00)
  Summary: Fixed income and equities trading desks outperform amid market volatility.
  Source: https://www.reuters.com/business/goldman-trading/
- Goldman Asset Management Expands Alternatives (Published: 2024-01-12 12:00:00)
  Summary: Private credit and real estate fund offerings attract institutional investors.
  Source: https://www.bloomberg.com/news/goldman-alternatives/
""",

    "energy": """News for XOM:
- ExxonMobil Pioneer Merger Closes (Published: 2024-01-15 08:00:00)
  Summary: $60 billion Pioneer Natural Resources acquisition makes Exxon the largest Permian Basin producer.
  Source: https://www.reuters.com/business/exxon-pioneer/
- Exxon Boosts Shareholder Returns (Published: 2024-01-14 10:00:00)
  Summary: Company increases dividend and announces $20 billion share buyback program.
  Source: https://www.fool.com/investing/exxon-dividends/
- ExxonMobil Carbon Capture Projects Advance (Published: 2024-01-13 11:00:00)
  Summary: Major carbon capture and storage initiatives progress along Gulf Coast.
  Source: https://www.bloomberg.com/news/exxon-carbon/

News for CVX:
- Chevron Hess Acquisition Faces Arbitration (Published: 2024-01-12 09:00:00)
  Summary: ExxonMobil challenges Chevron's Hess deal over Guyana asset rights, adding uncertainty.
  Source: https://www.cnbc.com/chevron-hess/
- Chevron Production Grows in Permian (Published: 2024-01-11 10:00:00)
  Summary: U.S. shale production increases while international operations face challenges.
  Source: https://www.reuters.com/business/chevron-permian/
- Chevron Renewable Fuels Investment Expands (Published: 2024-01-10 14:00:00)
  Summary: Investments in renewable diesel and sustainable aviation fuel production grow.
  Source: https://www.bloomberg.com/news/chevron-renewables/

News for BP:
- BP Strategy Under Investor Scrutiny (Published: 2024-01-14 07:00:00)
  Summary: Shareholders question pace of energy transition and demand for higher returns.
  Source: https://www.reuters.com/business/bp-strategy/
- BP North Sea Operations Face Headwinds (Published: 2024-01-13 09:00:00)
  Summary: UK windfall taxes and declining production impact profitability.
  Source: https://www.bloomberg.com/news/bp-north-sea/
- BP Electric Vehicle Charging Network Grows (Published: 2024-01-12 11:00:00)
  Summary: BP Pulse expands fast-charging infrastructure across Europe and US.
  Source: https://www.fool.com/investing/bp-ev-charging/
""",
}

# Default mock news for unknown industries
DEFAULT_MOCK_NEWS = """News for SPY:
- S&P 500 Reaches New All-Time Highs (Published: 2024-01-15 09:00:00)
  Summary: Broad market rally continues as economic data supports soft landing narrative.
  Source: https://www.reuters.com/markets/sp500-high/
- Federal Reserve Signals Rate Cut Timeline (Published: 2024-01-14 14:00:00)
  Summary: Fed officials indicate potential rate reductions later this year if inflation continues to decline.
  Source: https://www.bloomberg.com/news/fed-rates/
- Corporate Earnings Season Kicks Off Strong (Published: 2024-01-13 10:00:00)
  Summary: Early Q4 earnings reports exceed expectations, supporting bullish market sentiment.
  Source: https://www.cnbc.com/earnings-season/
"""

# Mock investment recommendations by industry
MOCK_RECOMMENDATIONS = {
    "technology": """Recommendation: NVDA

Explanation:
NVIDIA stands out as the top technology investment due to its dominant position in AI chip manufacturing and data center growth [Motley Fool].

Key Points:
- Strong AI demand: NVIDIA's GPU sales have surged with the AI boom, driving record revenue growth [Reuters].
- Data center expansion: The company's data center segment grew 154% year-over-year, establishing market leadership [Bloomberg].
- Strategic partnerships: Major cloud providers continue to expand their NVIDIA-based infrastructure [CNBC].
- Innovation pipeline: The upcoming Blackwell architecture promises significant performance improvements [The Verge].

The other companies were not chosen for specific reasons:
AAPL was not chosen due to slower growth in the smartphone market and regulatory challenges [Motley Fool].
MSFT shows strong cloud performance but trades at higher valuation multiples [Reuters].
GOOGL faces ongoing antitrust concerns that may impact future growth [Bloomberg].""",

    "healthcare": """Recommendation: LLY

Explanation:
Eli Lilly emerges as the premier healthcare investment driven by its revolutionary weight-loss drug portfolio and strong pipeline [Motley Fool].

Key Points:
- GLP-1 leadership: Mounjaro and Zepbound are experiencing unprecedented demand globally [Reuters].
- Strong pipeline: Multiple late-stage candidates including Alzheimer's treatments show promise [Bloomberg].
- Revenue growth: The company projects 20%+ revenue growth for the coming years [CNBC].
- Market expansion: New indications and international launches will drive continued momentum [Seeking Alpha].

The other companies were not chosen for specific reasons:
JNJ faces litigation headwinds and slower pharmaceutical growth [Motley Fool].
PFE struggles with declining COVID-19 product revenues [Reuters].
UNH faces regulatory scrutiny over healthcare practices [Bloomberg].""",

    "finance": """Recommendation: JPM

Explanation:
JPMorgan Chase leads the financial sector with robust earnings and strong positioning across all business lines [Motley Fool].

Key Points:
- Interest income surge: Higher rates have boosted net interest income significantly [Reuters].
- Investment banking recovery: M&A and IPO activity is showing signs of improvement [Bloomberg].
- Technology leadership: Significant fintech investments position the bank for future growth [CNBC].
- Credit quality: Conservative lending practices have maintained strong loan portfolios [Barron's].

The other companies were not chosen for specific reasons:
BAC has higher exposure to rate sensitivity risks [Motley Fool].
GS faces headwinds in trading revenues [Reuters].
WFC continues to deal with regulatory constraints [Bloomberg].""",

    "automotive": """Recommendation: TSLA

Explanation:
Tesla remains the top automotive pick due to its EV leadership and energy business expansion [Motley Fool].

Key Points:
- Production scale: Gigafactory expansions continue to drive manufacturing efficiency [Reuters].
- Energy growth: The energy storage segment is becoming a significant revenue contributor [Bloomberg].
- FSD progress: Full Self-Driving technology continues to advance with regulatory approvals [Electrek].
- Brand strength: Tesla maintains premium positioning despite price competition [CNBC].

The other companies were not chosen for specific reasons:
F faces EV transition challenges and legacy costs [Motley Fool].
GM's EV lineup rollout has faced delays [Reuters].
RIVN struggles with production scaling and cash burn [Bloomberg].""",

    "energy": """Recommendation: XOM

Explanation:
ExxonMobil offers the best energy sector value with strong cash flows and strategic acquisitions [Motley Fool].

Key Points:
- Cash generation: Record free cash flow supports dividends and buybacks [Reuters].
- Pioneer acquisition: The merger expands Permian Basin presence significantly [Bloomberg].
- Low-carbon investments: Strategic carbon capture and hydrogen projects position for transition [CNBC].
- Cost discipline: Structural cost reductions have improved margins [Barron's].

The other companies were not chosen for specific reasons:
CVX faces integration challenges from Hess acquisition [Motley Fool].
BP struggles with strategic direction uncertainty [Reuters].
SHEL European regulatory pressures impact growth plans [Bloomberg].""",
}

# Default mock recommendation for unknown industries
DEFAULT_MOCK_RECOMMENDATION = """Recommendation: SPY

Explanation:
For this industry, a diversified S&P 500 ETF provides the best risk-adjusted exposure to market growth [Motley Fool].

Key Points:
- Diversification: Broad market exposure reduces individual stock risk [Reuters].
- Low cost: Minimal expense ratios maximize returns [Bloomberg].
- Liquidity: High trading volume ensures easy entry and exit [CNBC].
- Track record: Consistent long-term performance beats most active managers [Barron's].

Consider researching specific companies in this industry for more targeted recommendations."""

# Mock chat responses
MOCK_CHAT_RESPONSES = [
    "Based on the recommendation analysis, {ticker} shows strong fundamentals with positive momentum in recent quarters. The company's market position and growth trajectory make it an attractive investment option.",
    "The investment thesis for {ticker} is supported by several factors: strong revenue growth, expanding margins, and favorable industry tailwinds. However, investors should always consider their own risk tolerance and investment horizon.",
    "Looking at the technical indicators and fundamental data for {ticker}, the stock appears fairly valued at current levels. Key catalysts to watch include upcoming earnings reports and any strategic announcements.",
    "The recommended stock {ticker} has shown resilience in various market conditions. Its competitive advantages and management execution provide confidence in long-term value creation.",
    "For {ticker}, the risk-reward profile is favorable based on current valuations. The company's strong balance sheet and cash flow generation support both growth investments and shareholder returns.",
]

# Mock news references
MOCK_REFERENCES = {
    "Motley Fool": {"title": "Industry Analysis Report", "url": "https://www.fool.com/investing/"},
    "Reuters": {"title": "Market Update", "url": "https://www.reuters.com/markets/"},
    "Bloomberg": {"title": "Financial News", "url": "https://www.bloomberg.com/markets"},
    "CNBC": {"title": "Business News", "url": "https://www.cnbc.com/"},
    "Barron's": {"title": "Investment Analysis", "url": "https://www.barrons.com/"},
    "Seeking Alpha": {"title": "Stock Analysis", "url": "https://seekingalpha.com/"},
    "The Verge": {"title": "Tech News", "url": "https://www.theverge.com/"},
    "Electrek": {"title": "EV News", "url": "https://electrek.co/"},
}

MOCK_NUMBERED_REFS = {
    1: {"title": "Industry Analysis Report", "url": "https://www.fool.com/investing/", "source_name": "Motley Fool"},
    2: {"title": "Market Update", "url": "https://www.reuters.com/markets/", "source_name": "Reuters"},
    3: {"title": "Financial News", "url": "https://www.bloomberg.com/markets", "source_name": "Bloomberg"},
    4: {"title": "Business News", "url": "https://www.cnbc.com/", "source_name": "CNBC"},
}


def get_mock_recommendation(industry: str) -> tuple[str, dict, dict]:
    """
    Get a mock recommendation for the given industry.

    Args:
        industry: The industry name (case-insensitive)

    Returns:
        Tuple of (recommendation_text, references_dict, numbered_refs_dict)
    """
    industry_lower = industry.lower()
    recommendation = MOCK_RECOMMENDATIONS.get(industry_lower, DEFAULT_MOCK_RECOMMENDATION)
    return recommendation, MOCK_REFERENCES.copy(), MOCK_NUMBERED_REFS.copy()


def get_mock_chat_response(prompt: str, recommendation: str) -> str:
    """
    Get a mock chat response based on the prompt and recommendation.

    Args:
        prompt: The user's question
        recommendation: The current recommendation context

    Returns:
        A mock response string
    """
    import re
    import random

    # Extract ticker from recommendation
    ticker_match = re.search(r"Recommendation:\s*([A-Z.\-]{1,10})", recommendation)
    ticker = ticker_match.group(1) if ticker_match else "the stock"

    # Select a random response template
    response_template = random.choice(MOCK_CHAT_RESPONSES)
    return response_template.format(ticker=ticker)


def is_mock_mode_enabled() -> bool:
    """Check if mock mode is enabled via environment variable."""
    import os
    return os.environ.get("MOCK_LLM", "").lower() in ("1", "true", "yes")


def get_mock_industry_tickers(industry: str) -> str:
    """
    Get mock tickers for the given industry.

    Args:
        industry: The industry name (case-insensitive)

    Returns:
        Comma-separated string of ticker symbols
    """
    industry_lower = industry.lower()
    return MOCK_INDUSTRY_TICKERS.get(industry_lower, "SPY, QQQ, DIA")


def get_mock_news_summaries(tickers: str) -> str:
    """
    Get mock news summaries for the given tickers.

    Args:
        tickers: Comma-separated string of ticker symbols

    Returns:
        Formatted news summaries string
    """
    # Determine industry from tickers
    ticker_list = [t.strip().upper() for t in tickers.split(",")]

    # Map tickers to industries
    ticker_to_industry = {
        "NVDA": "technology", "AAPL": "technology", "MSFT": "technology",
        "LLY": "healthcare", "JNJ": "healthcare", "PFE": "healthcare",
        "JPM": "finance", "BAC": "finance", "GS": "finance",
        "TSLA": "automotive", "F": "automotive", "GM": "automotive",
        "XOM": "energy", "CVX": "energy", "BP": "energy",
    }

    # Find matching industry
    for ticker in ticker_list:
        if ticker in ticker_to_industry:
            industry = ticker_to_industry[ticker]
            if industry in MOCK_NEWS_SUMMARIES:
                return MOCK_NEWS_SUMMARIES[industry]

    return DEFAULT_MOCK_NEWS
