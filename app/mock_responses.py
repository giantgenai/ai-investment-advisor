"""
Mock responses for testing the investment advisor app without OpenAI or Ollama APIs.

Usage:
    Set environment variable MOCK_LLM=1 to enable mock responses.

    Example:
        MOCK_LLM=1 streamlit run investment_app.py
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
