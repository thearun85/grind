import logging
from pathlib import Path
import sqlite3
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

DB_PATH = Path.cwd() / "grind.db"
MARKDOWN_FILE = Path("leetlog.md")

def parse_log(md_file: Path) -> list[dict[str, str]]:
    """
    Parse leetlog.md format:
    - [x] <url> | <category> | <difficulty> | <date>
    """
    problems = []
    with open(md_file, 'r') as f:
        for line in f:
            # Skips headers and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse problem lines
            if line.startswith('- [x]'):
                content = line[5:].strip()
                parts = [p.strip() for p in content.split('|')]
                if len(parts) >= 4:
                    problems.append({
                        'leetcode_url': parts[0],
                        'category': parts[1],
                        'difficulty': parts[2],
                        'solved_on': parts[3],
                    })
        return problems

def insert_problems(problems: list[dict[str, str]]) -> None:
    """Insert problems into database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted = skipped = 0
    for problem in problems:
        try:
            cursor.execute('''
                insert into problems
                (leetcode_url, category, difficulty, solved_on, created_at)
                values (?, ?, ?, ?, ?)
            ''', (
                problem['leetcode_url'],
                problem['category'],
                problem['difficulty'],
                problem['solved_on'],
                datetime.now().isoformat()
            ))
            inserted+=1

        except sqlite3.IntegrityError:
            # URL already exists for the date
            skipped+=1
    conn.commit()
    conn.close()

    logger.info(f"Inserted {inserted} problems")
    
if __name__ == '__main__':
    try:
        problems = parse_log(MARKDOWN_FILE)
        logger.info(f"Length of leetcode.md file is {len(problems)}")
        insert_problems(problems)
    except Exception as e:
        logger.error(f"Leetlog processing failed: {e}")
        exit(1)
    
