import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

<<<<<<< HEAD
# Retrieve sensitive data from environment variables
account = int(os.getenv("MT5_ACCOUNT", "0"))  # Ensures account is int
=======
account = os.getenv("MT5_ACCOUNT")
>>>>>>> 25ca9d097fe87cd35b145727ddbb2cfb82d9ba69
password = os.getenv("MT5_PASSWORD")
server = os.getenv("MT5_SERVER")
symbol = os.getenv("SYMBOL")

pip_size = float(os.getenv("PIP_SIZE", 0.10))  
stop_loss_pips = float(os.getenv("STOP_LOSS_PIPS", 15)) * pip_size
take_profit_pips = float(os.getenv("TAKE_PROFIT_PIPS", 10)) * pip_size
lot_size = float(os.getenv("LOT_SIZE", 0.1))

<<<<<<< HEAD
# Connect to MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5.")
    quit()

if not mt5.login(account, password=password, server=server):
    print(f"Failed to log in to MetaTrader 5. Error: {mt5.last_error()}")
    mt5.shutdown()
    quit()
=======
# Connect to MT5
mt5.initialize()
mt5.login(account, password=password, server=server)
>>>>>>> 25ca9d097fe87cd35b145727ddbb2cfb82d9ba69

def get_data():
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 50)  # 50 1-min candles
    if rates is None:
        print(f"Error retrieving data for {symbol}")
        return None
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data

# Calculate MACD and determine if there’s a crossover
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    data['ema_fast'] = data['close'].ewm(span=fast_period, adjust=False).mean()
    data['ema_slow'] = data['close'].ewm(span=slow_period, adjust=False).mean()
    data['macd'] = data['ema_fast'] - data['ema_slow']
    data['signal'] = data['macd'].ewm(span=signal_period, adjust=False).mean()
    data['hist'] = data['macd'] - data['signal']
    data['macd_cross'] = (data['macd'] > data['signal']) & (data['macd'].shift(1) <= data['signal'].shift(1))
    data['signal_cross'] = (data['macd'] < data['signal']) & (data['macd'].shift(1) >= data['signal'].shift(1))
    return data

# Identify support and resistance levels using the last 10 bars
def find_support_resistance(data):
    recent_highs = data['high'].tail(10)
    recent_lows = data['low'].tail(10)
    resistance_level = recent_highs.max()  # Highest high in the last 10 bars
    support_level = recent_lows.min()      # Lowest low in the last 10 bars
    return resistance_level, support_level

# Check if the market is open
def is_market_open(symbol):
    market_info = mt5.symbol_info(symbol)
    if market_info is None:
        print("Error retrieving market info.")
        return False
    return market_info.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL

# Check if a buy or sell signal is triggered
def check_trade_conditions(data, resistance_level, support_level):
    latest = data.iloc[-1]
    if latest['signal_cross'] and latest['hist'] < 0 and latest['close'] < resistance_level:
        return "sell"
    elif latest['macd_cross'] and latest['hist'] > 0 and latest['close'] > resistance_level:
        return "buy"
    return None

#Check open positions
def show_open_positions():
    positions = mt5.positions_get()
    if positions is None:
        print("No open positions or failed to retrieve positions.")
        return
    if len(positions) > 0:
        print("Open positions:")
        for pos in positions:
            print(f"Symbol: {pos.symbol}, Type: {'Buy' if pos.type == 0 else 'Sell'}, Volume: {pos.volume}, Price: {pos.price_open}")
    else:
        print("No open positions.")


# Execute trades
def place_order(direction, price):
    sl = price - stop_loss_pips if direction == "sell" else price + stop_loss_pips
    tp = price + take_profit_pips if direction == "sell" else price - take_profit_pips
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_TYPE_SELL if direction == "sell" else mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "Auto-trading bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.retcode}")
    else:
        print(f"{direction.capitalize()} order placed at {price}")

# Run the trading bot in a loop
while True:
    print("Checking market status...")
    if is_market_open(symbol):
        print(f"Market for {symbol} is open.")
    else:
        print(f"Market for {symbol} is not open. Exiting.")
        mt5.shutdown()
        quit()


    data = get_data()
    if data is None or data.empty:
        sleep(60)
        continue

    data = calculate_macd(data)
    resistance_level, support_level = find_support_resistance(data)
    trade_signal = check_trade_conditions(data, resistance_level, support_level)

    if trade_signal:
        latest_price = mt5.symbol_info_tick(symbol).ask if trade_signal == "buy" else mt5.symbol_info_tick(symbol).bid
        place_order(trade_signal, latest_price)
    
    show_open_positions()

    sleep(60)  # Wait for the next minute candle
