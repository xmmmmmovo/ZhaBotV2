from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    app_id = ""
    app_key = ""

    class Config:
        extra = "ignore"
