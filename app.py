from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from market_scraper import get_bse_market_overview  # Import the market scraper function
import yfinance as yf

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined stock symbols for Yahoo Finance
STOCK_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "SBIN.NS", "BHARTIARTL.NS", "HDFC.NS", "ITC.NS"
]

def fetch_stock_data_yahoo(symbol: str):
    """Fetch stock data for a single symbol using Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract relevant stock data
        return {
            "symbol": info.get("symbol", symbol),
            "price": info.get("regularMarketPrice", 0.0),
            "volume": info.get("volume", 0),
            "market_cap": info.get("marketCap", 0),
            "name": info.get("shortName", "Unknown")
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

@app.get("/market-overview")
def market_overview():
    """Fetch market overview details."""
    try:
        # Get BSE market data
        bse_data = get_bse_market_overview()

        # Fetch top 10 companies data from Yahoo Finance
        stock_data = []
        for symbol in STOCK_SYMBOLS:
            stock = fetch_stock_data_yahoo(symbol)
            if stock:
                stock_data.append(stock)

        # Sort stocks by market cap
        sorted_stocks = sorted(stock_data, key=lambda x: x["market_cap"], reverse=True)

        # Extract the top 10 companies
        top_10_companies = sorted_stocks[:10]

        return {
            "as_on_date": bse_data["as_on_date"],
            "total_companies": bse_data["total_companies"],
            "total_market_cap": bse_data["total_market_cap"],
            "top_10_market_cap": bse_data["top_10_market_cap"],
            "top_10_companies": top_10_companies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market overview: {e}")

@app.get("/stock/{symbol}")
def stock_details(symbol: str):
    """Fetch individual stock details using Yahoo Finance."""
    stock = fetch_stock_data_yahoo(symbol)
    if stock:
        return stock
    else:
        raise HTTPException(status_code=404, detail=f"Data for {symbol} not found.")
