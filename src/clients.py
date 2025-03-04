from datetime import datetime
from decimal import Decimal

import httpx
from jsonpath_ng import parse, DatumInContext

from src.models import PriceSh, NameExchanges, CurrencyPair


class CryptoAPIClient:
    def __init__(
        self, 
        exchange_name: NameExchanges, 
        currency_pair: CurrencyPair, 
        url: str,
        json_path: str,
        params: dict[str, str] | None = None, 
        headers: dict[str, str] | None = None
    ) -> None:
        self.exchange_name = exchange_name
        self.currency_pair = currency_pair
        self.url = url
        self.json_path = json_path
        self.params = params
        self.headers = headers
        
    async def request_to_api(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=self.url, params=self.params, headers=self.headers)
            json_response = response.json()
            return json_response
        
    def parsing_data(self, json_data: str) -> DatumInContext:
        path = parse(self.json_path)
        return path.find(json_data)
        
    async def get_exchange_rate(self) -> PriceSh:
        data = await self.request_to_api()
        price = Decimal(self.parsing_data(data)[0].value)
        
        return PriceSh(
            exchange_name=self.exchange_name,
            currency_pair=self.currency_pair,
            price=price,
            max_price=price,
            min_price=price,
            difference=price - price,
            total_amount=3 * price,
            date_at=datetime.now()
        )
