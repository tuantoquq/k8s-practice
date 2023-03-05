from pydruid.client import *
from pydruid.utils.aggregators import *
from pydruid.utils.filters import Dimension
from Repository.userRepository import UserRepository
from Entity.entity import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends
from .utils import JWTUtils
from fastapi import HTTPException
from datetime import timedelta
from config import Settings
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer

reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )
class DruidService:
    def __init__(self, ):
        self.settings = Settings()
        self.query = PyDruid(self.settings.DRUID_BROKER, self.settings.DRUID_URL)

    async def load_ticker_data(self, start_date, end_date, ticker_table):
        self.query.topn(
            datasource=ticker_table,
            granularity="day",
            intervals=start_date + "/" + end_date,
            filter=Dimension("ticker") != "null",
            dimension="ticker",
            metric="high",
            aggregations={"high": longmax("high"),
                          "low": longmin("low"),
                          "open": stringfirst("open"),
                          "close": stringlast("close"),
                          "volume": longsum("volume")},
            threshold=2000
        )
        df = self.query.export_pandas().to_json(orient='records', date_format='iso')
        return df
