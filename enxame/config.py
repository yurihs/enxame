from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    dokku_hostname: str
    dokku_username: str
    dokku_ssh_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
