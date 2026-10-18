from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    database_url:str
    jwt_secret_key:str
    jwt_algorithms:str="HS256"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings=Setting()