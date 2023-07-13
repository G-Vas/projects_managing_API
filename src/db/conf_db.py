from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.conf import DATABASE_URL


engine = create_engine(str(DATABASE_URL))
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
