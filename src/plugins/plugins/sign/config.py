from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    sign_in_money_down = 1
    sign_in_money_up = 20
    money_unit = ""

    class Config:
        extra = "ignore"
