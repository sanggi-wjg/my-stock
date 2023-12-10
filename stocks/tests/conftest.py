import pytest
import pandas as pd


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
