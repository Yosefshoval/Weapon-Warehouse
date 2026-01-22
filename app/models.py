import pandas as pd


def risk_level_categoy(df: pd.DataFrame):
    df['level_risk'] = pd.cut(
        df['km_range'], 
        bins=[0, 20, 100, 300, float('inf')], 
        labels=['low', 'medium', 'high', 'extreme']
        )
    return df
    


def repalce_none_values(df: pd.DataFrame, replacement_value):
    df['manufacturer'].fillna(replacement_value, inplace=True)
    return df

