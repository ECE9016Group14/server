import datetime

from fastapi import Query
from typing import List, Dict
from fastapi import APIRouter
from fastapi.params import Depends

from app.services.cryptocurrencies_service import CryptoCurrenciesService
from src.app.models.response import CommRes, CommResCode
import os
crypto_currencies_router = APIRouter(prefix="/crypto-currencies", tags=["Crypto Currencies"])
router = crypto_currencies_router

@router.get("/query_physical_currencies", response_model=CommRes[List[Dict[str,str]]], summary="", description="")
async def query_physical_currencies(service:CryptoCurrenciesService=Depends()):
    physical_data_path='src/resources/physical_currency_list.csv'
    physical_data=service.read_csv_currency_file(physical_data_path)
    return CommRes(data=physical_data)

@router.get("/query_digital_currencies", response_model=CommRes[List[Dict[str,str]]], summary="", description="")
async def query_digital_currencies(service:CryptoCurrenciesService=Depends()):
    digital_data_path='src/resources/digital_currency_list.csv'
    digital_data=service.read_csv_currency_file(digital_data_path)
    return CommRes(data=digital_data)

@router.get("/exchange-rate/query", response_model=CommRes[Dict], summary="", description="")
async def query_exchange_rate(from_currency: str = Query('BTC', description=""),to_currency: str = Query('USD', description=""),service:CryptoCurrenciesService=Depends()):
        data=await service.query_exchange_rate(from_currency,to_currency)
        if data and data.get("Error Message")==None:
            return CommRes(data=data)
        return CommRes(errorcode=CommResCode.FAIL, msg="Invalid currency pair")

@router.get("/fx-daily",response_model=CommRes[Dict], summary="", description="")
async def get_fx_daily(
    from_symbol: str = Query('EUR', description="The base currency symbol (e.g., EUR)"),
    to_symbol: str = Query("USD", description="The target currency symbol (e.g., USD)"),
    start_date: datetime.datetime = Query(datetime.datetime.strptime('2024-06-02', "%Y-%m-%d"), description="The start date of the time series"),
    end_date: datetime.datetime = Query(datetime.datetime.now().date(), description="The end date of the time series"),
    service:CryptoCurrenciesService=Depends()
):
    data=await service.get_fx_daily(from_symbol,to_symbol,start_date,end_date)
    return CommRes(data=data)

@router.get("/fx-weekly",response_model=CommRes[Dict], summary="", description="")
async def get_fx_weekly(
    from_symbol: str = Query('EUR', description="The base currency symbol (e.g., EUR)"),
    to_symbol: str = Query("USD", description="The target currency symbol (e.g., USD)"),
    start_date: datetime.datetime = Query(datetime.datetime.strptime('2023-12-02', "%Y-%m-%d"), description="The start date of the time series"),
    end_date: datetime.datetime = Query(datetime.datetime.now().date(), description="The end date of the time series"),
    service:CryptoCurrenciesService=Depends()
):
    data=await service.get_fx_weekly(from_symbol,to_symbol,start_date,end_date)
    return CommRes(data=data)
@router.get("/fx-monthly",response_model=CommRes[Dict], summary="", description="")
async def get_fx_monthly(
    from_symbol: str = Query('EUR', description="The base currency symbol (e.g., EUR)"),
    to_symbol: str = Query("USD", description="The target currency symbol (e.g., USD)"),
    start_date: datetime.datetime = Query(datetime.datetime.strptime('2023-12-30', "%Y-%m-%d"), description="The start date of the time series"),
    end_date: datetime.datetime = Query(datetime.datetime.now().date(), description="The end date of the time series"),
    service:CryptoCurrenciesService=Depends()
):
    data=await service.get_fx_monthly(from_symbol,to_symbol,start_date,end_date)
    return CommRes(data=data)

