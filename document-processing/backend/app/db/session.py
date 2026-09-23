from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import get_settings


settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
