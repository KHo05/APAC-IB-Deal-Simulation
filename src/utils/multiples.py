import pandas as pd

def comps_frame(comps_path):
    """Load pre-prepared comps data from CSV"""
    return pd.read_csv(comps_path)