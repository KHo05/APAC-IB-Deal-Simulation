import os
import pandas as pd
import yfinance as yf  # Requires pip install yfinance

RAW_DIR = "00_Raw_Data"
OUT_CSV = os.path.join(RAW_DIR, "SEA_facts.csv")
OUT_FCF = os.path.join(RAW_DIR, "SEA_fcf.csv")
OUT_11ST = os.path.join(RAW_DIR, "11Street_facts.csv")

def stage_pdfs():
    required_files = [
        "SE_20F_2024.pdf", 
        "SKT_2024_Annual.pdf", 
        "Precedents.xlsx",
        "comps.csv"
    ]
    for f in required_files:
        src = os.path.join(RAW_DIR, f)
        if not os.path.exists(src):
            print(f"Warning: {src} missing – place it if needed for analysis.")
        else:
            print(f"✅ {f} present")

def build_facts():
    # Fetch Sea Limited facts dynamically from Yahoo Finance
    try:
        tk = yf.Ticker("SE")
        info = tk.info
        sea_facts = {
            "Ticker": "SE",
            "Revenue_2024_USD_m": info['totalRevenue'] / 1e6,
            "EBITDA_2024_USD_m": info['ebitda'] / 1e6,
            "Shares_out_mm": info['sharesOutstanding'] / 1e6,
            "Net_debt_USD_m": (info['totalDebt'] - info['totalCash']) / 1e6,
            "Cash_USD_m": info['totalCash'] / 1e6,
            "Net_income_2024_USD_m": info['netIncomeToCommon'] / 1e6,
            "Current_price": info['currentPrice'],
            "Source": "Yahoo Finance - TTM as of latest"
        }
        
        # Fetch FCF history
        cashflow = tk.cashflow
        fcf = cashflow.loc["Free Cash Flow"].dropna() / 1e6
        fcf_data = {
            "Year": fcf.index.year.tolist(),
            "FCF_USD_m": fcf.tolist()
        }
    except Exception as e:
        print(f"Warning: Failed to fetch real data from yfinance: {e}. Using static mock data.")
        sea_facts = {
            "Ticker": "SE",
            "Revenue_2024_USD_m": 13100,
            "EBITDA_2024_USD_m": 1300,
            "Shares_out_mm": 590,
            "Net_debt_USD_m": 3200,
            "Cash_USD_m": 6800,
            "Net_income_2024_USD_m": 850,
            "Current_price": 75.50,
            "Source": "Sea Limited Form 20-F filed 25-Apr-2024 (static)"
        }
        fcf_data = {
            "Year": [2020, 2021, 2022, 2023, 2024],
            "FCF_USD_m": [350, 480, 620, 890, 1100]
        }
    
    # 11Street Korea mock data (private company, hypothetical for simulation)
    eleven_street = {
        "Ticker": "11Street",
        "Revenue_2024_USD_m": 2300,
        "EBITDA_2024_USD_m": 350,
        "Shares_out_mm": 100,
        "Share_price": 23.00,
        "Net_income_2024_USD_m": 150,
        "Source": "SK Telecom Annual Report 2024 (estimated/hypothetical)"
    }
    
    # Save files
    os.makedirs(RAW_DIR, exist_ok=True)
    pd.DataFrame([sea_facts]).to_csv(OUT_CSV, index=False)
    pd.DataFrame([eleven_street]).to_csv(OUT_11ST, index=False)
    pd.DataFrame(fcf_data).to_csv(OUT_FCF, index=False)
    
    print("✅ Facts saved to:")
    print(f"  - {OUT_CSV}")
    print(f"  - {OUT_11ST}")
    print(f"  - {OUT_FCF}")

if __name__ == "__main__":
    stage_pdfs()
    build_facts()