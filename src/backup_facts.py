import pandas as pd
# Manual inputs from 20-F / Annual Report
facts = {
    "Ticker": ["SE"],
    "Revenue_2024": [13.1e9],        # USD
    "EBITDA_2024": [1.3e9],
    "Shares_out": [590e6],
    "Net_debt": [3.2e9],
    "Cash": [6.8e9]
}
pd.DataFrame(facts).to_csv("00_Raw_Data/SEA_facts.csv", index=False)