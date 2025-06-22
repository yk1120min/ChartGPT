from openai import OpenAI
import pandas as pd
from config import OPENAI_API_KEY
import json

# OpenAIクライアント初期化
client = OpenAI(api_key=OPENAI_API_KEY)

def get_trade_signal(multi_df: dict[str, pd.DataFrame]) -> str:
    """
    複数時間足のDataFrameからトレード戦略を生成する（ChatGPTに依頼）

    :param multi_df: 時間足をキー、DataFrameを値にした辞書
    :return: ChatGPTからの助言（買い/売り/様子見 など）
    """

    # 日本語ラベルに変換
    interval_labels = {
        "15min": "15分足(短期)",
        "1h": "1時間足(中期)",
        "1day": "4時間足(長期)"
    }

    parts = []
    for interval, df in multi_df.items():
        interval_label = interval_labels.get(interval, interval)

        latest_data = df.to_dict(orient="records")
        formatted_data = json.dumps(latest_data, indent=2, ensure_ascii=False, default=str)
        
        # プロンプトの一部を構築
        part_prompt = f"""

        ▼{interval_label}:
        {formatted_data}
        """
        parts.append(part_prompt.strip())

    full_prompt = """

あなたはプロのFXトレーダーです。
以下の3つの時間足（15分足、1時間足、4時間足）の価格データとテクニカル指標に基づいて、USD/JPYの今後の戦略判断を行ってください。
目的はデイトレードで約20〜50pipsの利益を狙う短〜中期の戦略を構築することです。
マルチタイムフレーム分析により、各時間足の整合性から最適なエントリー判断を行ってください。

【各時間足の役割と分析基準】

- 4時間足：
    - 大局のトレンドを把握するために使用
    - 使用指標：EMA20、EMA50
    - EMAの傾き、クロス、ローソク足との位置関係から上昇・下降トレンドを判断

- 1時間足：
    - 押し目買い／戻り売りのタイミングを見極める主軸の時間足として使用
    - 使用指標：EMA20、EMA50、MACD、RSI
    - EMAへの接触・反発、MACDのクロスや方向性、RSIの水準を確認

- 15分足：
    - エントリータイミングの精度を上げるために使用
    - 使用指標：EMA20、EMA50、MACD、RSI
    - 短期トレンドの転換点（EMAクロス、MACDヒストグラム反転、RSIの水準など）を確認

【出力形式】

    1. 戦略判断（買い／売り／様子見 のいずれかを1つに絞って提示）
    2. 根拠の解説（各時間足毎に簡潔に説明）
    3. エントリーポイントの仮説（どの水準でどのシグナルが出れば仕掛けるか）※様子見なら不要
    4. リスク要因と撤退基準（逆行した場合の対応や損切り条件） ※様子見なら不要

【データカラムの説明】

    - datetime：日時
    - open：始値
    - high：高値
    - low：安値
    - close：終値
    - ema_20：指数移動平均線（20本）
    - ema_50：指数移動平均線（50本）
    - ema_20_slope：ema_20の傾き（前との差）
    - ema_50_slope：ema_50の傾き（前との差）
    - macd_line：MACDライン（12EMAと26EMAの差）
    - signal_line：MACDのシグナルライン（9期間EMA）
    - macd_hist：MACDヒストグラム（macd_lineとsignal_lineの差）
    - rsi_14：RSI（14期間、70超で買われすぎ、30未満で売られすぎ）


    【JSON形式のデータ】
    """ + "\n\n".join(parts)

    #print(full_prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "あなたはプロのFXトレーダーです。"},
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ ChatGPT呼び出し失敗: {e}")
        return "エラー"