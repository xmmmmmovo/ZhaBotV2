from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    weather_api_key = ""

    class Config:
        extra = "ignore"
