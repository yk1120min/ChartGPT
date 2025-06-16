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
        "1day": "1日足(長期)"
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
    以下の3つの時間足（15分足・1時間足・1日足）の価格データとテクニカル指標に基づいて、USD/JPYの今後の戦略判断を行ってください。

    【あなたの役割】
    - デイトレードにおいて10〜50pipsの値幅を狙う短〜中期の戦略を立てること
    - 各時間足のSMA（20, 50, 100）の方向・位置関係・傾きからトレンドを分析すること
    - 各ローソク足（open, high, low, close）からプライスアクション（陽線/陰線・ヒゲ・包み足など）の兆候を読み取ること
    - 短期・中期・長期の整合性を見て、マルチタイムフレームで最適な売買判断をすること

    【出力形式】
    1. 判断（買い／売り／様子見）のいずれかを**1つに絞って**明示
    2. 根拠（各時間足の分析と整合性に基づいて、なぜその判断か）
    3. エントリーポイントの仮説（目安となるタイミングや水準の例）
    4. リスク要因（逆行した場合の懸念）

    【各カラムの説明】
    - datetime: 日時
    - open: 始値
    - high: 高値
    - low: 安値
    - close: 終値
    - sma_20: 直近20本の単純移動平均
    - sma_50: 直近50本の移動平均
    - sma_100: 直近100本の移動平均
    - sma_20_slope: sma_20の傾き（前の値との差）
    - sma_50_slope: sma_50の傾き（前の値との差）
    - sma_100_slope: sma_100の傾き（前の値との差）

    【データ】
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