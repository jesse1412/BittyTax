from pathlib import Path

import pandas as pd


def extract_from_t212_export(p: Path):
    t212 = pd.read_csv(p)
    t212 = t212.loc[t212["Action"].isin(["Market buy", "Market sell"])]
    df = pd.DataFrame(columns=["Type"])
    is_buy = t212["Action"] == "Market buy"
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
    df["Buy Quantity"] = t212.loc[:, "No. of shares"].where(is_buy, t212.loc[:, "Total"])
    df["Type"] = "Trade"
    df["Buy Asset"] = t212.loc[:, "ISIN"].where(is_buy, "GBP")
    df["Buy Value in GBP"] = t212.loc[:, "Total"].where(is_buy)
    df["Sell Quantity"] = t212.loc[:, "Total"].where(is_buy, t212.loc[:, "No. of shares"])
    # t212["Sell Asset"] = "GBP"
    df["Sell Asset"] = t212.loc[:, "ISIN"].where(~is_buy, "GBP")
    df["Sell Value in GBP"] = t212.loc[:, "Total"].where(~is_buy)
    df["Fee Quantity"] = None
    df["Fee Asset"] = None
    df["Fee Value in GBP"] = None
    df["Wallet"] = "T212"
    df["Timestamp"] = t212.loc[:, "Time"]
    df["Note"] = t212.loc[:, "Ticker"]
    return df
    # Type	Buy Quantity	Buy Asset	Buy Value in GBP	Sell Quantity	Sell Asset	Sell Value in GBP	Fee Quantity	Fee Asset	Fee Value in GBP	Wallet	Timestamp	         Note
    # Trade	10	            BTC		    	                                GBP			           	                                                                2013-05-24 20:17:40


def extract_from_t212_exports(paths: list[Path]):
    df = pd.concat([extract_from_t212_export(p) for p in paths])
    p = paths[0]
    df.to_csv(p.parent / ("bittytax.csv"), index=False)


if __name__ == "__main__":
    extract_from_t212_exports(
        [
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\t212\from_2022-01-02_to_2023-01-01_MTcwODk3Mzc5NTcyNA.csv"
            ),
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\t212\from_2023-01-02_to_2024-01-01_MTcwODk3MzgzNDUzNw.csv"
            ),
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\t212\from_2024-01-02_to_2024-02-26_MTcwODk3Mzg1Nzk5MQ.csv"
            ),
        ]
    )
