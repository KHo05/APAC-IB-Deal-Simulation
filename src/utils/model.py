import yfinance as yf, pandas as pd, numpy as np

def build_accretion_dilution(acq, tgt, cash_pct, stock_pct, synergies, year):
    a = yf.Ticker(acq).info
    t = {"shares": 100e6, "net_income": 150e6, "share_price": 23}  # mock 11Street
    deal_value = t["shares"] * t["share_price"]
    cash_used = deal_value * cash_pct
    shares_issued = (deal_value * stock_pct) / a["currentPrice"]

    pre_acq_eps = a["netIncomeToCommon"] / a["sharesOutstanding"]
    pro_net = a["netIncomeToCommon"] + t["net_income"] + synergies
    pro_shares = a["sharesOutstanding"] + shares_issued
    pro_eps = pro_net / pro_shares
    accretion = (pro_eps / pre_acq_eps) - 1
    return pd.DataFrame({
        "Metric": ["Pre-Deal EPS", "Pro-Forma EPS", "Accretion %"],
        "Value": [pre_acq_eps, pro_eps, accretion*100]
    })