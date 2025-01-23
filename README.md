# XAU/USD Trading Bot

This is an automated bot designed to trade the **Gold (XAU) to US Dollar (USD)** currency pair on the MetaTrader 5 (MT5) platform. It uses a **MACD-based trading strategy** combined with **price action** to generate buy and sell signals.

---

## ⚠️ VERY IMPORTANT NOTES

> This software is for educational and testing purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.
>Always start by running a trading bot on demo accounts and do not engage money before you understand how it works and what profit/loss you should expect.
> The current setup includes predefined risk management rules (e.g., **Stop Loss: 15 pips**). Adjust these parameters to match your personal risk management strategy.
> Better results are shown during the London session.

---

## 🌟 Features

- **MACD Strategy:**  
  The bot uses the **MACD (Moving Average Convergence Divergence)** indicator to identify buy and sell signals based on market momentum.

- **Price Action:**  
  Dynamic calculation of **support** and **resistance levels** using the last 10 bars to optimize trade entry/exit points.

- **Risk Management:**  
  Predefined **Stop Loss** (15 pips) and **Take Profit** (10 pips) for automated risk management.

- **Real-Time Trading:**  
  Executes trades in real-time using the **MetaTrader 5 API**.

---

## 📈 Trading Strategy

### Buy Signal Setup:
- When the MACD line crosses above the signal line **then** the price crosses above the last resistance level in the 1 min time frame.

### Sell Signal Setup:
- When the MACD line crosses below the signal line **then** the price crosses below the last support level in the 1 min time frame.

### Risk Management:
- **Stop Loss:** Set at **15 pips**.
- **Take Profit:** Set at **10 pips**.

---

## ⚙️ Installation

### 1. Clone the Repository

First, clone this repository to your local machine:
git clone https://github.com/3aLaee/xauusd-trading-bot.git

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Set Up the `.env` File

Create a `.env` file to store data such as your MetaTrader 5 credentials and trading parameters. Here's an example of what the `.env` file should look like:
  > ACCOUNT=your_account_number
  > PASSWORD=your_password
  > SERVER=your_server_name
  > PIP_SIZE=0.10
  > STOP_LOSS_PIPS=15
  > TAKE_PROFIT_PIPS=10
  > LOT_SIZE=0.1

## 🛠 Contributing

I welcome contributions! To contribute to this project, follow these steps:

1. **Fork the repository** and clone it to your local machine.
2. **Create a new branch** for your feature:
   git checkout -b feature-name
3. Make your changes to the code.
4. Commit your changes with a descriptive message:
  git commit -m "Description of the changes"
5- Push to your fork:
  git push origin feature-name
6. Create a pull request to merge your changes into the main branch.

We ask that you ensure your code is clean, well-documented, and thoroughly tested before submitting a pull request.

## 📝 License
This project is licensed under the ![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
. For more details, please check the LICENSE file.










