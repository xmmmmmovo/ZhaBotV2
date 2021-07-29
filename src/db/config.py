from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    mongo_url = ""

    class Config:
        extra = "ignore"