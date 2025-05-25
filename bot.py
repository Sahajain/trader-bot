import logging
import streamlit as st
from binance import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize the trading bot with Binance Testnet client."""
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Trading bot initialized with Testnet: %s", testnet)

    def validate_symbol(self, symbol):
        """Validate trading pair symbol."""
        try:
            info = self.client.get_symbol_info(symbol)
            if not info:
                raise ValueError(f"Invalid symbol: {symbol}")
            self.logger.info("Symbol %s validated successfully", symbol)
            return True
        except BinanceAPIException as e:
            self.logger.error("Symbol validation failed: %s", str(e))
            return False

    def place_market_order(self, symbol, side, quantity):
        """Place a market order."""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.logger.info("Market order placed: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place market order: %s", str(e))
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        """Place a limit order."""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            self.logger.info("Limit order placed: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place limit order: %s", str(e))
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        """Place a stop-limit order."""
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price
            )
            self.logger.info("Stop-limit order placed: %s", order)
            return order
        except BinanceAPIException as e:
            self.logger.error("Failed to place stop-limit order: %s", str(e))
            raise

    def get_order_status(self, symbol, order_id):
        """Retrieve order status."""
        try:
            status = self.client.get_order(symbol=symbol, orderId=order_id)
            self.logger.info("Order status retrieved: %s", status)
            return status
        except BinanceAPIException as e:
            self.logger.error("Failed to retrieve order status: %s", str(e))
            raise

def display_order_details(order):
    """Display order details in Streamlit."""
    st.write("**Order Details:**")
    st.write(f"- Symbol: {order['symbol']}")
    st.write(f"- Order ID: {order['orderId']}")
    st.write(f"- Side: {order['side']}")
    st.write(f"- Type: {order['type']}")
    st.write(f"- Quantity: {order['origQty']}")
    st.write(f"- Price: {order.get('price', 'N/A')}")
    st.write(f"- Stop Price: {order.get('stopPrice', 'N/A')}")
    st.write(f"- Status: {order['status']}")
    st.write(f"- Time: {order['time']}")

def main():
    st.title("Binance Futures Testnet Trading Bot")
    st.write("Trade on Binance Futures Testnet with Market, Limit, and Stop-Limit orders.")

    # Load API credentials from .env file
    load_dotenv()
    api_key = os.getenv("api_key")
    api_secret = os.getenv("api_secret")

    if not api_key or not api_secret:
        st.error("API key and secret not found. Please set them in a .env file.")
        return

    bot = BasicBot(api_key, api_secret, testnet=True)

    # Sidebar for action selection
    action = st.sidebar.selectbox("Select Action", [
        "Place Market Order",
        "Place Limit Order",
        "Place Stop-Limit Order",
        "Check Order Status"
    ])

    # Common inputs
    symbol = st.text_input("Trading Pair (e.g., BTCUSDT)", value="BTCUSDT").upper()
    
    if action != "Check Order Status":
        side = st.selectbox("Order Side", ["BUY", "SELL"])
        quantity = st.number_input("Quantity", min_value=0.0, step=0.001, format="%.3f")

    # Validate symbol
    if symbol and st.button("Validate Symbol"):
        if bot.validate_symbol(symbol):
            st.success(f"Symbol {symbol} is valid.")
        else:
            st.error(f"Invalid symbol: {symbol}")

    # Handle different actions
    if action == "Place Market Order" and symbol and quantity > 0:
        if st.button("Place Market Order"):
            try:
                order = bot.place_market_order(symbol, side, quantity)
                st.success("Market order placed successfully!")
                display_order_details(order)
            except BinanceAPIException as e:
                st.error(f"Error: {str(e)}")
                bot.logger.error("Streamlit market order error: %s", str(e))

    elif action == "Place Limit Order" and symbol and quantity > 0:
        price = st.number_input("Limit Price", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Place Limit Order"):
            try:
                order = bot.place_limit_order(symbol, side, quantity, price)
                st.success("Limit order placed successfully!")
                display_order_details(order)
            except (BinanceAPIException, ValueError) as e:
                st.error(f"Error: {str(e)}")
                bot.logger.error("Streamlit limit order error: %s", str(e))

    elif action == "Place Stop-Limit Order" and symbol and quantity > 0:
        stop_price = st.number_input("Stop Price", min_value=0.0, step=0.01, format="%.2f")
        limit_price = st.number_input("Limit Price", min_value=0.0, step=0.01, format="%.2f")
        if st.button("Place Stop-Limit Order"):
            try:
                order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
                st.success("Stop-Limit order placed successfully!")
                display_order_details(order)
            except (BinanceAPIException, ValueError) as e:
                st.error(f"Error: {str(e)}")
                bot.logger.error("Streamlit stop-limit order error: %s", str(e))

    elif action == "Check Order Status" and symbol:
        order_id = st.text_input("Order ID")
        if st.button("Check Status"):
            try:
                status = bot.get_order_status(symbol, order_id)
                st.success("Order status retrieved!")
                display_order_details(status)
            except BinanceAPIException as e:
                st.error(f"Error: {str(e)}")
                bot.logger.error("Streamlit order status error: %s", str(e))

if __name__ == "__main__":
    main()