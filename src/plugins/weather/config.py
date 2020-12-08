from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    weather_api_key = ""
    base_dir = ""

    class Config:
        extra = "ignore"
