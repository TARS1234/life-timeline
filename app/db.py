import logging
from sqlmodel import SQLModel, create_engine, Session

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///data/timeline.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)
    _migrate_db()


def _migrate_db():
    """Tiny helper: adds new columns to existing milestone table without dropping data."""
    import sqlite3
    db_path = "data/timeline.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(milestone)")
        cols = {row[1] for row in cursor.fetchall()}

        if "parent_id" not in cols:
            cursor.execute("ALTER TABLE milestone ADD COLUMN parent_id INTEGER")
            logger.info("[_migrate_db] Added parent_id column to milestone")

        if "end_date" not in cols:
            cursor.execute("ALTER TABLE milestone ADD COLUMN end_date DATE")
            logger.info("[_migrate_db] Added end_date column to milestone")

        if "color" not in cols:
            cursor.execute("ALTER TABLE milestone ADD COLUMN color TEXT")
            logger.info("[_migrate_db] Added color column to milestone")

        if "notes" not in cols:
            cursor.execute("ALTER TABLE milestone ADD COLUMN notes TEXT")
            logger.info("[_migrate_db] Added notes column to milestone")

        conn.commit()
        conn.close()
        logger.info("[_migrate_db] Migration complete")
    except Exception as e:
        logger.error(f"[_migrate_db ERROR] Migration failed: {e}")
        raise


def get_session():
    with Session(engine) as session:
        yield session
