from fastapi import FastAPI, HTTPException
from nsepython import nse_quote

from market_scraper import get_bse_market_overview

app = FastAPI()

@app.get("/")
def root():
    """Root Endpoint"""
    return {"message": "Welcome to the Indian Market API"}

@app.get("/market-overview")
def market_overview():
    """Fetch overall market details from BSE"""
    market_data = get_bse_market_overview()
    if market_data:
        return market_data
    raise HTTPException(status_code=500, detail="Failed to fetch market overview data")

@app.get("/stock/{symbol}")
def stock_details(symbol: str):
    """Fetch stock details by symbol"""
    try:
        stock_data = nse_quote(symbol.upper())

        if "stocks" not in stock_data or len(stock_data["stocks"]) == 0:
            raise HTTPException(status_code=404, detail="Stock data not found")

        # Extract stock details
        stock_info = stock_data["stocks"][0]["metadata"]

        response = {
            "symbol": stock_data["info"]["symbol"],
            "companyName": stock_data["info"]["companyName"],
            "lastPrice": stock_info["lastPrice"],
            "dayHigh": stock_info["highPrice"],
            "dayLow": stock_info["lowPrice"],
            "previousClose": stock_info["prevClose"],
            "totalTradedVolume": stock_info["numberOfContractsTraded"],
        }
        return response

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
