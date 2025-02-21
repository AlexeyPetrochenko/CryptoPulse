from src.models import PriceSh, PriceСrypto
from src.db import session_maker


class CryptoRepository:
    
    async def add_new_max_price(self, data: PriceSh) -> int:
        async with session_maker() as session:
            price = PriceСrypto(**data.model_dump())
            session.add(price)
            await session.commit()
            return price.id
