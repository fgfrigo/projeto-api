import os

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ISSUER = os.getenv("JWT_ISSUER", "projeto-fer-ui")
DB_URL = os.getenv("DB_URL", "sqlite:///./app.db")

