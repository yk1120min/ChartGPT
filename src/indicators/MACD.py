import pandas as pd

def add_macd(df: pd.DataFrame, short_period: int = 12, long_period: int = 26, signal_period: int = 9) -> pd.DataFrame:
    """
    MACDを計算してDataFrameに追加
    """

    # EMAの算出
    ema_short = df["close"].ewm(span=short_period, adjust=False).mean()
    ema_long = df["close"].ewm(span=long_period, adjust=False).mean()

    # MACDライン(勢いを確認)
    df["macd_line"] = ema_short - ema_long

    # シグナルライン()
    df["signal_line"] = df["macd_line"].ewm(span=signal_period, adjust=False).mean()

    # ヒストグラム（MACDライン - シグナルライン）
    df["macd_hist"] = df["macd_line"] - df["signal_line"]

    return df