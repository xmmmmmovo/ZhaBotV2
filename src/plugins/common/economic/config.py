from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    money_unit = ""

    class Config:
        extra = "ignore"