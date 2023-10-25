from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from infrastructure.config import DB_URL

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Session:
    """
    Db session to be injected as Dependency in the different routes.
    This give you the freedom to switch between local and testing sessions to avoid use the current db for tests.

    Do not use if not as a dependency because otherwise the session will remain open!
    """
    db_session = SessionLocal()
    try:
        yield db_session
    except:
        db_session.rollback()
        raise
    finally:
        db_session.close()
