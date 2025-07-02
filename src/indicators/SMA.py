import pandas as pd

def add_sma(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    指定された期間の単純移動平均（SMA）をDataFrameに追加する関数
    """
    df[f"sma_{period}"] = df["close"].rolling(window=period).mean()

    return df

def add_sma_slope(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    SMAと、その1本前との傾き（差分）を追加
    """
    sma_colums = f"sma_{period}"
    slope_colums = f"{sma_colums}_slope"

    # SMAが未計算なら先に追加
    if sma_colums not in df.columns:
        df = add_sma(df, period)

    # 傾き（1本前との差）を追加
    df[slope_colums] = df[sma_colums].diff()

    return df

##メモ
#rolling()は移動ウィンドウの処理を行うDataframeクラスの関数
#f"”文字列は中の変数が展開される