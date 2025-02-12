# app.py
from flask import Flask, render_template, request, redirect, flash
from utils import image_processing, gemini_api, nutrition_api
from config.config import Config
from urllib.parse import quote
import logging
import requests

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.FLASK_SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            flash("ファイルが選択されていません")
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            flash("ファイルが選択されていません")
            return redirect(request.url)
        if file:
            try:
                logger.debug("画像の前処理を開始")
                # 画像の前処理（リサイズ等）
                processed_image = image_processing.preprocess_image(file)
                
                logger.debug("Gemini APIによる食品認識を開始")
                # geminiAPI で食品認識を実施し、英語の食品名を取得
                food_text_en = gemini_api.recognize_food_text(processed_image)
                logger.debug(f"認識結果 (英語): {food_text_en}")
                
                if not food_text_en:
                    flash("食品の認識に失敗しました。")
                    return render_template("index.html", nutrition_results=None)
                
                # 英語の食品名を使用してNutritionix APIで栄養情報を取得
                logger.debug(f"Nutritionix APIで栄養情報を取得: {food_text_en}")
                nutrition_results = nutrition_api.get_nutrition_info(food_text_en)
                logger.debug(f"栄養情報取得結果: {nutrition_results}")
                
                if nutrition_results:
                    # 日本語の食品名を取得
                    food_text_ja = get_japanese_food_name(food_text_en)
                    return render_template(
                        "index.html",
                        nutrition_results=nutrition_results,
                        recognized_food_en=food_text_en,
                        recognized_food_ja=food_text_ja
                    )
                else:
                    flash("栄養情報の取得に失敗しました。")
                    return render_template("index.html", nutrition_results=None)
                    
            except Exception as e:
                logger.error(f"エラーが発生しました: {str(e)}", exc_info=True)
                flash(f"エラーが発生しました: {str(e)}")
                return render_template("index.html", nutrition_results=None)
                
    return render_template("index.html", nutrition_results=None)


def get_japanese_food_name(food_text_en):
    """
    英語の食品名から日本語の食品名を取得
    """
    try:
        # Gemini APIを使用して翻訳
        prompt = f"Translate this food name to Japanese (return ONLY the Japanese name): {food_text_en}"
        translation_data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 100
            }
        }
        
        url = f"{Config.GEMINI_API_ENDPOINT}?key={Config.GEMINI_API_KEY}"
        response = requests.post(
            url,
            json=translation_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        return food_text_en  # 翻訳に失敗した場合は英語をそのまま返す
        
    except Exception as e:
        logger.error(f"翻訳エラー: {str(e)}")
        return food_text_en  # エラーの場合は英語をそのまま返す


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
