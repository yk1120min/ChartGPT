from data_fetch.twelvedata_api import fetch_data
from data_process.dataframe_utils import format_dataframe
from indicators.SMA import add_sma
from indicators.SMA import add_sma_slope
from ai.gpt_signal import get_trade_signal
from notify.email_notifier import send_email_notification
from indicators.EMA import add_ema
from indicators.EMA import add_ema_slope
from indicators.MACD import add_macd
from indicators.RSI import add_rsi



# 取得する時間足のリスト型(中身はタプル型)
pairs = [("15min", 200), ("1h", 200), ("4h", 200)]
multi_df={}

#データを取得
for interval,outputsize in pairs:
    json_data = fetch_data(symbol="USD/JPY", interval=interval, outputsize=outputsize)

    if json_data:
        # 取得したデータをDataFrameへ整形
        df = format_dataframe(json_data)

        #SMAと傾きを追加
        #df = add_sma(df, period=20)
        #df = add_sma(df, period=50)
        #df = add_sma(df, period=100)
        #df = add_sma_slope(df, period=20)
        #df = add_sma_slope(df, period=50)
        #df = add_sma_slope(df, period=100)

        #EMAと傾きを追加
        df = add_ema(df, period=20)
        df = add_ema(df, period=50)
        df = add_ema_slope(df, period=20)
        df = add_ema_slope(df, period=50)

        #MACDを追加
        df = add_macd(df, short_period=12, long_period=26, signal_period=9)

        #RSIを追加
        add_rsi(df, period=14)


        multi_df[interval] = df

    else:
        print(f" {interval} データ取得失敗")

#画面出力確認用
#for interval, df in multi_df.items():
#    print(f"\n=== {interval} の最新5本 ===")
#    print(df.tail(5))        

#CSV出力確認用
for interval, df in multi_df.items():
    filename = f"data/usd_jpy_{interval}.csv"
    df.to_csv(filename, index=False)

#AI戦略判断を実施
body = get_trade_signal(multi_df)

#分析結果をメール送信
send_email_notification("AI分析",body)


