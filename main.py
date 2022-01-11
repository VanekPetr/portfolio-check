import json
import pandas
from loguru import logger
import yfinance as yf
import datetime

# Initialization
portfolio_value_usd = {}
portfolio_value_czk = {}
date_today = datetime.date.today().strftime('%Y-%m-%d')
date_yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# Load portfolio composition
with open("portfolio_composition.json") as f:
    portfolio_positions = json.load(f)


for stock_name, stock_pos in portfolio_positions['american_stocks'].items():
    try:
        stock_price = yf.download(stock_name, start=date_today, end=date_today)['Adj Close'][0]
    except Exception as e:
        logger.warning(f"Problem when downloading today's data with error: {e}")
        # download yesterday's data
        stock_price = yf.download(stock_name, start=date_yesterday, end=date_yesterday)['Adj Close'][0]

    portfolio_value_usd[stock_name] = stock_price * stock_pos

print("Total portfolio value is ", round(sum(portfolio_value_usd.values())), " USD")

