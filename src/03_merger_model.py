import argparse
import pandas as pd
import numpy as np
import os

def build_accretion_dilution(acq_path, tgt_path, cash_pct, stock_pct, synergies, year):
    # Load data
    acquirer = pd.read_csv(acq_path).iloc[0]
    target = pd.read_csv(tgt_path).iloc[0]
    
    # Convert to numeric values
    deal_value = target["Shares_out_mm"] * 1e6 * target["Share_price"]
    cash_used = deal_value * cash_pct
    shares_issued = (deal_value * stock_pct) / acquirer["Current_price"]
    
    # EPS calculations
    pre_acq_eps = (acquirer["Net_income_2024_USD_m"] * 1e6) / (acquirer["Shares_out_mm"] * 1e6)
    pro_net = (acquirer["Net_income_2024_USD_m"] + target["Net_income_2024_USD_m"]) * 1e6 + synergies * 1e6
    pro_shares = acquirer["Shares_out_mm"] * 1e6 + shares_issued
    pro_eps = pro_net / pro_shares
    
    # Accretion/dilution
    accretion = (pro_eps / pre_acq_eps) - 1
    
    return pd.DataFrame({
        "Metric": ["Pre-Deal EPS", "Pro-Forma EPS", "Accretion/(Dilution) %"],
        "Value": [pre_acq_eps, pro_eps, accretion * 100]
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merger Model")
    parser.add_argument("--acquirer", required=True, help="Path to acquirer facts CSV")
    parser.add_argument("--target", required=True, help="Path to target facts CSV")
    parser.add_argument("--cash_pct", type=float, default=0.60)
    parser.add_argument("--stock_pct", type=float, default=0.40)
    parser.add_argument("--synergies", type=float, default=75.0)
    parser.add_argument("--deal_year", type=int, default=2025)
    parser.add_argument("--output", required=True, help="Output Excel file")
    args = parser.parse_args()

    model = build_accretion_dilution(
        args.acquirer,
        args.target,
        cash_pct=args.cash_pct,
        stock_pct=args.stock_pct,
        synergies=args.synergies,
        year=args.deal_year
    )

    mode = 'a' if os.path.exists(args.output) else 'w'
    with pd.ExcelWriter(args.output, engine='openpyxl', mode=mode) as writer:
        model.to_excel(writer, sheet_name="Merger_Model", index=False)
    
    print(f"✅ Merger model appended to {args.output}")