from typing import Generator

from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


def _create_engine_and_session():
    sqlalchemy_database_url = settings.DATABASE_URL

    # When using in-memory SQLite, we need StaticPool to share the same
    # in-memory database across all threads, and check_same_thread=False
    # to allow FastAPI's thread pool to access it.
    if sqlalchemy_database_url == "sqlite://":
        engine = create_engine(
            sqlalchemy_database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        # Configure secure database connection pooling for PostgreSQL
        engine = create_engine(
            sqlalchemy_database_url,
            # Connection pool settings for security and performance
            pool_size=20,  # Maximum number of connections in the pool
            max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
            pool_timeout=30,  # Timeout for getting a connection from the pool
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_pre_ping=True,  # Verify connections before using them
            # Security: Isolate connections per transaction
            isolation_level="READ COMMITTED",
        )

    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, session_local


engine, SessionLocal = _create_engine_and_session()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
