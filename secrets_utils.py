from dotenv import dotenv_values
import os

SECRET_FILE_NAME = 'secrets.env'

def get_secrets():
    """Get secrets with required keys"""
    required_keys = ["BASE_URL", "PRODUCT_TYPE1_TAB_NAME", "PRODUCT_TYPE2_TAB_NAME"]
    
    if not os.path.exists(SECRET_FILE_NAME):
        raise FileNotFoundError("Secrets file not found!")

    secrets = dotenv_values(SECRET_FILE_NAME)

    # Validate existence
    missing = [key for key in required_keys if key not in secrets]
    if missing:
        raise RuntimeError(f"CRITICAL: Missing secrets for keys: {', '.join(missing)}")

    # Validate non-empty values
    empty = [key for key in required_keys if secrets[key] == ""]
    if empty:
        raise ValueError(f"CRITICAL: Empty values for keys: {', '.join(empty)}")
    
    return secrets