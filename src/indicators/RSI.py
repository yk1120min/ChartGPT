import pandas as pd

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    RSIを計算してDataFrameに追加
    """
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss

    #RSI(相場の買われすぎ/売られすぎを判断する)
    df[f"rsi_{period}"] = 100 - (100 / (1 + rs))

    return df

##メモ
#.clipはdataframeクラスの関数で、値を指定した範囲に収める。
#