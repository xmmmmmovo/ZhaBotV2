from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    mysql_host = ""
    mysql_port = ""
    mysql_user = ""
    mysql_password = ""
    mysql_db = ""

    class Config:
        extra = "ignore"