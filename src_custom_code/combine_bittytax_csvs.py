import pandas as pd

et = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\etrade\bittytax.csv")
ft = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\freetrade\bittytax.csv")
ie = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\investengine\bittytax.csv")
t212 = pd.read_csv(r"C:\Projects\BittyTax\src_custom_code\data\t212\bittytax.csv")
pd.concat([et, ft, ie, t212]).sort_values(by="Timestamp").to_csv(
    r"bittytax_combined.csv", index=False
)
