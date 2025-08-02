import yfinance as yf, pandas as pd, numpy as np

def dcf_model(ticker, r, g):
    tk = yf.Ticker(ticker)
    fcf = tk.cashflow.loc["Free Cash Flow"].sort_index().dropna()
    fcf = fcf[fcf.index >= 2020]
    proj = pd.Series([fcf.iloc[-1]*(1.15)**(i+1) for i in range(5)], index=range(2025,2030))
    tv = proj.iloc[-1]*(1+g)/(r-g)
    pv = (proj / (1+r)**np.arange(1,6)).sum() + tv/(1+r)**5
    out = pd.DataFrame({"FCF": proj, "PV": proj/(1+r)**np.arange(1,6)})
    out.loc["Terminal Value"] = [tv, tv/(1+r)**5]
    out.loc["Enterprise Value"] = [None, pv]
    return out