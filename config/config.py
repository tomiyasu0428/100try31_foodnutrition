# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env ファイルから環境変数を読み込む


class Config:
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    GEMINI_API_ENDPOINT = os.environ.get("GEMINI_API_ENDPOINT")
    NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
    NUTRITIONIX_APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
    NUTRITIONIX_AUTH_ENDPOINT = os.environ.get("NUTRITIONIX_AUTH_ENDPOINT")
    NUTRITIONIX_NATURAL_NUTRIENTS_ENDPOINT = os.environ.get("NUTRITIONIX_NATURAL_NUTRIENTS_ENDPOINT")
