from pathlib import Path

import pandas as pd
from numpy import nan


# For sales, fill the "Record Type" column with "Sell",
# fill in "Purchased Qty.", "Purchase Date", ahd "Purchase price".
# Fill them in the same as other rows, the extractor will auto flip.
def extract_from_et_export(etrade_data_path: Path, yahoo_usd_to_gbp_data_path: Path):
    print("NOTE: You have to manually enter sells for ETrade as they aren't exported")
    et = pd.read_excel(etrade_data_path)
    et = et.loc[et["Record Type"].isin(["Purchase", "Sell"])]
    et["Purchase Date"] = pd.to_datetime(et["Purchase Date"], format=r"%d-%b-%Y")
    usd_to_gbp = pd.read_csv(yahoo_usd_to_gbp_data_path)
    usd_to_gbp["USD to GBP avg on day"] = (usd_to_gbp["Open"] + usd_to_gbp["Close"]) / 2
    usd_to_gbp["Date"] = pd.to_datetime(usd_to_gbp["Date"], format=r"%Y-%m-%d")
    usd_to_gbp = usd_to_gbp.set_index("Date")
    add_indices = pd.Index(
        pd.date_range(usd_to_gbp.index.min(), usd_to_gbp.index.max())
    ).difference(usd_to_gbp.index)
    add_df = pd.DataFrame(index=add_indices, columns=usd_to_gbp.columns)
    usd_to_gbp = pd.concat([usd_to_gbp, add_df])
    usd_to_gbp = usd_to_gbp.sort_index()
    usd_to_gbp = usd_to_gbp.interpolate(method="index")
    # usd_to_gbp = usd_to_gbp.reindex(idx)
    et = et.merge(usd_to_gbp, left_on="Purchase Date", right_index=True, how="inner")
    df = pd.DataFrame(columns=["Type"])
    is_buy = et["Record Type"] == "Purchase"
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
    et["Total usd"] = et.loc[:, "Purchased Qty."] * et.loc[:, "Purchase Price"]
    et["Total"] = et["Total usd"] * et["USD to GBP avg on day"]
    df["Buy Quantity"] = et.loc[:, "Purchased Qty."].where(is_buy, et.loc[:, "Total"])
    df["Buy Asset"] = et.loc[:, "Symbol"].where(is_buy, "GBP")
    df["Buy Value in GBP"] = et.loc[:, "Total"].where(is_buy)
    df["Sell Quantity"] = et.loc[:, "Total"].where(is_buy, et.loc[:, "Purchased Qty."])
    # t212["Sell Asset"] = "GBP"
    df["Sell Asset"] = et.loc[:, "Symbol"].where(~is_buy, "GBP")
    df["Sell Value in GBP"] = et.loc[:, "Total"].where(~is_buy)
    df["Fee Quantity"] = None
    df["Fee Asset"] = None
    df["Fee Value in GBP"] = None
    df["Wallet"] = "ETrade"
    df["Timestamp"] = pd.to_datetime(et.loc[:, "Purchase Date"]).dt.strftime(r"%Y-%m-%d %H:%M:%S")
    df["Note"] = et.loc[:, "Symbol"]
    df["Type"] = "Trade"
    return df
    # Type	Buy Quantity	Buy Asset	Buy Value in GBP	Sell Quantity	Sell Asset	Sell Value in GBP	Fee Quantity	Fee Asset	Fee Value in GBP	Wallet	Timestamp	         Note
    # Trade	10	            BTC		    	                                GBP			           	                                                                2013-05-24 20:17:40


def extract_from_et_exports(paths: list[Path], yahoo_usd_to_gbp_data_path: Path):
    df = pd.concat([extract_from_et_export(p, yahoo_usd_to_gbp_data_path) for p in paths])
    p = paths[0]
    df.to_csv(p.parent / ("bittytax.csv"), index=False)


if __name__ == "__main__":
    extract_from_et_exports(
        [
            Path(
                r"C:\Projects\BittyTax\src_custom_code\data\etrade\BenefitHistory_with_sells.xlsx"
            ),
        ],
        Path(r"C:\Projects\BittyTax\src_custom_code\data\etrade\GBP=X.csv"),
    )
