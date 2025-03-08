from pydantic_settings import BaseSettings
import os

class AlphaVantageConfig(BaseSettings):
    API_KEY:str=os.getenv('ALPHA_VANTAGE_API_KEY', "C8PNEUBK3E04F6H6")
alphaVantageConfig=AlphaVantageConfig()