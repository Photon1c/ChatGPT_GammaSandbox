import numpy as np
from scipy.stats import norm
import yfinance as yf
import datetime

def d1(S, K, r, sigma, T):
    """Calculate d1 in the Black-Scholes model."""
    d1 = (np.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * np.sqrt(T))
    return d1

def d2(S, K, r, sigma, T):
    """Calculate d2 in the Black-Scholes model."""
    d2 = d1(S, K, r, sigma, T) - sigma * np.sqrt(T)
    return d2

def call_price(S, K, r, sigma, T):
    """Calculate the price of a European call option using the Black-Scholes model."""
    d1_val = d1(S, K, r, sigma, T)
    d2_val = d2(S, K, r, sigma, T)
    call_price = S * norm.cdf(d1_val) - K * np.exp(-r * T) * norm.cdf(d2_val)
    return call_price

# User input
ticker = input('Enter a ticker symbol: ')
expiration = input('Enter an expiration date in YYYY-MM-DD format: ')
strike_price = float(input('Enter a strike price: '))

# Stock data
stock = yf.Ticker(ticker)
S = stock.history(period='1d')['Close'][0] # current stock price
market_returns = yf.Ticker('^GSPC').history(period='max', interval='1mo').Close.pct_change().dropna() # historical market returns
r = np.mean(market_returns) # expected return (annualized)
sigma = stock.history(period='1y').Close.pct_change().std() * np.sqrt(252) # annualized volatility

# Calculate time to expiration in years
today = datetime.date.today()
T = (expiration - today).days / 365

# Calculate the call price using the Black-Scholes model
call_price = call_price(S, strike_price, r, sigma, T)

print(f'Call price for {ticker} with a strike price of {strike_price} and expiration date of {expiration} is: {call_price:.2f}')