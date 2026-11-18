import os

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32).hex())

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30