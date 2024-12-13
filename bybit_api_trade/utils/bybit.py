import time
import json
from datetime import datetime

from pybit.unified_trading import HTTP

from bybit_api_trade.config import api_keys
from bybit_api_trade.utils.monitoring_token import price_now
from logger import logger


sessions = [
    HTTP(api_key=key['api_key'], api_secret=key['api_secret'], testnet=False)  # True для тестовой среды, False для основной среды
    for key in api_keys
]


def place_market_order(session, symbol, qty):
    try:
        response = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=qty,
        )

        if response and 'result' in response:
            order_id = response['result'].get('orderId')
            order_link_id = response['result'].get('orderLinkId')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            order_data = {
                "order_id": order_id,
                "order_link_id": order_link_id,
                "symbol": symbol,
                "qty": qty,
                "timestamp": timestamp,
                "type": "Market",
                "status": response.get("retMsg", "Unknown Status")
            }

            logger.info(f"Цена на данный момент покупки: {price_now(symbol)}")
            time.sleep(3)

            logger.info(f"Создан ордер по маркету: ID ордера {order_id}")
            save_order_history(order_data)
        else:
            logger.error(f"Ошибка при размещении ордера на аккаунте: {response.get('retMsg', 'Неизвестная ошибка')}")
    except Exception as e:
        logger.error(f"Ошибка при размещении ордера: {e}")


def place_order_market_mult(symbol, qty):
    for i, session in enumerate(sessions):
        logger.info(f"Попытка разместить ордер на аккаунте {i + 1}")
        place_market_order(session, symbol, qty)

def place_order_limit(session, symbol, qty, price):
    try:
        response = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=qty,
            price=price
        )

        if response and 'result' in response:
            order_id = response['result'].get('orderId')
            order_link_id = response['result'].get('orderLinkId')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            order_data = {
                "order_id": order_id,
                "order_link_id": order_link_id,
                "symbol": symbol,
                "qty": qty,
                "timestamp": timestamp,
                "type": "Market",
                "status": response.get("retMsg", "Unknown Status")
            }

            logger.info(f"Цена на данный момент покупки: {price_now(symbol)}")
            time.sleep(3)

            logger.info(f"Создан ордер по лимиту: ID ордера {order_id}")
            save_order_history(order_data)
        else:
            logger.error(f"Ошибка при размещении ордера на аккаунте: {response.get('retMsg', 'Неизвестная ошибка')}")
    except Exception as e:
        logger.error(f"Ошибка при размещении ордера: {e}")

def place_order_limit_mult(symbol, qty, price):
    for i, session in enumerate(sessions):
        logger.info(f"Попытка разместить лимит-ордер на аккаунте {i + 1}")
        place_order_limit(session=session, symbol=symbol, qty=qty, price=price)


def sell_market_order(session, symbol, qty):
    try:
        response = session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=qty,
        )

        logger.info(f"Цена на данный момент покупки: {price_now(symbol)}")
        time.sleep(3)

        if response and 'result' in response:
            order_id = response['result'].get('orderId')
            order_link_id = response['result'].get('orderLinkId')
            logger.info(f"Маркет-ордер на продажу для {symbol} успешно размещен на аккаунте. Order ID: {order_id}, Order Link ID: {order_link_id}")
        else:
            logger.error(f"Ошибка при размещении ордера на аккаунте: {response.get('retMsg', 'Неизвестная ошибка')}")
    except Exception as e:
        logger.error(f"Ошибка при размещении ордера: {e}")


def sell_order_market_mult(symbol, qty):
    for i, session in enumerate(sessions):
        logger.info(f"Попытка разместить ордер на аккаунте {i + 1}")
        sell_market_order(session, symbol, qty)


def sell_order_limit(session, symbol, qty, price):
    try:
        response = session.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            order_type="Market",
            qty=qty,
            price=price
        )

        logger.info(f"Цена на данный момент покупки: {price_now(symbol)}")

        time.sleep(3)
        if response and 'result' in response:
            order_id = response['result'].get('orderId')
            order_link_id = response['result'].get('orderLinkId')
            logger.info(f"Лимит-ордер на продажу для {symbol} успешно размещен на аккаунте. Order ID: {order_id}, Order Link ID: {order_link_id}")
        else:
            logger.error(f"Ошибка при размещении ордера на аккаунте: {response.get('retMsg', 'Неизвестная ошибка')}")
    except Exception as e:
        logger.error(f"Ошибка при размещении ордера: {e}")

def sell_order_limit_mult(symbol, qty, price):
    for i, session in enumerate(sessions):
        logger.info(f"Попытка разместить ордер на аккаунте {i + 1}")
        sell_order_limit(session, symbol, qty, price)




def get_balance():
    for i, session in enumerate(sessions):
        try:
            response = session.get_wallet_balance(account_type="SPOT")

            if response['retCode'] == 0:
                result = response['result']
                logger.info(f"Баланс успешно получен для аккаунта {i + 1}.")

                for currency, data in result.items():
                    logger.info(f"{currency}: {data['availableBalance']} {currency}")
            else:
                logger.error(f"Ошибка при получении баланса для аккаунта {i + 1}: {response['retMsg']}")
        except Exception as e:
            logger.error(f"Ошибка при запросе баланса для аккаунта {i + 1}: {e}")



def save_order_history(order_data, filename="order_history.json"):
    try:
        try:
            with open(filename, "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        history.append(order_data)

        with open(filename, "w") as f:
            json.dump(history, f, indent=4)

        print(f"Данные ордера сохранены: {order_data}")
    except Exception as e:
        print(f"Ошибка сохранения истории ордеров: {e}")


