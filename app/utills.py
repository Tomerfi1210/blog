from dotenv import load_dotenv
import os


load_dotenv()

def get_access_token_expire_minutes():
    return int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
