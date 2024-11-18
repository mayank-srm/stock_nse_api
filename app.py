from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from market_scraper import get_bse_market_overview  # Import the scraper
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

# Predefined stock symbols (Yahoo Finance Ticker Format)
STOCK_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS",
    "ICICIBANK.NS", "INFY.NS", "SBIN.NS", "ITC.NS", "HINDUNILVR.NS", "HDFC.NS"
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
        return {
            "symbol": symbol,
            "price": 0.0,
            "volume": 0,
            "market_cap": 0,
            "name": "Unknown"
        }

@app.get("/market-overview")
def market_overview():
    """Fetch market overview details."""
    try:
        # Step 1: Get BSE market data
        bse_data = get_bse_market_overview()

        # Step 2: Fetch stock data for top 10 companies
        stock_data = []
        for symbol in STOCK_SYMBOLS:
            stock = fetch_stock_data_yahoo(symbol)
            stock_data.append(stock)

        # Step 3: Sort and extract the top 10 companies
        sorted_stocks = sorted(stock_data, key=lambda x: x["market_cap"], reverse=True)
        top_10_companies = sorted_stocks[:10]

        # Step 4: Construct the final response
        return {
            "as_on_date": bse_data["as_on_date"],
            "total_companies": int(bse_data["total_companies"]),  # Ensure integer
            "total_market_cap": float(bse_data["total_market_cap"]),  # Ensure float
            "top_10_market_cap": float(bse_data["top_10_market_cap"]),  # Ensure float
            "top_10_companies": top_10_companies  # No change needed for the list
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
