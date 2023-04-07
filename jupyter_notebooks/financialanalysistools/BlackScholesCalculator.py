#Simple Black-Scholes price function calculator
from mibian import BS
import yfinance as yf
import pandas as pd
import datetime as dt

#create starting and ending dates, set to nearest friday and two weeks from nearest friday
get_first_friday = dt.date.today()
while get_first_friday.weekday() != 4:
    get_first_friday += dt.timedelta(1)
two_weeks = dt.timedelta(days=14)
two_weeks_from_nearest_friday = get_first_friday + two_weeks
two_weeks_from_nearest_friday_formatted = two_weeks_from_nearest_friday.strftime("%Y-%m-%d")

# Define the stock symbol and expiration date
stock = yf.Ticker(input("Enter the Stock Ticker: "))
#make a quick expiration date using the datetime module, while this is automatic 3 weeks out this can just be inputted by user                  
expiration_date = two_weeks_from_nearest_friday_formatted                  
#expiration_date = input("Enter the Expiration Date in YYYY-MM-DD Format: )
strike_price = int(input("Enter the strike price: "))

# Get the option chain for the expiration date
options = stock.option_chain(expiration_date)

# Get the call option with the strike price defined by user
option = options.calls[options.calls["strike"] == strike_price].iloc[0]

# Define the parameters for the Black-Scholes model
underlying_price = stock.info["regularMarketPrice"]
strike_price = option["strike"]
expiration = option.get('expiration', None)

# initialize time_to_expiration to None
time_to_expiration = (pd.to_datetime(expiration_date) - pd.to_datetime('today')).days / 365
if expiration is not None:
    # process the expiration value
    try:
        time_to_expiration = (option["expiration"] - option["lastTradeDate"]).days / 365.0
    except:
        print("Try again!")
else:
    # handle the missing key error
    print("Warning! Missing Key")
risk_free_rate = 0.01
implied_volatility = option["impliedVolatility"] / 100.0

# Calculate the call option price using the Black-Scholes model
bs = BS([underlying_price, strike_price, risk_free_rate, time_to_expiration],
        volatility=implied_volatility)
call_price = bs.callPrice

print(f"Call option price: {call_price:.2f}")

