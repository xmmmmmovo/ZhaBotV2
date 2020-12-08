from typing import Any

from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    morning_groups: Any
    bots: Any
    weather_api_key = ""

    class Config:
        extra = "ignore"
