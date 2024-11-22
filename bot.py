import MetaTrader5 as mt5
import pandas as pd
import logging
from time import sleep
from dotenv import load_dotenv
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Trading configuration
account = int(os.getenv("MT5_ACCOUNT", "0"))
password = os.getenv("MT5_PASSWORD")
server = os.getenv("MT5_SERVER")
symbol = os.getenv("SYMBOL")
pip_size = float(os.getenv("PIP_SIZE", 0.01))
stop_loss_pips = float(os.getenv("STOP_LOSS_PIPS", 15)) * pip_size
take_profit_pips = float(os.getenv("TAKE_PROFIT_PIPS", 10)) * pip_size
lot_size = float(os.getenv("LOT_SIZE", 0.1))

# Initialize MetaTrader 5
def initialize_mt5():
    if not mt5.initialize():
        logging.error("Failed to initialize MetaTrader 5.")
        sys.exit()
    if not mt5.login(account, password=password, server=server):
        logging.error(f"Failed to log in to MetaTrader 5. Error: {mt5.last_error()}")
        mt5.shutdown()
        sys.exit()

# Check if the market is open for the given symbol
def is_market_open(symbol):
    market_info = mt5.symbol_info(symbol)
    if market_info is None:
        logging.error(f"Error retrieving market info for {symbol}. Symbol might not be available.")
        return False
    if market_info.trade_mode == mt5.SYMBOL_TRADE_MODE_DISABLED:
        logging.info(f"Market for {symbol} is closed or disabled for trading.")
        return False
    return True

# Get recent market data
def get_data(symbol):
    try:
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 50)
        if rates is None:
            logging.error("Failed to retrieve data from MetaTrader 5.")
            return pd.DataFrame()
        data = pd.DataFrame(rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        return data
    except Exception as e:
        logging.error(f"Error in get_data: {e}")
        return pd.DataFrame()

# Calculate MACD indicator
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    data['ema_fast'] = data['close'].ewm(span=fast_period, adjust=False).mean()
    data['ema_slow'] = data['close'].ewm(span=slow_period, adjust=False).mean()
    data['macd'] = data['ema_fast'] - data['ema_slow']
    data['signal'] = data['macd'].ewm(span=signal_period, adjust=False).mean()
    data['hist'] = data['macd'] - data['signal']
    data['macd_cross'] = (data['macd'] > data['signal']) & (data['macd'].shift(1) <= data['signal'].shift(1))
    data['signal_cross'] = (data['macd'] < data['signal']) & (data['macd'].shift(1) >= data['signal'].shift(1))
    return data

# Find support and resistance levels
def find_support_resistance(data):
    recent_highs = data['high'].tail(10)
    recent_lows = data['low'].tail(10)
    resistance_level = recent_highs.max()
    support_level = recent_lows.min()
    return resistance_level, support_level


# Check for trading signals
def check_trade_conditions(data, resistance_level, support_level):
    latest = data.iloc[-1]
    if latest['signal_cross'] and latest['hist'] < 0 and latest['close'] < resistance_level:
        return "sell"
    elif latest['macd_cross'] and latest['hist'] > 0 and latest['close'] > support_level:
        return "buy"
    return None

# Function to calculate indicators for testing
def calculate_indicators(data):
    """
    Calculates and returns key indicators such as MACD, support, and resistance.
    Returns:
        dict: A dictionary with MACD, support, and resistance values.
    """
    data_with_macd = calculate_macd(data)
    resistance_level, support_level = find_support_resistance(data_with_macd)
    return {
        "macd": data_with_macd[['macd', 'signal', 'hist']].tail(1).to_dict('records')[0],
        "support": support_level,
        "resistance": resistance_level
    }


# Place an order with MetaTrader 5
def place_order(direction, price):
    # Determine order type and SL/TP prices based on direction
    if direction == "sell":
        order_type = mt5.ORDER_TYPE_SELL
        sl = price + stop_loss_pips  # Stop Loss above sell price
        tp = price - take_profit_pips  # Take Profit below sell price
    else:  # buy
        order_type = mt5.ORDER_TYPE_BUY
        sl = price - stop_loss_pips  # Stop Loss below buy price
        tp = price + take_profit_pips  # Take Profit above buy price

    # Place order with SL and TP
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": sl,  # Stop Loss price
        "tp": tp,  # Take Profit price
        "deviation": 20,
        "magic": 123456,
        "comment": "Auto-trading bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Order failed: {result.retcode} - {result.comment}")
    else:
        logging.info(f"{direction.capitalize()} order placed at {price} with SL: {sl} and TP: {tp}")


# Display open positions
def show_open_positions():
    positions = mt5.positions_get()
    if positions is None:
        logging.warning("No open positions or failed to retrieve positions.")
        return
    if len(positions) > 0:
        logging.info("Open positions:")
        for pos in positions:
            logging.info(f"Symbol: {pos.symbol}, Type: {'Buy' if pos.type == 0 else 'Sell'}, "
                         f"Volume: {pos.volume}, Open Price: {pos.price_open}, "
                         f"SL: {pos.sl}, TP: {pos.tp}")
    else:
        logging.info("No open positions.")

# Main trading loop
def run_trading_bot():
    if not is_market_open(symbol):
        logging.warning("Market is closed. Exiting.")
        return
    while True:
        data = get_data(symbol)
        if data.empty:
            logging.error("Data retrieval failed. Skipping this iteration.")
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

# Initialize MT5 and start the trading bot
initialize_mt5()
run_trading_bot()
