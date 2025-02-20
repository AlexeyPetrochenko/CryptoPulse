import httpx
import time
import asyncio
from decimal import Decimal
from datetime import datetime

from src.config import load_from_env
from src.repository import CryptoRepository
from src.models import PriceSh, NameExchanges, CurrencyPair


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': load_from_env().CMC_PRO_API_KEY,
}
    
    

class CryptoAPIClient:
    
    async def request_to_api(self) -> tuple:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=USDT',
                headers=headers
            )
            response1 = await client.get('https://data-api.binance.vision/api/v3/ticker/price?symbol=BTCUSDT')
            response2 = await client.get('https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT')
            response3 = await client.get('https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT')
            
            data_binance = response1.json()
            data_kucoin = response2.json()
            data_coinmarket = response.json()
            data_bybit = response3.json()
            
            price_binance = data_binance['price']
            price_kucoin = data_kucoin['data']['price']
            price_coinmarket = data_coinmarket["data"]["BTC"]["quote"]["USDT"]["price"]
            price_bybit = data_bybit['result']['list'][0]['lastPrice']
            
            return price_coinmarket, price_binance, price_kucoin, price_bybit
        
        
    async def make_data(self) -> PriceSh:
        tuple_prices = await self.request_to_api()
        max_price = max(map(float, tuple_prices))
        data = PriceSh(
            exchange_name=NameExchanges.BINANCE,
            currency_pair=CurrencyPair.BTC_USDT,
            price=Decimal(max_price),
            max_price=Decimal(max_price),
            min_price=Decimal(max_price),
            difference=Decimal(max_price - max_price),
            total_amount=Decimal(3 * max_price),
            date_at=datetime.now()
        )
        return data
    
    
    async def service_write_in_db(self) -> int:
        data = await self.make_data()
        id = await CryptoRepository.add_new_max_price(data)
        return id
        
if __name__ == '__main__':
    start = time.time()
    client = CryptoAPIClient()
    answer = asyncio.run(client.service_write_in_db())
    print(time.time() - start)
