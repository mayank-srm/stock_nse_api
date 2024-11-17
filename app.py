from fastapi import FastAPI, HTTPException
from nsepython import nse_index, nse_market_cap, nse_get_quote

app = FastAPI()

@app.get("/")
def root():
    """Root Endpoint"""
    return {"message": "Welcome to the Indian Market API"}

@app.get("/market-overview")
def market_overview():
    """Fetch overall market details"""
    try:
        # Fetch Nifty 50 market data
        nifty_data = nse_index("NIFTY 50")
        market_cap = nse_market_cap()

        response = {
            "indices": {
                "NIFTY 50": {
                    "lastPrice": nifty_data["lastPrice"],
                    "dayChange": nifty_data["change"],
                    "dayChangePercent": nifty_data["pChange"],
                }
            },
            "totalMarketCap": market_cap["total"],
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/{symbol}")
def stock_details(symbol: str):
    """Fetch stock details by symbol"""
    try:
        stock_data = nse_get_quote(symbol.upper())
        if not stock_data:
            raise HTTPException(status_code=404, detail="Stock not found")

        response = {
            "symbol": stock_data["symbol"],
            "lastPrice": stock_data["lastPrice"],
            "dayHigh": stock_data["dayHigh"],
            "dayLow": stock_data["dayLow"],
            "previousClose": stock_data["previousClose"],
            "totalTradedVolume": stock_data["totalTradedVolume"],
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
