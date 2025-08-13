from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL : str
    ACCESS_TOKEN_EXPIRE_IN_MINUTES : int
    SECRET_KEY : set
    ALGORITHM: str
    SECRET_KEY: str
    
    
    class Config:
        env_file = ".env"
        
settings = Settings()