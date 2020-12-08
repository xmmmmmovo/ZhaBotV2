from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    bot_sql = ""

    class Config:
        extra = "ignore"
