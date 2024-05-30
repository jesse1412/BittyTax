Usage: Get the data from relevant brokers, then run the relevant extract scripts. Combine those extracted csvs with the combining script.

For ETrade, you have to add sells manually, and remove the "totals" line. You'll also need the Yahoo Finance USD/GBP pairing https://finance.yahoo.com/quote/GBP=X/

For coinbase, just add your new transactions manually (in the bittytax file). It's all weird and messed up.

Finally use BittyTax (`pipx install BittyTax`, `bittytax "path"`)
