import asyncio
import logging

from src.workers import CryptoPulsWorker
from src.clients import CryptoAPIClient
from src.repository import CryptoRepository
from src.models import NameExchanges, CurrencyPair
from src.config import load_from_env, configure_logging
from src.config import logger


EXCHANGE_CLIENTS = [
    {
        'exchange_name': NameExchanges.BINANCE, 
        'currency_pair': CurrencyPair.BTC_USDT, 
        'url': 'https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT',
        'json_path': '$.price'
    },
    {
        'exchange_name': NameExchanges.COINMARKETCAP, 
        'currency_pair': CurrencyPair.BTC_USDT, 
        'url': 'https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT',
        'json_path': '$.price',
        'headers': {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': load_from_env().CMC_PRO_API_KEY,
            }
    },
    {
        'exchange_name': NameExchanges.KUCOIN, 
        'currency_pair': CurrencyPair.BTC_USDT, 
        'url': 'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT',
        'json_path': '$.data.price',
    },
    {
        'exchange_name': NameExchanges.BYBIT, 
        'currency_pair': CurrencyPair.BTC_USDT, 
        'url': 'https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT',
        'json_path': '$.result.list[0].lastPrice',
    },
]


if __name__ == '__main__':
    configure_logging(logging.INFO)
    
    repository = CryptoRepository()
    exchange_clients = [CryptoAPIClient(**data_client) for data_client in EXCHANGE_CLIENTS]  # type: ignore
    worker = CryptoPulsWorker(repository, exchange_clients=exchange_clients)
    try:
        asyncio.run(worker.main())
    except KeyboardInterrupt:
        logger.info('Worker Stopped')
