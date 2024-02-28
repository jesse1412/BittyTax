from pathlib import Path

import pandas as pd


def extract_from_ft_export(p: Path):
    ft = pd.read_csv(p)
    ft = ft.loc[ft["Buy / Sell"].isin(["BUY", "SELL"])]
    df = pd.DataFrame(columns=["Type"])
    is_buy = ft["Buy / Sell"] == "BUY"
    # Market buy -> Buy asset = Ticker,
    #               Buy Quantity = No. of shares.
    #               Sell asset = GBP.
    #               Sell quantity = Price
    #               Buy Value in GBP = Price
    #               Sell Value in GBP = NULL
    # Market sell ->Buy asset = GBP,
    #               Buy Quantity = Price.
    #               Sell asset = Ticker.
    #               Sell quantity = No. of shares
    #               Buy Value in GBP = NULL
    #               Sell Value in GBP = Price
    df["Buy Quantity"] = ft.loc[:, "Quantity"].where(is_buy, ft.loc[:, "Total Amount"])
    df["Type"] = "Trade"
    df["Buy Asset"] = ft.loc[:, "ISIN"].where(is_buy, "GBP")
    df["Buy Value in GBP"] = ft.loc[:, "Total Amount"].where(is_buy)
    df["Sell Quantity"] = ft.loc[:, "Total Amount"].where(is_buy, ft.loc[:, "Quantity"])
    # t212["Sell Asset"] = "GBP"
    df["Sell Asset"] = ft.loc[:, "ISIN"].where(~is_buy, "GBP")
    df["Sell Value in GBP"] = ft.loc[:, "Total Amount"].where(~is_buy)
    df["Fee Quantity"] = None
    df["Fee Asset"] = None
    df["Fee Value in GBP"] = None
    df["Wallet"] = "FreeTrade"
    df["Timestamp"] = pd.to_datetime(ft.loc[:, "Timestamp"]).dt.strftime(r"%Y-%m-%d %H:%M:%S")
    df["Note"] = ft.loc[:, "Ticker"]
    return df
    # Type	Buy Quantity	Buy Asset	Buy Value in GBP	Sell Quantity	Sell Asset	Sell Value in GBP	Fee Quantity	Fee Asset	Fee Value in GBP	Wallet	Timestamp	         Note
    # Trade	10	            BTC		    	                                GBP			           	                                                                2013-05-24 20:17:40


def extract_from_ft_exports(paths: list[Path]):
    df = pd.concat([extract_from_ft_export(p) for p in paths])
    p = paths[0]
    df.to_csv(p.parent / ("bittytax.csv"), index=False)


if __name__ == "__main__":
    extract_from_ft_exports(
        [
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\freetrade\activity-feed-export_c0c5c84c-0626-45c5-89bd-eba15c2ea7ea.csv"
            ),
        ]
    )
