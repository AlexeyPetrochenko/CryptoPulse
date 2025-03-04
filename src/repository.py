from sqlalchemy import select

from src.models import PriceSh, PriceСrypto, PriceShFromDB
from src.db import session_maker
from src.config import logger


class CryptoRepository:
    
    async def add_new_max_price(self, data: PriceSh) -> int:
        async with session_maker() as session:
            price = PriceСrypto(**data.model_dump())
            session.add(price)
            await session.commit()
            logger.info("Commit Success")
            return price.id

    async def get_max_price(self) -> PriceShFromDB | None:
        async with session_maker() as session:
            stmt = select(PriceСrypto).order_by(PriceСrypto.price.desc(), PriceСrypto.date_at.desc()).limit(1)
            result = await session.execute(stmt)
            price = result.scalar()
            if price:
                return PriceShFromDB.model_validate(price)
            return None
