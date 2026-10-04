"""Utility script to create all database tables using SQLAlchemy metadata.
It reads the configuration from app.core.config.Settings (which in turn reads .env).
Run it once after the database exists.
"""
import sys
from app.core.config import settings
from app.db import Base, engine

def main():
    try:
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
