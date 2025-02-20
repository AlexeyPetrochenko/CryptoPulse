import httpx
import enum
import time
import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    CMC_PRO_API_KEY: str
    
    model_config = SettingsConfigDict(env_file='.env')
    
config = Config()  


class CurrencyPair(enum.StrEnum):
    BTC_USDT = 'BTCUSDT'
    BTC_ETH = "ETHBTC"
    BTC_XMR = "BTCXMR"
    BTC_SOL = "BTC_SOL"
    BTC_RUB = "BTC_RUB"
    BTC_DOGE = "BTC_DOGE"


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': config.CMC_PRO_API_KEY,
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
        
        
        
if __name__ == '__main__':
    start = time.time()
    client = CryptoAPIClient()
    answer = asyncio.run(client.request_to_api())
    print(answer)
    print(time.time() - start)
