from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    sign_in_money_lower_limit = 1
    sign_in_money_upper_limit = 20
    money_unit = ""

    class Config:
        extra = "ignore"
