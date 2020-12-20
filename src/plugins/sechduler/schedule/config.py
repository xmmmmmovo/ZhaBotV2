from typing import Any

from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    morning_groups: Any
    weather_api_key = ""
    base_dir = ""

    class Config:
        extra = "ignore"
