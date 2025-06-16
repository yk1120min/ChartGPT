import pandas as pd

def format_dataframe(json_data: dict) -> pd.DataFrame:
    """
    JSON形式のローソク足データを整形し、pandasのDataFrameとして返す
    
    """
    # "values" 部分を取り出して DataFrame 化
    df = pd.DataFrame(json_data['values'])

    # datetime列を日時型に変換し、昇順に並び替え
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime')

    # open/high/low/close を float に変換
    for col in ['open', 'high', 'low', 'close']:
        df[col] = pd.to_numeric(df[col])

    return df