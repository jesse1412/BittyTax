import pandas as pd

et = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\etrade\bittytax.csv")
ft = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\freetrade\bittytax.csv")
ie = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\investengine\bittytax.csv")
t212 = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\t212\bittytax.csv")
nm = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\nutmeg\bittytax.csv")
bn = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\coinbase\bittytax.csv")

use_future_planning = True
if use_future_planning:
    futures = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\future_plans_bittytax.csv")
    all = pd.concat([et, ft, ie, t212, nm, bn, futures]).sort_values(by="Timestamp")
else:
    all = pd.concat([et, ft, ie, t212, nm, bn]).sort_values(by="Timestamp")
all["Fee Quantity"] = 0
all["Fee Asset"] = "GBP"
all.to_csv(r"bittytax_combined.csv", index=False)
