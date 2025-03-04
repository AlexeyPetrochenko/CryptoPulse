import asyncio

from src.repository import CryptoRepository
from src.clients import CryptoAPIClient
from src.config import logger


class CryptoPulsWorker:
    def __init__(self, repository: CryptoRepository, exchange_clients: list[CryptoAPIClient]) -> None:
        self.repository = repository
        self.exchange_clients = exchange_clients
        
        
    async def compare_and_update_prices(self, crypto_client: CryptoAPIClient) -> None:
        price_now, max_price = await asyncio.gather(
            crypto_client.get_exchange_rate(), 
            self.repository.get_max_price()
        )
        
        if max_price is None:
            await self.repository.add_new_max_price(price_now)
            return None
        
        if price_now.price > max_price.price:
            await self.repository.add_new_max_price(price_now)
            logger.info('Цена обновлена %s -> %s', max_price.price, price_now.price)
    
        
        
    async def main(self) -> None:
        logger.info("Worker Start")
        while True:
            for client in self.exchange_clients:
                await self.compare_and_update_prices(client)
            await asyncio.sleep(5)
