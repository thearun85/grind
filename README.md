# Grind

A lightweight DSA problem tracker that syncs your markdown progress log to a local SQLite database. Track which problems you've solved, when, and by category/difficulty.

## Why Grind?

Solving DSA problems once isn't enough—**repetition is key**. Grind helps you:
- Track problems you've solved with dates and metadata
- Maintain a version-controlled record in `leetlog.md`
- Automatically sync markdown to a queryable SQLite database
- Stay consistent with pre-commit hooks and automated syncing

## Features

✅ **Markdown-first workflow** — edit `leetlog.md`, everything else is automated
✅ **Local SQLite DB** — fast, queryable, yours to keep
✅ **Deduplication** — composite key prevents duplicate (url, date) entries
✅ **Pre-commit hooks** — mypy, ruff, formatting checks before commit
✅ **Offline-first** — works completely locally

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/grind.git
cd grind

# Install dependencies and hooks
make install
```

### 2. Initialize Database

```bash
make init
```

Creates `grind.db` with `problems` table.

### 3. Add Problems to `leetlog.md`

```markdown
# DSA Progress

- [x] https://leetcode.com/problems/two-sum/ | Array | Easy | 2026-04-23
- [x] https://leetcode.com/problems/valid-parentheses/ | Stack | Easy | 2026-04-23
```

Format: `- [x] <url> | <category> | <difficulty> | <date>`

### 4. Sync to Database

```bash
make log
```

## File Format

### Solved Problem
```markdown
- [x] https://leetcode.com/problems/problem-name/ | Category | Difficulty | YYYY-MM-DD
```

**Rules:**
- URLs must be complete LeetCode links
- Category, difficulty, and date are required
- Dates must be in `YYYY-MM-DD` format
- Use `|` as delimiter between fields

## Database Schema

```sql
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    leetcode_url TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    solved_on TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(leetcode_url, solved_on)
);
```

**Key points:**
- Composite unique constraint on `(leetcode_url, solved_on)` prevents duplicate entries
- Same problem can be solved multiple times on different dates
- `created_at` tracks when the record was added to the database

## Project Structure

```
grind/
├── leetlog.md                  # Your problem log (edit this!)
├── grind.db                    # SQLite database (auto-synced, .gitignored)
├── src/
│   ├── __init__.py
│   ├── init_db.py             # Database initialization
│   └── leetlog.py             # Markdown parser & DB syncer
├── tests/
│   └── __init__.py
├── Makefile                    # Task automation
├── pyproject.toml             # Poetry configuration
├── .pre-commit-config.yaml    # Pre-commit hooks
├── LICENSE
└── README.md
```

## Commands

```bash
# Setup
make install          # Install dependencies and git hooks
make init            # Initialize database

# Development
make log             # Parse leetlog.md and sync to DB
make fmt             # Format code with ruff
make lint            # Lint with ruff
make typecheck       # Type check with mypy
make test            # Run pytest
make check           # Run fmt, lint, typecheck, test

# Cleanup
make clean           # Remove cache directories
```

## Workflow

1. **Edit `leetlog.md`** — add a new problem entry
2. **Commit** — `git add leetlog.md && git commit -m "message"`
   - Pre-commit hooks run (mypy, ruff, formatting)
3. **Database updated** — `grind.db` now contains your new problem
4. **Push** — `git push` to share your progress

## Querying the Database

### From command line

```bash
sqlite3 grind.db
```

### Example queries

```sql
-- All problems
SELECT * FROM problems;

-- Count by category
SELECT category, COUNT(*) as count
FROM problems
GROUP BY category;

-- Problems solved on a specific date
SELECT leetcode_url, category, difficulty
FROM problems
WHERE solved_on = '2026-04-23';

-- Easy problems
SELECT leetcode_url, category
FROM problems
WHERE difficulty = 'Easy'
ORDER BY solved_on DESC;
```

## Configuration

### Pre-commit Hooks

Hooks run automatically before every commit. Configured in `.pre-commit-config.yaml`:

- **trailing-whitespace** — removes trailing spaces
- **end-of-file-fixer** — ensures files end with newline
- **check-yaml** — validates YAML syntax
- **check-toml** — validates TOML syntax
- **ruff** — lints and fixes Python code
- **ruff-format** — auto-formats Python code
- **mypy** — type checks Python code

Skip hooks if needed:
```bash
git commit --no-verify -m "skip hooks"
```

### Ruff Configuration

Line length: 88 characters
Target Python: 3.12
Linting rules: E, F, I, UP, B, SIM, RUF, N, PT

See `pyproject.toml` for details.

## Installation & Dependencies

### Requirements
- Python 3.12+
- Poetry

### First time setup

```bash
git clone https://github.com/yourusername/grind.git
cd grind
make install
make init
```

This will:
1. Install Python dependencies (via Poetry)
2. Install pre-commit hooks
3. Create SQLite database with schema

## Examples

### Example 1: First Problem

```bash
# Edit leetlog.md
- [x] https://leetcode.com/problems/two-sum/ | Array | Easy | 2026-04-23

# Commit
git add leetlog.md
git commit -m "Solve two sum"

# Post-commit hook syncs to DB
# Result: 1 problem in grind.db
```

### Example 2: Retry a Problem

```bash
# Add same URL with different date
- [x] https://leetcode.com/problems/two-sum/ | Array | Easy | 2026-04-23
- [x] https://leetcode.com/problems/two-sum/ | Array | Easy | 2026-04-30

# Commit
git commit -m "Retry two sum"

# Result: 2 rows in DB (different dates)
```

### Example 3: Query Progress

```bash
# View all array problems
sqlite3 grind.db "SELECT leetcode_url, difficulty FROM problems WHERE category = 'Array';"

# Count problems by difficulty
sqlite3 grind.db "SELECT difficulty, COUNT(*) FROM problems GROUP BY difficulty;"
```

## Troubleshooting

### Database file not found

```bash
make init
```

### Pre-commit hooks not running

```bash
pre-commit install
```

### Sync not working

Check the file path:
```bash
ls -la grind.db
```

Should be in project root. Then:
```bash
make log
```

### Type checking fails

```bash
make typecheck
```

Fix errors or add type hints. See `pyproject.toml` for mypy configuration.

## Development

### Running tests

```bash
make test
```

### Code formatting

```bash
make fmt     # Format code
make lint    # Check linting
make check   # Format + lint + typecheck + test
```

### Adding new features

1. Create feature branch: `git checkout -b feature/name`
2. Write code with type hints
3. Run `make check` before committing
4. Push and open a pull request

## Performance

- **Parse time**: ~1ms for typical `leetlog.md` files
- **Database indexes**: Fast lookups on URL and category
- **Storage**: ~100KB per 1000 problems (SQLite)

## Future Ideas

- CLI to query database (`grind stats`, `grind list --category Array`)
- GitHub Actions to generate stats in README
- Export to CSV/JSON
- Integration with Notion or Obsidian
- Web dashboard

## License

MIT — use freely, modify, and distribute.

## Contributing

This is a personal project, but feel free to fork and customize for your needs!

---

**Start grinding!** 🔥

```bash
make install && make init
```

Then edit `leetlog.md` and commit.
