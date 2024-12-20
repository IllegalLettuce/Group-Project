import json
import yfinance as yf
import logging

# Stock definitions
stocks = [
    {"name": "Lockheed Martin", "ticker": "LMT"},
    {"name": "General Dynamics", "ticker": "GD"},
    {"name": "Northrop Grumman", "ticker": "NOC"},
    {"name": "RTX", "ticker": "RTX"},
    {"name": "Boeing", "ticker": "BA"},
    {"name": "L3Harris", "ticker": "LHX"},
    {"name": "Rheinmetall", "ticker": "RHM.DE"},
    {"name": "SAAB", "ticker": "SAAB-B.ST"},
    {"name": "Hensoldt", "ticker": "HAG.DE"},
    {"name": "Leonardo", "ticker": "LDO.MI"},
    {"name": "Dodge", "ticker": ""},
    {"name": "Bitcoin", "ticker": ""},
    {"name": "XHR", "ticker": ""}
]

def fetch_intraday_data_yahoo(ticker, interval="15m", period="5d"):
    """
    Fetch intraday stock data from Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(interval=interval, period=period)
        
        if hist.empty:
            print(f"No intraday data found for {ticker}.")
            return None

        data = hist[["Open", "High", "Low", "Close", "Volume"]].to_dict(orient="index")
        
        formatted_data = {
            date.strftime("%Y-%m-%d %H:%M:%S"): {
                "Open": float(values["Open"]),
                "High": float(values["High"]),
                "Low": float(values["Low"]),
                "Close": float(values["Close"]),
                "Volume": int(values["Volume"]),
            }
            for date, values in data.items()
        }
        
        return formatted_data
    
    except Exception as e:
        print(f"Error fetching intraday data for {ticker}: {e}")
        return None

def get_stock_data(stock_symbol):
    """
    Fetch the latest stock data using Yahoo Finance.
    Returns a list of closing prices for the past 7 days.
    """
    try:
        stock = yf.Ticker(stock_symbol)
        latest_prices = stock.history(period='7d')['Close'].tolist()
        return latest_prices
    except Exception as e:
        logging.error(f"Error fetching stock data for {stock_symbol}: {e}")
        return None

def main_stock_data():
    """
    Fetch and save intraday data for all stocks to a JSON file.
    """
    stock_data = {}
    for stock in stocks:
        if stock["ticker"]:  # Only fetch data if ticker is not empty
            data = fetch_intraday_data_yahoo(stock["ticker"], interval="15m", period="5d")
            if data:
                stock_data[stock["name"]] = data

    output_filename = "stock_data.json"
    with open(output_filename, "w") as json_file:
        json.dump(stock_data, json_file, indent=2)
    print(f"Data saved to {output_filename}")

def get_all_stocks():
    """
    Return the list of all available stocks.
    """
    return stocks

# Helper function to validate stock ticker
def is_valid_stock(ticker):
    """
    Check if a given ticker exists in our stock list.
    """
    return any(stock["ticker"] == ticker for stock in stocks)

def get_stock_by_name(name):
    """
    Get stock information by company name.
    """
    for stock in stocks:
        if stock["name"].lower() == name.lower():
            return stock
    return None

def get_stock_by_ticker(ticker):
    """
    Get stock information by ticker symbol.
    """
    for stock in stocks:
        if stock["ticker"].lower() == ticker.lower():
            return stock
    return None

def get_current_price(ticker):
    """
    Get the current price of a stock.
    """
    try:
        if not ticker:
            return None
        stock = yf.Ticker(ticker)
        return stock.info.get('regularMarketPrice')
    except Exception as e:
        logging.error(f"Error fetching current price for {ticker}: {e}")
        return None