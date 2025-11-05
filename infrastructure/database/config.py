from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class DatabaseSettings(BaseSettings):
    """Configuración de la base de datos"""
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 3306))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "helpdeskpro")
    
    @property
    def database_url(self) -> str:
        """Genera la URL de conexión a la base de datos"""
        if self.db_password:
            return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        else:
            return f"mysql+pymysql://{self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}"


# Configuración de la base de datos
db_settings = DatabaseSettings()
engine = create_engine(
    db_settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Generador de sesiones de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

