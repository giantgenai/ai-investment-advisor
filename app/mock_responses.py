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

# Industry aliases for fuzzy matching
# Maps various user inputs to canonical industry names
INDUSTRY_ALIASES = {
    # Technology
    "technology": "technology",
    "tech": "technology",
    "software": "technology",
    "it": "technology",
    "computer": "technology",
    "computers": "technology",
    "internet": "technology",
    "cloud": "technology",
    # Healthcare
    "healthcare": "healthcare",
    "health": "healthcare",
    "medical": "healthcare",
    "hospital": "healthcare",
    "hospitals": "healthcare",
    # Finance
    "finance": "finance",
    "financial": "finance",
    "fintech": "finance",
    # Automotive
    "automotive": "automotive",
    "auto": "automotive",
    "automobile": "automotive",
    "automobiles": "automotive",
    "car": "automotive",
    "cars": "automotive",
    "vehicle": "automotive",
    "vehicles": "automotive",
    "ev": "automotive",
    "electric vehicle": "automotive",
    "electric vehicles": "automotive",
    # Energy
    "energy": "energy",
    "oil": "energy",
    "gas": "energy",
    "oil and gas": "energy",
    "petroleum": "energy",
    "fossil fuel": "energy",
    "fossil fuels": "energy",
    # Retail
    "retail": "retail",
    "retailer": "retail",
    "retailers": "retail",
    "shopping": "retail",
    "ecommerce": "retail",
    "e-commerce": "retail",
    "consumer": "retail",
    # Airlines
    "airlines": "airlines",
    "airline": "airlines",
    "aviation": "airlines",
    "air travel": "airlines",
    "travel": "airlines",
    # Entertainment
    "entertainment": "entertainment",
    "media": "entertainment",
    "streaming": "entertainment",
    "movie": "entertainment",
    "movies": "entertainment",
    "film": "entertainment",
    "tv": "entertainment",
    "television": "entertainment",
    # Pharmaceuticals
    "pharmaceuticals": "pharmaceuticals",
    "pharmaceutical": "pharmaceuticals",
    "pharma": "pharmaceuticals",
    "drug": "pharmaceuticals",
    "drugs": "pharmaceuticals",
    "biotech": "pharmaceuticals",
    "biotechnology": "pharmaceuticals",
    # Banking
    "banking": "banking",
    "bank": "banking",
    "banks": "banking",
    # Semiconductors
    "semiconductors": "semiconductors",
    "semiconductor": "semiconductors",
    "chips": "semiconductors",
    "chip": "semiconductors",
    "chipmaker": "semiconductors",
    "chipmakers": "semiconductors",
    # Real Estate
    "real estate": "real estate",
    "realestate": "real estate",
    "property": "real estate",
    "properties": "real estate",
    "reit": "real estate",
    "reits": "real estate",
    # Telecommunications
    "telecommunications": "telecommunications",
    "telecom": "telecommunications",
    "telco": "telecommunications",
    "wireless": "telecommunications",
    "mobile": "telecommunications",
    # Food & Beverage
    "food": "food",
    "food and beverage": "food",
    "food & beverage": "food",
    "beverage": "food",
    "beverages": "food",
    "restaurant": "food",
    "restaurants": "food",
    # Defense
    "defense": "defense",
    "defence": "defense",
    "aerospace": "defense",
    "military": "defense",
    "weapons": "defense",
    # Insurance
    "insurance": "insurance",
    "insurer": "insurance",
    "insurers": "insurance",
}

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
    "telecommunications": "VZ, T, TMUS",
    "food": "MCD, SBUX, KO",
    "defense": "LMT, RTX, NOC",
    "insurance": "BRK.B, PGR, MET",
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

    "retail": """News for WMT:
- Walmart E-commerce Growth Accelerates (Published: 2024-01-15 09:00:00)
  Summary: Online sales surge 23% as Walmart+ membership and grocery delivery expand nationwide.
  Source: https://www.reuters.com/business/walmart-ecommerce/
- Walmart Raises Full-Year Guidance (Published: 2024-01-14 08:00:00)
  Summary: Strong holiday sales and market share gains prompt upward revision to earnings outlook.
  Source: https://www.fool.com/investing/walmart-guidance/
- Walmart Automation Investments Pay Off (Published: 2024-01-13 10:00:00)
  Summary: Warehouse robotics and AI-powered inventory management improve margins significantly.
  Source: https://www.bloomberg.com/news/walmart-automation/

News for TGT:
- Target Same-Store Sales Decline (Published: 2024-01-12 09:00:00)
  Summary: Discretionary spending weakness impacts comparable sales despite grocery strength.
  Source: https://www.cnbc.com/target-sales/
- Target Inventory Levels Normalize (Published: 2024-01-11 11:00:00)
  Summary: After markdown pressure, inventory management improvements restore healthy stock levels.
  Source: https://www.reuters.com/business/target-inventory/
- Target Expands Same-Day Delivery (Published: 2024-01-10 14:00:00)
  Summary: Shipt integration and drive-up services continue to gain customer adoption.
  Source: https://www.fool.com/investing/target-delivery/

News for COST:
- Costco Membership Revenue Hits Record (Published: 2024-01-14 10:00:00)
  Summary: Membership renewals exceed 93% as Costco considers first fee increase since 2017.
  Source: https://www.bloomberg.com/news/costco-membership/
- Costco International Expansion Continues (Published: 2024-01-13 08:00:00)
  Summary: New warehouse openings in China and Europe drive global growth strategy.
  Source: https://www.reuters.com/business/costco-expansion/
- Costco Gold Bar Sales Surge (Published: 2024-01-12 12:00:00)
  Summary: Precious metals and luxury items drive traffic as consumers seek value.
  Source: https://www.cnbc.com/costco-gold/
""",

    "airlines": """News for DAL:
- Delta Reports Record Revenue Quarter (Published: 2024-01-15 07:00:00)
  Summary: Strong travel demand drives record quarterly revenue with premium cabin outperformance.
  Source: https://www.reuters.com/business/delta-earnings/
- Delta Expands International Routes (Published: 2024-01-14 09:00:00)
  Summary: New transatlantic and Asia-Pacific routes launch as international travel recovers.
  Source: https://www.fool.com/investing/delta-international/
- Delta Technology Investments Improve Operations (Published: 2024-01-13 11:00:00)
  Summary: AI-powered scheduling and maintenance systems reduce cancellations and delays.
  Source: https://www.bloomberg.com/news/delta-technology/

News for UAL:
- United Airlines Fleet Modernization Progresses (Published: 2024-01-12 08:00:00)
  Summary: Boeing and Airbus deliveries continue despite supply chain challenges.
  Source: https://www.cnbc.com/united-fleet/
- United Frequent Flyer Program Enhances Benefits (Published: 2024-01-11 10:00:00)
  Summary: MileagePlus improvements drive customer loyalty and ancillary revenue.
  Source: https://www.reuters.com/business/united-mileageplus/
- United Sustainable Aviation Fuel Partnership Expands (Published: 2024-01-10 13:00:00)
  Summary: Investments in SAF production position United as sustainability leader.
  Source: https://www.bloomberg.com/news/united-saf/

News for AAL:
- American Airlines Debt Reduction Continues (Published: 2024-01-14 09:00:00)
  Summary: Aggressive deleveraging improves balance sheet strength post-pandemic.
  Source: https://www.fool.com/investing/american-debt/
- American Airlines Labor Agreements Finalized (Published: 2024-01-13 10:00:00)
  Summary: Pilot and flight attendant contracts provide labor stability for coming years.
  Source: https://www.reuters.com/business/american-labor/
- American Airlines Cargo Revenue Declines (Published: 2024-01-12 11:00:00)
  Summary: Air freight normalization impacts cargo segment after pandemic boom.
  Source: https://www.cnbc.com/american-cargo/
""",

    "telecommunications": """News for VZ:
- Verizon 5G Network Expansion Accelerates (Published: 2024-01-15 08:00:00)
  Summary: C-band spectrum deployment reaches 200 million people, improving competitive position.
  Source: https://www.reuters.com/technology/verizon-5g/
- Verizon Dividend Yield Attracts Income Investors (Published: 2024-01-14 10:00:00)
  Summary: 37-year dividend growth streak continues with stable 6.5% yield.
  Source: https://www.fool.com/investing/verizon-dividend/
- Verizon Business Segment Shows Strength (Published: 2024-01-13 11:00:00)
  Summary: Enterprise and government contracts drive B2B revenue growth.
  Source: https://www.bloomberg.com/news/verizon-business/

News for T:
- AT&T Fiber Subscriber Growth Continues (Published: 2024-01-12 09:00:00)
  Summary: Fiber additions exceed expectations as broadband competition intensifies.
  Source: https://www.cnbc.com/att-fiber/
- AT&T Free Cash Flow Improves (Published: 2024-01-11 08:00:00)
  Summary: Cost reductions and subscriber growth boost free cash flow generation.
  Source: https://www.reuters.com/business/att-cashflow/
- AT&T HBO Max Integration Benefits Emerge (Published: 2024-01-10 14:00:00)
  Summary: Warner Bros Discovery partnership provides content advantages for retention.
  Source: https://www.bloomberg.com/news/att-hbomax/

News for TMUS:
- T-Mobile Subscriber Gains Lead Industry (Published: 2024-01-14 07:00:00)
  Summary: Postpaid phone additions outpace Verizon and AT&T combined.
  Source: https://www.fool.com/investing/tmobile-subscribers/
- T-Mobile 5G Home Internet Expands (Published: 2024-01-13 09:00:00)
  Summary: Fixed wireless offering takes market share from cable providers.
  Source: https://www.reuters.com/technology/tmobile-home/
- T-Mobile Sprint Integration Complete (Published: 2024-01-12 10:00:00)
  Summary: Synergy targets exceeded as network consolidation finalizes.
  Source: https://www.cnbc.com/tmobile-sprint/
""",

    "food": """News for MCD:
- McDonald's Global Comparable Sales Grow (Published: 2024-01-15 08:00:00)
  Summary: International markets and digital ordering drive same-store sales increases.
  Source: https://www.reuters.com/business/mcdonalds-sales/
- McDonald's Loyalty Program Reaches 150 Million Members (Published: 2024-01-14 10:00:00)
  Summary: MyMcDonald's Rewards drives repeat visits and average ticket increases.
  Source: https://www.fool.com/investing/mcdonalds-loyalty/
- McDonald's Menu Innovation Continues (Published: 2024-01-13 11:00:00)
  Summary: New product launches and limited-time offers maintain customer interest.
  Source: https://www.bloomberg.com/news/mcdonalds-menu/

News for SBUX:
- Starbucks China Recovery Progresses (Published: 2024-01-12 09:00:00)
  Summary: Chinese market rebounds with store expansion resuming after COVID disruptions.
  Source: https://www.cnbc.com/starbucks-china/
- Starbucks Rewards Program Drives Traffic (Published: 2024-01-11 08:00:00)
  Summary: Mobile ordering and personalization increase customer frequency.
  Source: https://www.reuters.com/business/starbucks-rewards/
- Starbucks Labor Relations Stabilize (Published: 2024-01-10 14:00:00)
  Summary: Union negotiations progress as company increases barista wages.
  Source: https://www.bloomberg.com/news/starbucks-labor/

News for KO:
- Coca-Cola Price Increases Stick (Published: 2024-01-14 07:00:00)
  Summary: Volume growth resumes despite higher prices, demonstrating brand strength.
  Source: https://www.fool.com/investing/coca-cola-pricing/
- Coca-Cola Zero Sugar Growth Accelerates (Published: 2024-01-13 09:00:00)
  Summary: Sugar-free variants drive growth as health-conscious consumers shift preferences.
  Source: https://www.reuters.com/business/coca-cola-zero/
- Coca-Cola Emerging Markets Expansion (Published: 2024-01-12 10:00:00)
  Summary: Africa and Southeast Asia investments drive long-term growth strategy.
  Source: https://www.cnbc.com/coca-cola-emerging/
""",

    "defense": """News for LMT:
- Lockheed Martin F-35 Deliveries Increase (Published: 2024-01-15 08:00:00)
  Summary: Fighter jet production ramps up as international orders accelerate.
  Source: https://www.reuters.com/business/lockheed-f35/
- Lockheed Hypersonic Weapons Contract Awarded (Published: 2024-01-14 10:00:00)
  Summary: $2.5 billion Pentagon contract advances next-generation missile development.
  Source: https://www.fool.com/investing/lockheed-hypersonic/
- Lockheed Space Division Wins NASA Contract (Published: 2024-01-13 11:00:00)
  Summary: Artemis program participation drives space segment growth.
  Source: https://www.bloomberg.com/news/lockheed-nasa/

News for RTX:
- RTX Engine Inspections Progress (Published: 2024-01-12 09:00:00)
  Summary: Pratt & Whitney powder metal issue remediation ahead of schedule.
  Source: https://www.cnbc.com/rtx-engines/
- Raytheon Missile Systems Backlog Grows (Published: 2024-01-11 08:00:00)
  Summary: Ukraine conflict and allied rearmament drive record order book.
  Source: https://www.reuters.com/business/raytheon-backlog/
- Collins Aerospace Aftermarket Strong (Published: 2024-01-10 14:00:00)
  Summary: Commercial aviation recovery boosts high-margin service revenues.
  Source: https://www.bloomberg.com/news/collins-aftermarket/

News for NOC:
- Northrop Grumman B-21 Production Begins (Published: 2024-01-14 07:00:00)
  Summary: Stealth bomber enters production phase with strong Air Force support.
  Source: https://www.fool.com/investing/northrop-b21/
- Northrop Space Systems Revenue Grows (Published: 2024-01-13 09:00:00)
  Summary: Satellite and launch vehicle programs drive segment expansion.
  Source: https://www.reuters.com/business/northrop-space/
- Northrop Cybersecurity Contracts Expand (Published: 2024-01-12 10:00:00)
  Summary: Government cyber defense spending increases drive technology segment.
  Source: https://www.cnbc.com/northrop-cyber/
""",

    "insurance": """News for BRK.B:
- Berkshire Insurance Float Reaches Record (Published: 2024-01-15 08:00:00)
  Summary: GEICO and reinsurance operations generate $168 billion investment float.
  Source: https://www.reuters.com/business/berkshire-float/
- Berkshire Cash Pile Exceeds $150 Billion (Published: 2024-01-14 10:00:00)
  Summary: Warren Buffett maintains dry powder amid elevated market valuations.
  Source: https://www.fool.com/investing/berkshire-cash/
- Berkshire Energy Investments Expand (Published: 2024-01-13 11:00:00)
  Summary: Renewable energy and utility acquisitions drive long-term growth.
  Source: https://www.bloomberg.com/news/berkshire-energy/

News for PGR:
- Progressive Market Share Gains Continue (Published: 2024-01-12 09:00:00)
  Summary: Direct-to-consumer model and Snapshot telematics drive growth.
  Source: https://www.cnbc.com/progressive-share/
- Progressive Combined Ratio Improves (Published: 2024-01-11 08:00:00)
  Summary: Underwriting discipline and rate increases boost profitability.
  Source: https://www.reuters.com/business/progressive-ratio/
- Progressive Commercial Auto Expands (Published: 2024-01-10 14:00:00)
  Summary: Small business insurance segment shows strong growth momentum.
  Source: https://www.bloomberg.com/news/progressive-commercial/

News for MET:
- MetLife Group Benefits Growth Accelerates (Published: 2024-01-14 07:00:00)
  Summary: Employee benefits segment benefits from tight labor market.
  Source: https://www.fool.com/investing/metlife-benefits/
- MetLife International Operations Strong (Published: 2024-01-13 09:00:00)
  Summary: Latin America and Asia divisions drive diversified revenue growth.
  Source: https://www.reuters.com/business/metlife-international/
- MetLife Investment Returns Improve (Published: 2024-01-12 10:00:00)
  Summary: Higher interest rates boost investment portfolio performance.
  Source: https://www.cnbc.com/metlife-investments/
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

    "retail": """Recommendation: WMT

