from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}?driver={os.getenv('DB_DRIVER')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask and JWT configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'fallback_flask_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_jwt_secret_key')
