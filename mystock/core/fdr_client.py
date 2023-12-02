import FinanceDataReader as fdr
import pandas as pd


class StockFdr:
    @classmethod
    def stock_listing(cls, market_name: str) -> pd.DataFrame:
        return fdr.StockListing(market_name)
