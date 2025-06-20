import pandas as pd

def add_ema(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    指定した期間のEMAをDataFrameに追加する関数
    """
    df[f"ema_{period}"] = df["close"].ewm(span=period, adjust=False).mean()
    return df

def add_ema_slope(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    EMAと、その1本前との傾き（差分）を追加
    """
    ema_column = f"ema_{period}"
    slope_column = f"{ema_column}_slope"

    # EMAが未計算なら先に追加
    if ema_column not in df.columns:
        df = add_ema(df, period)

    # 傾き（1本前との差）を追加
    df[slope_column] = df[ema_column].diff()

    return df