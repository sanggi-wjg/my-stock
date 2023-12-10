import pytest
import pandas as pd

from stocks.models import Stock, StockTypeEnum


@pytest.fixture(autouse=True)
def mock_fake_stock_listing(mocker):
    mocker.patch(
        "mystock.core.fdr_client.StockFdr.stock_listing",
        return_value=pd.DataFrame(
            [
                ["005930", "삼성전자"],
                ["373220", "LG에너지솔루션"],
            ],
            columns=["Code", "Name"],
        ),
    )


@pytest.fixture
def stock_fixture():
    stock = Stock(
        market="KOSPI",
        type=StockTypeEnum.STOCK,
        code="005930",
        name="삼성전자",
    )
    stock.save()
    return stock


@pytest.fixture
def stock_index_fixture():
    stock = Stock(
        market="INDEX",
        type=StockTypeEnum.INDEX,
        code="KS11",
        name="KOSPI",
    )
    stock.save()
    return stock
