import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
from dotenv import load_dotenv  # dotenvをインポート

# .envファイルの読み込み
load_dotenv(dotenv_path="../.env")  # .envファイルがルートディレクトリにある場合

# Flaskアプリケーションの設定
app = Flask(__name__)
CORS(app)  # フロントエンドとバックエンド間でCORSを許可

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate_reply", methods=["POST"])
def generate_reply():
    try:
        data = request.json
        review_text = data.get("review", "")
        if not review_text:
            return jsonify({"error": "口コミが入力されていません。"}), 400

        # ChatGPT APIを呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは親切でプロフェッショナルなラーメン屋のスタッフです。"},
                {"role": "user", "content": f"口コミ: {review_text}"}
            ],
            max_tokens=100,
        )

        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
