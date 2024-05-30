from pathlib import Path

import pandas as pd


def extract_from_nutmeg_export(p: Path):
    nm = pd.read_csv(p)
    nm = nm.loc[nm["Description"].isin(["Sale", "Purchase"])]
    nm["Asset Code"] = nm["Asset Code"].replace({"EMIM": "IE00BKM4GZ66"})
    df = pd.DataFrame(columns=["Type"])
    is_buy = nm["Description"] == "Purchase"
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
    df["Buy Quantity"] = nm.loc[:, "No. Shares"].where(is_buy, nm.loc[:, "Share Price (£)"])
    df["Type"] = "Trade"
    df["Buy Asset"] = nm.loc[:, "Asset Code"].where(is_buy, "GBP")
    df["Buy Value in GBP"] = nm.loc[:, "Total Value (£)"].where(is_buy)
    df["Sell Quantity"] = nm.loc[:, "Total Value (£)"].where(is_buy, nm.loc[:, "No. Shares"])
    # t212["Sell Asset"] = "GBP"
    df["Sell Asset"] = nm.loc[:, "Asset Code"].where(~is_buy, "GBP")
    df["Sell Value in GBP"] = nm.loc[:, "Total Value (£)"].where(~is_buy)
    df["Fee Quantity"] = None
    df["Fee Asset"] = None
    df["Fee Value in GBP"] = None
    df["Wallet"] = "Nutmeg"
    df["Timestamp"] = nm.loc[:, "Date"]
    df["Note"] = nm.loc[:, "Asset Code"]
    return df
    # Type	Buy Quantity	Buy Asset	Buy Value in GBP	Sell Quantity	Sell Asset	Sell Value in GBP	Fee Quantity	Fee Asset	Fee Value in GBP	Wallet	Timestamp	         Note
    # Trade	10	            BTC		    	                                GBP			           	                                                                2013-05-24 20:17:40


def extract_from_nutmeg_exports(paths: list[Path]):
    df = pd.concat([extract_from_nutmeg_export(p) for p in paths])
    p = paths[0]
    df.to_csv(p.parent / ("bittytax.csv"), index=False)


if __name__ == "__main__":
    extract_from_nutmeg_exports(
        [
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\nutmeg\Investment-Activity-22-Sept-2023.csv"
            ),
        ]
    )
