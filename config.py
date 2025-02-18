import os

# Application configuration
class Config:
    # Security settings
    ALLOWED_IPS = {"212.154.17.173"}  # Set of allowed IP addresses
    MICROSOFT_FORM_URL = "https://forms.office.com/r/GuzVi8sZHN"
    
    # Flask configuration
    SECRET_KEY = os.environ.get("SESSION_SECRET", "default-secret-key")  # For production, use environment variable
    DEBUG = True
    
    # Logging configuration
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'DEBUG'
