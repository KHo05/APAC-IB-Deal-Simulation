import argparse
import pandas as pd
import numpy as np
import os

def dcf_model(fcf_path, r, g):
    fcf = pd.read_csv(fcf_path)
    last_fcf = fcf.iloc[-1]["FCF_USD_m"] * 1e6  # Convert millions to actual USD
    
    # Projections (5 years at 15% CAGR as per simulation)
    proj_years = [2025, 2026, 2027, 2028, 2029]
    proj = [last_fcf * (1.15)**(i+1) for i in range(5)]
    
    # Terminal value
    tv = proj[-1] * (1 + g) / (r - g)
    
    # Present values
    pv_proj = [cf / (1+r)**(i+1) for i, cf in enumerate(proj)]
    pv_tv = tv / (1+r)**5
    
    # Build output
    out = pd.DataFrame({
        "Year": proj_years + ["Terminal Value", "Enterprise Value"],
        "FCF": proj + [tv, None],
        "PV": pv_proj + [pv_tv, sum(pv_proj) + pv_tv]
    }).set_index("Year")
    
    return out

def comps_frame(comps_path):
    if not os.path.exists(comps_path):
        raise FileNotFoundError(f"Comps file missing: {comps_path}")
    return pd.read_csv(comps_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Valuation Model")
    parser.add_argument("--comps", required=True, help="Path to comps CSV")
    parser.add_argument("--precedents", default="00_Raw_Data/Precedents.xlsx", help="Path to precedents Excel")
    parser.add_argument("--fcf", required=True, help="Path to FCF CSV")
    parser.add_argument("--discount_rate", type=float, default=0.115)
    parser.add_argument("--perp_growth", type=float, default=0.03)
    parser.add_argument("--output", required=True, help="Output Excel file")
    args = parser.parse_args()

    comps = comps_frame(args.comps)
    precedents = pd.read_excel(args.precedents) if os.path.exists(args.precedents) else pd.DataFrame()
    dcf = dcf_model(args.fcf, args.discount_rate, args.perp_growth)

    with pd.ExcelWriter(args.output, engine='openpyxl') as writer:
        comps.to_excel(writer, sheet_name="Trading_Comps", index=False)
        precedents.to_excel(writer, sheet_name="Precedent_Trans", index=False)
        dcf.to_excel(writer, sheet_name="DCF")
    
    print(f"✅ Valuation saved to {args.output}")