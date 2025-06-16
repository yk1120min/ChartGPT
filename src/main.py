from data_fetch.twelvedata_api import fetch_data
from data_process.dataframe_utils import format_dataframe
from indicators.moving_average import add_sma
from indicators.moving_average import add_sma_slope
from ai.gpt_signal import get_trade_signal
from notify.email_notifier import send_email_notification


# 取得する時間足のリスト
pairs = [("15min", 200), ("1h", 200), ("1day", 200)]
multi_df={}

#データを取得
for interval,outputsize in pairs:
    #print(f"\n=== {interval} データ取得中 ===")
    json_data = fetch_data(symbol="USD/JPY", interval=interval, outputsize=outputsize)

    if json_data:
        # 取得したデータをDataFrameへ整形
        df = format_dataframe(json_data)

        # テクニカル指標追加（SMAと傾き）
        df = add_sma(df, period=20)
        df = add_sma(df, period=50)
        df = add_sma(df, period=100)
        df = add_sma_slope(df, period=20)
        df = add_sma_slope(df, period=50)
        df = add_sma_slope(df, period=100)

        multi_df[interval] = df

    else:
        print(f" {interval} データ取得失敗")


# AI戦略判断を実施（SMA情報含めて渡す）
body = get_trade_signal(multi_df)

send_email_notification("AI分析",body)


