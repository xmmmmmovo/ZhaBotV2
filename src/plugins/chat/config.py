from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    openai_email: str
    openai_password: str
    openai_api_key: str
    openai_session_token: str

    class Config:
        extra = "ignore"