Explanation:
Walmart leads the retail sector with omnichannel dominance and strong execution across all formats [Motley Fool].

Key Points:
- E-commerce growth: Online sales growing 23%+ with Walmart+ gaining traction [Reuters].
- Market share gains: Grocery leadership and value positioning attract customers across income levels [Bloomberg].
- Automation investments: Warehouse robotics and AI improving margins significantly [CNBC].
- International strength: Flipkart and Walmex operations driving global growth [Barron's].

The other companies were not chosen for specific reasons:
TGT faces discretionary spending headwinds and margin pressure [Motley Fool].
COST trades at premium valuation despite strong execution [Reuters].
AMZN retail segment profitability remains challenged [Bloomberg].""",

    "airlines": """Recommendation: DAL

Explanation:
Delta Air Lines stands out as the premium airline investment with superior operational performance and customer loyalty [Motley Fool].

Key Points:
- Premium revenue: Business and first-class travelers drive industry-leading unit revenue [Reuters].
- Operational excellence: Lowest cancellation rate and highest on-time performance among majors [Bloomberg].
- Brand partnerships: American Express deal and SkyMiles program generate substantial revenue [CNBC].
- Fleet efficiency: Modern aircraft fleet reduces fuel costs and maintenance expenses [Barron's].

The other companies were not chosen for specific reasons:
UAL faces higher debt levels and fleet transition costs [Motley Fool].
AAL continues to deleverage with more work needed on balance sheet [Reuters].
LUV struggles with operational challenges and Boeing delivery delays [Bloomberg].""",

    "telecommunications": """Recommendation: TMUS

Explanation:
T-Mobile emerges as the top telecom investment with subscriber momentum and network leadership [Motley Fool].

Key Points:
- Subscriber growth: Industry-leading postpaid additions outpacing competitors combined [Reuters].
- 5G leadership: Largest and fastest 5G network drives competitive advantage [Bloomberg].
- Fixed wireless: Home internet offering disrupting cable with rapid adoption [CNBC].
- Synergy realization: Sprint integration complete with targets exceeded [Barron's].

The other companies were not chosen for specific reasons:
VZ faces subscriber losses and heavy debt load from spectrum purchases [Motley Fool].
T struggles with wireless competition despite fiber strength [Reuters].
CHTR cable business faces wireless and fiber competition [Bloomberg].""",

    "food": """Recommendation: MCD

Explanation:
McDonald's represents the premier food service investment with global scale and digital transformation [Motley Fool].

Key Points:
- Global reach: 40,000+ restaurants provide unmatched scale and brand recognition [Reuters].
- Digital leadership: Loyalty program with 150M+ members drives repeat visits [Bloomberg].
- Franchise model: 95% franchised generates stable, high-margin royalty income [CNBC].
- Value positioning: Affordable menu attracts customers in all economic conditions [Barron's].

The other companies were not chosen for specific reasons:
SBUX faces China uncertainty and labor cost pressures [Motley Fool].
KO growth limited by developed market saturation [Reuters].
CMG trades at premium valuation with limited international presence [Bloomberg].""",

    "defense": """Recommendation: LMT

Explanation:
Lockheed Martin leads the defense sector with dominant programs and strong government relationships [Motley Fool].

Key Points:
- F-35 dominance: Fighter jet program provides decades of production and service revenue [Reuters].
- Backlog strength: $156 billion order backlog provides exceptional visibility [Bloomberg].
- Space growth: NASA contracts and classified programs drive expansion [CNBC].
- Shareholder returns: Consistent dividend growth and buyback programs [Barron's].

The other companies were not chosen for specific reasons:
RTX faces engine inspection costs and integration challenges [Motley Fool].
NOC concentrated in fewer but larger programs with execution risk [Reuters].
GD commercial aerospace exposure adds volatility [Bloomberg].""",

    "insurance": """Recommendation: BRK.B

Explanation:
Berkshire Hathaway offers unique insurance exposure combined with diversified business ownership [Motley Fool].

Key Points:
- Float advantage: $168 billion insurance float provides investment capital at negative cost [Reuters].
- Diversification: Railroad, energy, and manufacturing businesses reduce risk [Bloomberg].
- Capital allocation: Warren Buffett's track record of value creation unmatched [CNBC].
- Balance sheet: $150B+ cash provides optionality for acquisitions or buybacks [Barron's].

The other companies were not chosen for specific reasons:
PGR trades at premium multiple despite strong execution [Motley Fool].
MET faces life insurance headwinds and rate sensitivity [Reuters].
ALL auto insurance competition pressures margins [Bloomberg].""",
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


def _normalize_industry(industry: str) -> str:
    """
    Normalize an industry name using aliases for fuzzy matching.

    Args:
        industry: The user-provided industry name

    Returns:
        Canonical industry name or the original if no match found
    """
    industry_lower = industry.lower().strip()

    # Direct match in aliases
    if industry_lower in INDUSTRY_ALIASES:
        return INDUSTRY_ALIASES[industry_lower]

    # Partial match - check if any alias is contained in the input
    for alias, canonical in INDUSTRY_ALIASES.items():
        if alias in industry_lower or industry_lower in alias:
            return canonical

    return industry_lower


def get_mock_recommendation(industry: str) -> tuple[str, dict, dict]:
    """
    Get a mock recommendation for the given industry.

    Args:
        industry: The industry name (case-insensitive, supports aliases)

    Returns:
        Tuple of (recommendation_text, references_dict, numbered_refs_dict)
    """
    canonical_industry = _normalize_industry(industry)
    recommendation = MOCK_RECOMMENDATIONS.get(canonical_industry, DEFAULT_MOCK_RECOMMENDATION)
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
        industry: The industry name (case-insensitive, supports aliases)

    Returns:
        Comma-separated string of ticker symbols
    """
    canonical_industry = _normalize_industry(industry)
    return MOCK_INDUSTRY_TICKERS.get(canonical_industry, "SPY, QQQ, DIA")


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
        # Technology
        "NVDA": "technology", "AAPL": "technology", "MSFT": "technology",
        # Healthcare
        "LLY": "healthcare", "JNJ": "healthcare", "PFE": "healthcare",
        # Finance
        "JPM": "finance", "BAC": "finance", "GS": "finance",
        # Automotive
        "TSLA": "automotive", "F": "automotive", "GM": "automotive",
        # Energy
        "XOM": "energy", "CVX": "energy", "BP": "energy",
        # Retail
        "WMT": "retail", "TGT": "retail", "COST": "retail",
        # Airlines
        "DAL": "airlines", "UAL": "airlines", "AAL": "airlines",
        # Telecommunications
        "VZ": "telecommunications", "T": "telecommunications", "TMUS": "telecommunications",
        # Food
        "MCD": "food", "SBUX": "food", "KO": "food",
        # Defense
        "LMT": "defense", "RTX": "defense", "NOC": "defense",
        # Insurance
        "BRK.B": "insurance", "PGR": "insurance", "MET": "insurance",
        # Semiconductors
        "AMD": "semiconductors", "INTC": "semiconductors",
        # Banking
        "WFC": "banking",
        # Pharmaceuticals
        "MRK": "pharmaceuticals",
        # Entertainment
        "DIS": "entertainment", "NFLX": "entertainment", "WBD": "entertainment",
        # Real Estate
        "PLD": "real estate", "AMT": "real estate", "SPG": "real estate",
    }

    # Find matching industry
    for ticker in ticker_list:
        if ticker in ticker_to_industry:
            industry = ticker_to_industry[ticker]
            if industry in MOCK_NEWS_SUMMARIES:
                return MOCK_NEWS_SUMMARIES[industry]

    return DEFAULT_MOCK_NEWS


# =============================================================================
# MOCK STOCK DATA - For fully offline testing without Yahoo Finance
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock stock info data
MOCK_STOCK_INFO = {
    "NVDA": {
        "shortName": "NVIDIA Corporation",
        "longName": "NVIDIA Corporation",
        "exchange": "NASDAQ",
        "currentPrice": 875.50,
        "regularMarketPrice": 875.50,
        "previousClose": 868.20,
        "open": 870.00,
        "dayLow": 865.30,
        "dayHigh": 882.15,
        "fiftyTwoWeekLow": 222.97,
        "fiftyTwoWeekHigh": 974.00,
        "volume": 42150000,
        "averageVolume": 45230000,
        "marketCap": 2160000000000,
        "beta": 1.72,
        "trailingPE": 68.5,
        "trailingEps": 12.78,
        "dividendRate": 0.16,
        "dividendYield": 0.0002,
        "exDividendDate": 1709164800,
        "targetMeanPrice": 950.00,
    },
    "AAPL": {
        "shortName": "Apple Inc.",
        "longName": "Apple Inc.",
        "exchange": "NASDAQ",
        "currentPrice": 185.92,
        "regularMarketPrice": 185.92,
        "previousClose": 184.25,
        "open": 184.50,
        "dayLow": 183.80,
        "dayHigh": 186.75,
        "fiftyTwoWeekLow": 164.08,
        "fiftyTwoWeekHigh": 199.62,
        "volume": 58230000,
        "averageVolume": 62450000,
        "marketCap": 2870000000000,
        "beta": 1.28,
        "trailingPE": 29.2,
        "trailingEps": 6.37,
        "dividendRate": 0.96,
        "dividendYield": 0.0052,
        "exDividendDate": 1707523200,
        "targetMeanPrice": 195.00,
    },
    "MSFT": {
        "shortName": "Microsoft Corporation",
        "longName": "Microsoft Corporation",
        "exchange": "NASDAQ",
        "currentPrice": 415.80,
        "regularMarketPrice": 415.80,
        "previousClose": 412.50,
        "open": 413.00,
        "dayLow": 410.25,
        "dayHigh": 418.90,
        "fiftyTwoWeekLow": 309.45,
        "fiftyTwoWeekHigh": 430.82,
        "volume": 21560000,
        "averageVolume": 23890000,
        "marketCap": 3090000000000,
        "beta": 0.91,
        "trailingPE": 36.8,
        "trailingEps": 11.30,
        "dividendRate": 3.00,
        "dividendYield": 0.0072,
        "exDividendDate": 1708041600,
        "targetMeanPrice": 450.00,
    },
    "TSLA": {
        "shortName": "Tesla, Inc.",
        "longName": "Tesla, Inc.",
        "exchange": "NASDAQ",
        "currentPrice": 248.50,
        "regularMarketPrice": 248.50,
        "previousClose": 245.80,
        "open": 246.00,
        "dayLow": 242.15,
        "dayHigh": 252.30,
        "fiftyTwoWeekLow": 152.37,
        "fiftyTwoWeekHigh": 299.29,
        "volume": 98750000,
        "averageVolume": 105230000,
        "marketCap": 790000000000,
        "beta": 2.31,
        "trailingPE": 72.5,
        "trailingEps": 3.43,
        "dividendRate": None,
        "dividendYield": None,
        "exDividendDate": None,
        "targetMeanPrice": 275.00,
    },
    "F": {
        "shortName": "Ford Motor Company",
        "longName": "Ford Motor Company",
        "exchange": "NYSE",
        "currentPrice": 12.45,
        "regularMarketPrice": 12.45,
        "previousClose": 12.30,
        "open": 12.35,
        "dayLow": 12.20,
        "dayHigh": 12.58,
        "fiftyTwoWeekLow": 9.63,
        "fiftyTwoWeekHigh": 14.85,
        "volume": 45230000,
        "averageVolume": 52180000,
        "marketCap": 49500000000,
        "beta": 1.45,
        "trailingPE": 11.2,
        "trailingEps": 1.11,
        "dividendRate": 0.60,
        "dividendYield": 0.048,
        "exDividendDate": 1706745600,
        "targetMeanPrice": 14.00,
    },
    "GM": {
        "shortName": "General Motors Company",
        "longName": "General Motors Company",
        "exchange": "NYSE",
        "currentPrice": 38.75,
        "regularMarketPrice": 38.75,
        "previousClose": 38.20,
        "open": 38.30,
        "dayLow": 37.85,
        "dayHigh": 39.15,
        "fiftyTwoWeekLow": 26.30,
        "fiftyTwoWeekHigh": 42.95,
        "volume": 12450000,
        "averageVolume": 14560000,
        "marketCap": 53200000000,
        "beta": 1.38,
        "trailingPE": 5.2,
        "trailingEps": 7.45,
        "dividendRate": 0.48,
        "dividendYield": 0.012,
        "exDividendDate": 1709251200,
        "targetMeanPrice": 45.00,
    },
    "LLY": {
        "shortName": "Eli Lilly and Company",
        "longName": "Eli Lilly and Company",
        "exchange": "NYSE",
        "currentPrice": 782.50,
        "regularMarketPrice": 782.50,
        "previousClose": 775.30,
        "open": 778.00,
        "dayLow": 772.80,
        "dayHigh": 789.45,
        "fiftyTwoWeekLow": 516.57,
        "fiftyTwoWeekHigh": 800.00,
        "volume": 3250000,
        "averageVolume": 3890000,
        "marketCap": 743000000000,
        "beta": 0.42,
        "trailingPE": 125.8,
        "trailingEps": 6.22,
        "dividendRate": 5.20,
        "dividendYield": 0.0066,
        "exDividendDate": 1707609600,
        "targetMeanPrice": 850.00,
    },
    "JPM": {
        "shortName": "JPMorgan Chase & Co.",
        "longName": "JPMorgan Chase & Co.",
        "exchange": "NYSE",
        "currentPrice": 198.50,
        "regularMarketPrice": 198.50,
        "previousClose": 196.20,
        "open": 197.00,
        "dayLow": 195.30,
        "dayHigh": 200.15,
        "fiftyTwoWeekLow": 135.19,
        "fiftyTwoWeekHigh": 205.88,
        "volume": 8560000,
        "averageVolume": 9230000,
        "marketCap": 571000000000,
        "beta": 1.12,
        "trailingPE": 11.5,
        "trailingEps": 17.26,
        "dividendRate": 4.60,
        "dividendYield": 0.023,
        "exDividendDate": 1706832000,
        "targetMeanPrice": 210.00,
    },
    "XOM": {
        "shortName": "Exxon Mobil Corporation",
        "longName": "Exxon Mobil Corporation",
        "exchange": "NYSE",
        "currentPrice": 105.80,
        "regularMarketPrice": 105.80,
        "previousClose": 104.50,
        "open": 104.75,
        "dayLow": 103.90,
        "dayHigh": 106.45,
        "fiftyTwoWeekLow": 95.77,
        "fiftyTwoWeekHigh": 120.70,
        "volume": 15680000,
        "averageVolume": 17230000,
        "marketCap": 420000000000,
        "beta": 0.92,
        "trailingPE": 12.8,
        "trailingEps": 8.27,
        "dividendRate": 3.80,
        "dividendYield": 0.036,
        "exDividendDate": 1707696000,
        "targetMeanPrice": 115.00,
    },
    "WMT": {
        "shortName": "Walmart Inc.",
        "longName": "Walmart Inc.",
        "exchange": "NYSE",
        "currentPrice": 168.50,
        "regularMarketPrice": 168.50,
        "previousClose": 166.80,
        "open": 167.20,
        "dayLow": 165.90,
        "dayHigh": 169.75,
        "fiftyTwoWeekLow": 149.08,
        "fiftyTwoWeekHigh": 173.75,
        "volume": 7850000,
        "averageVolume": 8560000,
        "marketCap": 453000000000,
        "beta": 0.52,
        "trailingPE": 28.9,
        "trailingEps": 5.83,
        "dividendRate": 2.49,
        "dividendYield": 0.015,
        "exDividendDate": 1708128000,
        "targetMeanPrice": 180.00,
    },
    "DAL": {
        "shortName": "Delta Air Lines, Inc.",
        "longName": "Delta Air Lines, Inc.",
        "exchange": "NYSE",
        "currentPrice": 42.85,
        "regularMarketPrice": 42.85,
        "previousClose": 42.10,
        "open": 42.25,
        "dayLow": 41.80,
        "dayHigh": 43.45,
        "fiftyTwoWeekLow": 33.47,
        "fiftyTwoWeekHigh": 54.50,
        "volume": 6230000,
        "averageVolume": 7450000,
        "marketCap": 27500000000,
        "beta": 1.35,
        "trailingPE": 6.8,
        "trailingEps": 6.30,
        "dividendRate": 0.40,
        "dividendYield": 0.009,
        "exDividendDate": 1706659200,
        "targetMeanPrice": 52.00,
    },
    "TMUS": {
        "shortName": "T-Mobile US, Inc.",
        "longName": "T-Mobile US, Inc.",
        "exchange": "NASDAQ",
        "currentPrice": 162.30,
        "regularMarketPrice": 162.30,
        "previousClose": 160.80,
        "open": 161.00,
        "dayLow": 159.50,
        "dayHigh": 163.75,
        "fiftyTwoWeekLow": 132.00,
        "fiftyTwoWeekHigh": 172.50,
        "volume": 4560000,
        "averageVolume": 5230000,
        "marketCap": 190000000000,
        "beta": 0.65,
        "trailingPE": 22.5,
        "trailingEps": 7.21,
        "dividendRate": 2.60,
        "dividendYield": 0.016,
        "exDividendDate": 1709078400,
        "targetMeanPrice": 175.00,
    },
    "MCD": {
        "shortName": "McDonald's Corporation",
        "longName": "McDonald's Corporation",
        "exchange": "NYSE",
        "currentPrice": 295.80,
        "regularMarketPrice": 295.80,
        "previousClose": 293.50,
        "open": 294.00,
        "dayLow": 291.75,
        "dayHigh": 298.20,
        "fiftyTwoWeekLow": 245.73,
        "fiftyTwoWeekHigh": 302.39,
        "volume": 3120000,
        "averageVolume": 3560000,
        "marketCap": 213000000000,
        "beta": 0.72,
        "trailingPE": 25.3,
        "trailingEps": 11.69,
        "dividendRate": 6.68,
        "dividendYield": 0.023,
        "exDividendDate": 1708992000,
        "targetMeanPrice": 315.00,
    },
    "LMT": {
        "shortName": "Lockheed Martin Corporation",
        "longName": "Lockheed Martin Corporation",
        "exchange": "NYSE",
        "currentPrice": 458.50,
        "regularMarketPrice": 458.50,
        "previousClose": 455.20,
        "open": 456.00,
        "dayLow": 452.80,
        "dayHigh": 462.15,
        "fiftyTwoWeekLow": 412.00,
        "fiftyTwoWeekHigh": 501.25,
        "volume": 1250000,
        "averageVolume": 1450000,
        "marketCap": 110000000000,
        "beta": 0.45,
        "trailingPE": 16.8,
        "trailingEps": 27.29,
        "dividendRate": 12.60,
        "dividendYield": 0.027,
        "exDividendDate": 1709337600,
        "targetMeanPrice": 510.00,
    },
    "BRK.B": {
        "shortName": "Berkshire Hathaway Inc.",
        "longName": "Berkshire Hathaway Inc. Class B",
        "exchange": "NYSE",
        "currentPrice": 412.50,
        "regularMarketPrice": 412.50,
        "previousClose": 409.80,
        "open": 410.50,
        "dayLow": 408.25,
        "dayHigh": 415.00,
        "fiftyTwoWeekLow": 323.95,
        "fiftyTwoWeekHigh": 425.00,
        "volume": 3450000,
        "averageVolume": 3890000,
        "marketCap": 892000000000,
        "beta": 0.88,
        "trailingPE": 10.2,
        "trailingEps": 40.44,
        "dividendRate": None,
        "dividendYield": None,
        "exDividendDate": None,
        "targetMeanPrice": 440.00,
    },
}

# Default stock info for unknown tickers
DEFAULT_STOCK_INFO = {
    "shortName": "Unknown Company",
    "longName": "Unknown Company",
    "exchange": "N/A",
    "currentPrice": 100.00,
    "regularMarketPrice": 100.00,
    "previousClose": 99.50,
    "open": 99.75,
    "dayLow": 98.50,
    "dayHigh": 101.25,
    "fiftyTwoWeekLow": 75.00,
    "fiftyTwoWeekHigh": 125.00,
    "volume": 1000000,
    "averageVolume": 1200000,
    "marketCap": 10000000000,
    "beta": 1.0,
    "trailingPE": 20.0,
    "trailingEps": 5.00,
    "dividendRate": 1.00,
    "dividendYield": 0.01,
    "exDividendDate": None,
    "targetMeanPrice": 110.00,
}


def _generate_mock_price_history(
    ticker: str,
    days: int = 365,
    end_date: datetime = None
) -> pd.DataFrame:
    """
    Generate realistic-looking mock price history for a ticker.

    Args:
        ticker: Stock ticker symbol
        days: Number of days of history to generate
        end_date: End date for the history (defaults to today)

    Returns:
        DataFrame with Date index and Open, High, Low, Close, Volume columns
    """
    if end_date is None:
        end_date = datetime.now()

    # Get base price from stock info or use default
    info = MOCK_STOCK_INFO.get(ticker, DEFAULT_STOCK_INFO)
    current_price = info.get("currentPrice", 100.0)

    # Generate dates (excluding weekends)
    dates = []
    current_date = end_date
    while len(dates) < days:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current_date)
        current_date -= timedelta(days=1)
    dates = dates[::-1]  # Reverse to chronological order

    # Generate price series with random walk
    np.random.seed(hash(ticker) % (2**32))  # Consistent per ticker

    # Start from a lower price and trend upward to current
    volatility = 0.02  # Daily volatility
    drift = 0.0003  # Slight upward drift

    # Calculate starting price to end at current price
    total_return = np.random.randn(len(dates)) * volatility + drift
    cumulative_return = np.cumsum(total_return)

    # Adjust so final price matches current price
    adjustment = np.log(current_price) - (np.log(current_price * 0.7) + cumulative_return[-1])
    prices = np.exp(np.log(current_price * 0.7) + cumulative_return + adjustment * np.linspace(0, 1, len(dates)))

    # Generate OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        daily_range = close * np.random.uniform(0.01, 0.03)
        open_price = close + np.random.uniform(-daily_range/2, daily_range/2)
        high = max(open_price, close) + np.random.uniform(0, daily_range/2)
        low = min(open_price, close) - np.random.uniform(0, daily_range/2)
        volume = int(info.get("averageVolume", 1000000) * np.random.uniform(0.5, 1.5))

        data.append({
            "Open": open_price,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        })

    df = pd.DataFrame(data, index=pd.DatetimeIndex(dates))
    df.index.name = "Date"
    return df


def get_mock_stock_info(ticker: str) -> dict:
    """
    Get mock stock info for a ticker.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with stock info
    """
    return MOCK_STOCK_INFO.get(ticker.upper(), DEFAULT_STOCK_INFO.copy())


def get_mock_stock_history(
    ticker: str,
    period: str = "1y",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Get mock stock price history.

    Args:
        ticker: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 6mo, ytd, 1y, 5y, max)
        interval: Data interval (ignored in mock, always daily)

    Returns:
        DataFrame with OHLCV data
    """
    # Map period to number of days
    period_days = {
        "1d": 1,
        "5d": 5,
        "1mo": 21,
        "3mo": 63,
        "6mo": 126,
        "ytd": 252,  # Approximate
        "1y": 252,
        "5y": 1260,
        "max": 2520,
    }

    days = period_days.get(period, 252)
    return _generate_mock_price_history(ticker, days)


def get_mock_stock_history_range(
    ticker: str,
    start_date: str,
    end_date: str = None
) -> pd.DataFrame:
    """
    Get mock stock price history for a date range.

    Args:
        ticker: Stock ticker symbol
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (optional, defaults to today)

    Returns:
        DataFrame with OHLCV data
    """
    end = datetime.now() if end_date is None else datetime.strptime(end_date, "%Y-%m-%d")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    days = (end - start).days

    if days <= 0:
        days = 1

    df = _generate_mock_price_history(ticker, days, end)
    return df[df.index >= pd.Timestamp(start)]
