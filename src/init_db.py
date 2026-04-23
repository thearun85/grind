import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DB_DIR = Path.cwd()
DB_PATH = DB_DIR / "grind.db"

def init_db() -> None:
    """create database and tables if they don't exist."""

    # Create directory
    DB_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"CWD is {Path.cwd()}")

    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Creates problems table 
    cursor.execute('''
        create table if not exists problems (
            id integer primary key autoincrement,
            leetcode_url text not null,
            category text not null,
            difficulty text not null,
            solved_on text not null,
            created_at text not null,
            unique(leetcode_url, solved_on)
        )'''
    )

    # Create index for faster queries
    cursor.execute('''
        create index if not exists idx_leetcode_url
        on problems(leetcode_url)
    ''')
    
    cursor.execute('''
        create index if not exists idx_category
        on problems(category)
    ''')

    conn.commit()
    conn.close()

    logger.info(f"Database initialised at {DB_PATH}")
    logger.info("Table 'problems' created")
    logger.info("Indices created for faster queries")
    
if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialise db: {e}")
        exit(1)
