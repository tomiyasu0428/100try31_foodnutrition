# utils/gemini_api.py
import os
import base64
import requests
import logging
from config.config import Config

# ロギングの設定
logger = logging.getLogger(__name__)

def recognize_food_text(image_data):
    """
    geminiAPI を利用して画像から食品を認識し、
    自然言語の食品名（例："Grilled Chicken Breast"）を返します。

    :param image_data: 前処理済みの画像バイトデータ
    :return: 認識結果の食品名（文字列）または None
    """
    try:
        # Base64エンコード
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # リクエストデータの構築
        request_data = {
            "contents": [{
                "parts": [
                    {
                        "text": "Look at this food image and tell me what it is in English. Return ONLY the food name, nothing else. For example: 'Grilled Chicken Breast' or 'Caesar Salad'"
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_b64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 1,
                "maxOutputTokens": 100
            }
        }

        # APIキーをURLパラメータとして追加
        url = f"{Config.GEMINI_API_ENDPOINT}?key={Config.GEMINI_API_KEY}"
        
        logger.debug(f"Gemini API URL: {url}")
        logger.debug("Sending request to Gemini API...")
        
        response = requests.post(
            url,
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        if response.status_code != 200:
            logger.error(f"API error response: {response.text}")
            return None
            
        data = response.json()
        logger.debug(f"API response data: {data}")
        
        # レスポンスから食品名を抽出
        if "candidates" in data and len(data["candidates"]) > 0:
            food_name = data["candidates"][0]["content"]["parts"][0]["text"]
            # 余分な記号や空白を削除
            food_name = food_name.strip().strip('"').strip("'")
            logger.debug(f"Extracted food name: {food_name}")
            return food_name
        else:
            logger.warning("No candidates found in response")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return None
