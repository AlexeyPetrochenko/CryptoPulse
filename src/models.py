from decimal import Decimal
from datetime import datetime
from enum import StrEnum

from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, ConfigDict

from src.db import Base


class CurrencyPair(StrEnum):
    BTC_USDT = 'BTC_USDT'
    BTC_ETH = "ETH_BTC"
    BTC_XMR = "BTC_XMR"
    BTC_SOL = "BTC_SOL"
    BTC_RUB = "BTC_RUB"
    BTC_DOGE = "BTC_DOGE"
    
    
class NameExchanges(StrEnum):
    BINANCE = 'binance'
    KUCOIN = 'kucoin'
    BYBIT = 'bybit'
    COINMARKETCAP = 'coinmarketcap'


class PriceСrypto(Base):
    __tablename__ = 'price_crypto'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_name: Mapped[str]
    currency_pair: Mapped[str]
    price: Mapped[Decimal]
    max_price: Mapped[Decimal]
    min_price: Mapped[Decimal]
    difference: Mapped[Decimal]
    total_amount: Mapped[Decimal]
    date_at: Mapped[datetime] = mapped_column(index=True)



class PriceSh(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    exchange_name: NameExchanges
    currency_pair: CurrencyPair
    price: Decimal
    max_price: Decimal
    min_price: Decimal
    difference: Decimal
    total_amount: Decimal
    date_at: datetime
    

class PriceShFromDB(PriceSh):
    id: int
