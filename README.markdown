# Binance Futures Testnet Trading Bot

A Python-based trading bot for placing orders on the Binance Futures Testnet using the `python-binance` library and a Streamlit web interface. The bot supports market, limit, and stop-limit orders, with logging and error handling.

## Features

- **Order Types**: Place market, limit, and stop-limit orders (buy/sell) on Binance Futures Testnet (USDT-M).
- **Streamlit UI**: User-friendly web interface for entering trading parameters and viewing order details.
- **Symbol Validation**: Validates trading pairs before order placement.
- **Order Status**: Check the status of placed orders by order ID.
- **Logging**: Logs all API requests, responses, and errors to `trading_bot.log`.
- **Error Handling**: Displays errors in the UI and logs them for debugging.
- **Secure Credentials**: Stores API key and secret in a `.env` file.

## Prerequisites

- **Python 3.8+**
- **Binance Testnet Account**: Register at https://testnet.binance.vision/ and generate API key and secret.
- **Dependencies**:
  - `streamlit`
  - `python-binance`
  - `python-dotenv`

## Installation

1. **Clone or Download the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

   Alternatively, download and extract the project files.

2. **Install Dependencies**:

   ```bash
   pip install streamlit python-binance python-dotenv
   ```

3. **Set Up API Credentials**:

   - Create a `.env` file in the project directory.
   - Add your Binance Testnet API key and secret:

     ```
     api_key=your_binance_testnet_api_key
     api_secret=your_binance_testnet_api_secret
     ```
   - Replace `your_binance_testnet_api_key` and `your_binance_testnet_api_secret` with your credentials from the Binance Testnet dashboard.

4. **Ensure Test Funds**:

   - Fund your Binance Testnet account with test USDT via the Testnet faucet.

## Usage

1. **Run the Application**:

   ```bash
   streamlit run bot.py
   ```

   - Streamlit will start a local server and provide a URL (e.g., `http://localhost:8501`).
   - Open the URL in your browser.

2. **Using the Interface**:

   - **Select Action**: Choose from "Place Market Order," "Place Limit Order," "Place Stop-Limit Order," or "Check Order Status" in the sidebar.
   - **Enter Parameters**:
     - **Trading Pair**: Input a valid pair (e.g., `BTCUSDT`).
     - **Order Side**: Select `BUY` or `SELL`.
     - **Quantity**: Specify the order quantity.
     - **Price** (for limit orders): Enter the limit price.
     - **Stop Price and Limit Price** (for stop-limit orders): Enter both prices.
     - **Order ID** (for status checks): Provide the order ID.
   - **Validate Symbol**: Click "Validate Symbol" to ensure the trading pair is valid.
   - **Place Order or Check Status**: Click the corresponding button to execute the action.
   - **View Results**: Order details or errors are displayed below the input fields.

## Example `.env` File

```plaintext
api_key=abc123xyz456
api_secret=def789ghi012
```

## 

## 

## Project Structure

```
<project-directory>/
│
├── binance_trading_bot.py  # Main script with bot logic and Streamlit UI
├── .env                    # API credentials (not tracked by git)
├── trading_bot.log         # Log file for API interactions and errors
├── README.md               # This file
```

## 