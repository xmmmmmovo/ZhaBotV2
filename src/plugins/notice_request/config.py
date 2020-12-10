from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    request_on = False
    notice_on = False

    class Config:
        extra = "ignore"
