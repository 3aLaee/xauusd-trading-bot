XAU/USD Trading Bot
This is an automated trading bot for the XAU/USD (Gold to US Dollar) currency pair using the MetaTrader 5 (MT5) platform. The bot implements a MACD-based trading strategy combined with price action for generating buy and sell signals.

VERY IMPORTANT NOTES
This code is for testing purposes only, always use trading bots in a demo accounts first. The current setup has predefined risk management rules (SL: 10 pips). Adjust parameters like Stop Loss and Take Profit to suit your proper risk mananagement strategy.

Features
MACD Strategy: The bot uses the MACD (Moving Average Convergence Divergence) indicator to identify potential buy and sell signals.
Support and Resistance Levels: The bot dynamically calculates support and resistance levels using the last 10 bars.
Risk Management: Set Stop Loss (15 pips) and Take Profit (10 pips).
Real-Time Trading: It executes trades in real-time using the MetaTrader 5 API.
Trading Strategy
Buy Signal: A buy signal is triggered when:

The MACD line crosses above the signal line, indicating a bullish trend.
The price crosses above the last resistance level.
Sell Signal: A sell signal is triggered when:

The MACD line crosses below the signal line, indicating a bearish trend.
The price crosses below the last resistance level.
Stop Loss and Take Profit:

Stop Loss is set at 15 pips.
Take Profit is set at 10 pips.
Installation
1. Clone the Repository
git clone github.com/3aLaee/xauusd-trading-bot

2. Install Dependencies
pip install -r requirements.txt

3. Create a .env File
Create a .env file to store sensitive data such as your credentials and trading parameters. Example .env:

ACCOUNT=your_account_number PASSWORD=your_password SERVER=your_server_name PIP_SIZE=0.10 STOP_LOSS_PIPS=15 TAKE_PROFIT_PIPS=10 LOT_SIZE=0.1

Contributing
If you wish to contribute to this project, feel free to fork the repository, make changes, and create a pull request. Please follow the guidelines mentioned below:

Fork the repository. Create a feature branch (git checkout -b feature-name). Make your changes and test them. Commit your changes (git commit -m "Description of the changes"). Push to the branch (git push origin feature-name). Create a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details

