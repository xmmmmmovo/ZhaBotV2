from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    sleep_time = 8

    class Config:
        extra = "ignore"
