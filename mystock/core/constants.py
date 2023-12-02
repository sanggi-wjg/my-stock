from django.db import models

MARKET_TYPE_STOCK = "STOCK"
MARKET_TYPE_INDEX = "INDEX"

MARKETS = [
    # 마켓
    ("KOSPI", MARKET_TYPE_STOCK),
    ("KOSDAQ", MARKET_TYPE_STOCK),
    # ("S&P500", 0),
    # ("NASDAQ", 0),
    # 한국
    ("KS11", MARKET_TYPE_INDEX),  # KOSPI
    ("KS100", MARKET_TYPE_INDEX),  # KOSPI 100
    ("KS200", MARKET_TYPE_INDEX),  # KOSPI 200
    ("KQ11", MARKET_TYPE_INDEX),  # KOSDAQ
    # 미국
    ("IXIC", MARKET_TYPE_INDEX),  # NASDAQ
    ("VIX", MARKET_TYPE_INDEX),  # 변동성 지수 (Greed And Fear)
    # 환율
    ("USD/KRW", MARKET_TYPE_INDEX),
    # 선물
    ("CL=F", MARKET_TYPE_INDEX),  # WTI
    ("NG=F", MARKET_TYPE_INDEX),  # 천연 가스
    ("GC=F", MARKET_TYPE_INDEX),  # 금
    ("SI=F", MARKET_TYPE_INDEX),  # 은
    ("HG=f", MARKET_TYPE_INDEX),  # 구리
]
