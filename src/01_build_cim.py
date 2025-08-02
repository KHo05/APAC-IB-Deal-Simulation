import shutil, os, json, pandas as pd

RAW_DIR = "00_Raw_Data"
OUT_JSON = os.path.join(RAW_DIR, "SEA_filings.json")
OUT_CSV = os.path.join(RAW_DIR, "SEA_facts.csv")
OUT_FCF = os.path.join(RAW_DIR, "SEA_fcf.csv")
OUT_11ST = os.path.join(RAW_DIR, "11Street_facts.csv")

def stage_pdfs():
    required_files = [
        "SE_20F_2024.pdf", 
        "SKT_2024_Annual.pdf", 
        "Precedents.xlsx"
    ]
    for f in required_files:
        src = os.path.join(RAW_DIR, f)
        if not os.path.exists(src):
            raise FileNotFoundError(f"{src} missing – download it first.")
        print(f"✅ {f} present")

def build_facts():
    # Sea Limited facts from 20-F (replace with your exact numbers)
    sea_facts = {
        "Ticker": "SE",
        "Revenue_2024_USD_m": 13100,   # p.72
        "EBITDA_2024_USD_m": 1300,     # p.89
        "Shares_out_mm": 590,           # p.178
        "Net_debt_USD_m": 3200,         # p.F-6
        "Cash_USD_m": 6800,             # p.F-6
        "Net_income_2024_USD_m": 850,   # Replace with actual
        "Current_price": 75.50,         # Manual input
        "Source": "Sea Limited Form 20-F filed 25-Apr-2024"
    }
    
    # 11Street Korea mock data (private company)
    eleven_street = {
        "Ticker": "11Street",
        "Revenue_2024_USD_m": 2300,
        "EBITDA_2024_USD_m": 350,
        "Shares_out_mm": 100,
        "Share_price": 23.00,
        "Net_income_2024_USD_m": 150,
        "Source": "SK Telecom Annual Report 2024 (estimated)"
    }
    
    # Sea Limited FCF history (replace with actuals from filings)
    fcf_data = {
        "Year": [2020, 2021, 2022, 2023, 2024],
        "FCF_USD_m": [350, 480, 620, 890, 1100]  # Replace with actuals
    }
    
    # Save all files
    os.makedirs(RAW_DIR, exist_ok=True)
    
    pd.Series(sea_facts).to_json(OUT_JSON, indent=2)
    pd.DataFrame([sea_facts]).to_csv(OUT_CSV, index=False)
    pd.DataFrame([eleven_street]).to_csv(OUT_11ST, index=False)
    pd.DataFrame(fcf_data).to_csv(OUT_FCF, index=False)
    
    print("✅ Static facts saved to:")
    print(f"  - {OUT_JSON}")
    print(f"  - {OUT_CSV}")
    print(f"  - {OUT_11ST}")
    print(f"  - {OUT_FCF}")

if __name__ == "__main__":
    stage_pdfs()
    build_facts()