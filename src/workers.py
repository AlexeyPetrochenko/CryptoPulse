import asyncio

from src.repository import CryptoRepository
from src.clients import CryptoAPIClient
from src.models import NameExchanges, CurrencyPair, PriceSh
from src.config import load_from_env

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


class CryptoPulsWorker:
    def __init__(self, repository: CryptoRepository, exchange_clients: list[CryptoAPIClient]) -> None:
        self.repository = repository
        self.exchange_clients = exchange_clients
        
    async def service_write_in_db(self, data: PriceSh) -> int:
        id = await repository.add_new_max_price(data)
        return id
        
    async def main(self) -> None:
        while True:
            tasks = []
            for client in self.exchange_clients:
                tasks.append(client.get_exchange_rate())
            all_price = await asyncio.gather(*tasks)
            max_price = max(all_price, key=lambda elem: elem.price)
            
            await self.service_write_in_db(max_price)
            await asyncio.sleep(5)



if __name__ == '__main__':
    repository = CryptoRepository()
    exchange_clients = [CryptoAPIClient(**data_client) for data_client in EXCHANGE_CLIENTS]  # type: ignore
    worker = CryptoPulsWorker(repository, exchange_clients=exchange_clients)
    
    asyncio.run(worker.main())
