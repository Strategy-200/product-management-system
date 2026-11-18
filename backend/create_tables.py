from database.database import Base, engine
from models.user import User
from models.product import Product
from models import user
from models import revoked_token

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")