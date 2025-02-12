# 栄養分析×食品画像アプリ

このプロジェクトは、アップロードされた食品画像から geminiAPI を利用して食品を認識し、その結果を基に Nutritionix API で栄養情報を取得するシンプルな Web アプリです。

## セットアップ

1. リポジトリをクローンする
2. `pip install -r requirements.txt` で依存ライブラリをインストールする
3. `.env` ファイルに必要な環境変数を設定する
4. `python app.py` でアプリを起動する

## 環境変数 (.env)

- `FLASK_SECRET_KEY`: Flask のシークレットキー
- `GEMINI_API_KEY`: geminiAPI の API キー
- `GEMINI_API_ENDPOINT`: geminiAPI のエンドポイント URL
- `NUTRITIONIX_API_KEY`: Nutritionix API の API キー
- `NUTRITIONIX_AUTH_ENDPOINT`: Nutritionix 認証エンドポイント URL
- `NUTRITIONIX_NATURAL_NUTRIENTS_ENDPOINT`: Nutritionix の /v2/natural/nutrients エンドポイント URL
