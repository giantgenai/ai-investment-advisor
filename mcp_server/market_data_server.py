"""MCP server exposing a market-data lookup tool.

Run with stdio transport (the standard way MCP clients launch local servers):

    python -m mcp_server.market_data_server

Or register it with an MCP-aware client (Claude Desktop, Claude Code, etc.)
by pointing the client at this script as the command.

Tools exposed:
    - get_market_data(ticker): quote-style snapshot (price, day range, market cap, P/E, ...)
    - get_price_history(ticker, period): recent OHLCV bars as a list of records
    - list_supported_tickers(): tickers backed by curated mock data

Data is sourced from the in-repo mock dataset (app.mock_responses) so the
server runs fully offline, matching the rest of this project.
"""

from __future__ import annotations

import os
import sys
from typing import Any

# Make `app/` importable when run as a script from the repo root.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from mcp.server.fastmcp import FastMCP  # type: ignore

from app.mock_responses import (
    MOCK_STOCK_INFO,
    get_mock_stock_history,
    get_mock_stock_info,
)

mcp = FastMCP("ai-investment-market-data")


@mcp.tool()
def get_market_data(ticker: str) -> dict[str, Any]:
    """Return a market-data snapshot for the given ticker.

    Includes current price, day range, 52-week range, volume, market cap,
    valuation multiples, and analyst target. Backed by the project's offline
    mock dataset; unknown tickers return the default profile.
    """
    info = get_mock_stock_info(ticker)
    fields = (
        "shortName", "exchange", "currentPrice", "previousClose", "open",
        "dayLow", "dayHigh", "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
        "volume", "averageVolume", "marketCap", "beta", "trailingPE",
        "trailingEps", "dividendYield", "targetMeanPrice",
    )
    snapshot = {k: info.get(k) for k in fields if k in info}
    snapshot["ticker"] = ticker.upper()
    return snapshot


@mcp.tool()
def get_price_history(ticker: str, period: str = "1mo") -> dict[str, Any]:
    """Return OHLCV bars for `ticker` over `period`.

    `period` accepts: 1d, 5d, 1mo, 3mo, 6mo, ytd, 1y, 5y, max.
    Returns a dict with `ticker`, `period`, and a `bars` list of
    {date, open, high, low, close, volume} records (most recent last).
    """
    df = get_mock_stock_history(ticker.upper(), period=period)
    bars = [
        {
            "date": idx.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]),
        }
        for idx, row in df.iterrows()
    ]
    return {"ticker": ticker.upper(), "period": period, "bars": bars}


@mcp.tool()
def list_supported_tickers() -> list[str]:
    """List tickers with curated mock data. Other tickers still resolve via the default profile."""
    return sorted(MOCK_STOCK_INFO.keys())


if __name__ == "__main__":
    mcp.run()
