from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    mongo_url = ""
    rpc_url = ""
    
    class Config:
        extra = "ignore"