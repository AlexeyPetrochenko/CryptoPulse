from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    
    CMC_PRO_API_KEY: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    
    model_config = SettingsConfigDict(env_file='.env')
    


def load_from_env() -> Config:
    return Config()  # type: ignore
