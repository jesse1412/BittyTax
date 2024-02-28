from pathlib import Path

import pandas as pd


def extract_from_ie_export(p: Path):
    ie = pd.read_csv(p, header=1)
    ie = ie.loc[ie["Transaction Type"].isin(["Buy", "Sell"])]
    ie[["Note", "ISIN"]] = ie["Security / ISIN"].str.split(" / ", expand=True, n=1)
    ie["ISIN"] = ie["ISIN"].str.removeprefix("ISIN ")
    df = pd.DataFrame(columns=["Type"])
    is_buy = ie["Transaction Type"] == "Buy"
    ie.loc[:, "Total Trade Value"] = ie.loc[:, "Total Trade Value"].str.removeprefix("£")
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
    df["Buy Quantity"] = ie.loc[:, "Quantity"].where(is_buy, ie.loc[:, "Total Trade Value"])
    df["Type"] = "Trade"
    df["Buy Asset"] = ie.loc[:, "ISIN"].where(is_buy, "GBP")
    df["Buy Value in GBP"] = ie.loc[:, "Total Trade Value"].where(is_buy)
    df["Sell Quantity"] = ie.loc[:, "Total Trade Value"].where(is_buy, ie.loc[:, "Quantity"])
    # t212["Sell Asset"] = "GBP"
    df["Sell Asset"] = ie.loc[:, "ISIN"].where(~is_buy, "GBP")
    df["Sell Value in GBP"] = ie.loc[:, "Total Trade Value"].where(~is_buy)
    df["Fee Quantity"] = None
    df["Fee Asset"] = None
    df["Fee Value in GBP"] = None
    df["Wallet"] = "IE"
    df["Timestamp"] = pd.to_datetime(ie.loc[:, "Trade Date/Time"]).dt.strftime(r"%Y-%m-%d %H:%M:%S")
    df["Note"] = ie.loc[:, "Note"]
    return df
    # Type	Buy Quantity	Buy Asset	Buy Value in GBP	Sell Quantity	Sell Asset	Sell Value in GBP	Fee Quantity	Fee Asset	Fee Value in GBP	Wallet	Timestamp	         Note
    # Trade	10	            BTC		    	                                GBP			           	                                                                2013-05-24 20:17:40


def extract_from_ie_exports(paths: list[Path]):
    df = pd.concat([extract_from_ie_export(p) for p in paths])
    p = paths[0]
    df.to_csv(p.parent / ("bittytax.csv"), index=False)


if __name__ == "__main__":
    extract_from_ie_exports(
        [
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\investengine\Trading_statement_26_Feb_2020_to_26_Feb_2024.csv"
            ),
        ]
    )
