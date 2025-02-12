# utils/nutrition_api.py
import requests
import logging
from config.config import Config

logger = logging.getLogger(__name__)

def get_nutrition_info(query):
    """
    Nutritionix APIを使用して食品の栄養情報を取得し、整理して返します。
    
    :param query: 検索する食品名（英語）
    :return: 整理された栄養情報の辞書、もしくはNone
    """
    try:
        headers = {
            'x-app-id': Config.NUTRITIONIX_APP_ID,
            'x-app-key': Config.NUTRITIONIX_API_KEY,
            'Content-Type': 'application/json'
        }
        
        data = {
            "query": query,
            "timezone": "Asia/Tokyo"
        }
        
        logger.debug(f"Nutritionix API request headers: {headers}")
        logger.debug(f"Nutritionix API request data: {data}")
        
        response = requests.post(
            "https://trackapi.nutritionix.com/v2/natural/nutrients",
            headers=headers,
            json=data
        )
        
        logger.debug(f"Nutritionix API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Nutritionix API error: {response.text}")
            return None
            
        result = response.json()
        logger.debug(f"Nutritionix API response: {result}")
        
        if 'foods' not in result or not result['foods']:
            logger.warning("No foods found in response")
            return None
            
        # 最初の食品の栄養情報を取得
        food = result['foods'][0]
        
        # 栄養情報を整理して日本語で返す
        nutrition_info = {
            "基本情報": {
                "食品名（英語）": food.get('food_name', '不明'),
                "分量": f"{food.get('serving_qty', 0)} {food.get('serving_unit', '')}",
                "重さ": f"{food.get('serving_weight_grams', 0)}g"
            },
            "主要栄養素": {
                "カロリー": f"{food.get('nf_calories', 0)}kcal",
                "タンパク質": f"{food.get('nf_protein', 0)}g",
                "脂質": f"{food.get('nf_total_fat', 0)}g",
                "炭水化物": f"{food.get('nf_total_carbohydrate', 0)}g"
            },
            "詳細栄養素": {
                "食物繊維": f"{food.get('nf_dietary_fiber', 0)}g",
                "糖質": f"{food.get('nf_sugars', 0)}g",
                "コレステロール": f"{food.get('nf_cholesterol', 0)}mg",
                "ナトリウム": f"{food.get('nf_sodium', 0)}mg"
            },
            "ビタミン・ミネラル": {
                "カリウム": f"{food.get('nf_potassium', 0)}mg",
                "鉄分": f"{food.get('nf_iron_dv', 0)}%",
                "カルシウム": f"{food.get('nf_calcium_dv', 0)}%",
                "ビタミンA": f"{food.get('nf_vitamin_a_dv', 0)}%",
                "ビタミンC": f"{food.get('nf_vitamin_c_dv', 0)}%"
            }
        }
        
        return nutrition_info
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None
