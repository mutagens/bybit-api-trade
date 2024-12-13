from pybit.unified_trading import HTTP
from bybit_api_trade.utils.core.logger import logger

session = HTTP(testnet=False)


def price_now(symbol):
    try:
        response = session.get_tickers(
            category="spot",
            symbol=symbol
        )


        if response.get('retCode') == 0:

            ticker_data = response['result']['list'][0]
            price = ticker_data['lastPrice']
            logger.info(f"Текущая цена для {symbol}: {price}")
            return float(price)
        else:
            logger.error(f"Ошибка при запросе цены: {response.get('retMsg')}")
            return None
    except Exception as e:
        logger.error(f"Произошла ошибка при запросе цены: {e}")
        return None



symbol = "USDCUSDT"
current_price = price_now(symbol)

if current_price:
    logger.info(f"Цена на данный момент покупки: {current_price}")
else:
    logger.error("Не удалось получить цену.")
