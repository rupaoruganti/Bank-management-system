# Bank Management — Project Report

## Project overview

This project simulates and manages a simple bank system. Core responsibilities include:

- Managing customers and accounts.
- Handling deposits, withdrawals and transfers.
- Maintaining transaction history.
- Enforcing business rules using stored procedures and triggers.
- Exporting database schema and data for backup or sharing.

## Key features

- Account and customer management (create/read/update/delete).
- Transaction processing with rollback on errors.
- Stored procedures for common operations.
- Triggers for automatic logging and constraints enforcement.
- Export/import utilities for schema and data.
- Sample complex queries used for reporting and analysis.

## Files explained (details)

- `database.py` — Central DB module. Wraps connection creation, query helpers, and (where implemented) schema initialization. Edit connection parameters here if you need to switch between SQLite, MySQL, or PostgreSQL.
- `bank.py` — Business logic; higher-level functions that call into `database.py` and stored procedures.
- `app.py` / `main.py` — Simple command-line entry points demonstrating usage (examples, sample flows).
- `export_database.py` — Produces SQL dumps and structure exports into `exports/`.
- SQL files (`*.sql`) — Contain schema, triggers, procedures and example complex queries. Use these to recreate the database schema on a supported SQL server.

## Assumptions and environment

- The project is written for Python 3.8+.
- The code expects a relational database. The project is written to be portable — `database.py` can be configured to use SQLite for local runs or a server DB (MySQL/Postgres) for full-featured runs. If you use a server DB, create a user and import the SQL scripts in this repo.
- If you change the DB backend, update connection parameters in `database.py` accordingly and re-run any initialization SQL.

If you want to run quickly and don't want to configure a DB server, try using SQLite (modify `database.py` to use `sqlite3` and a local file). The repository includes SQL scripts and Python wrappers that are compatible with typical SQL engines, but server-specific SQL (e.g., certain procedural syntax) may need small edits.

## Setup (quick)

1. Install Python 3.8 or later.
2. Create a virtual environment (recommended) and install any dependencies (if a `requirements.txt` exists, install from it). If not present, the project uses only the Python stdlib and the `sqlite3` module by default.

PowerShell example (from project root):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt # if present; otherwise skip
```

3. Edit `database.py` to configure your DB connection (SQLite file path or server credentials).
4. Initialize the database by running the SQL scripts (if using a server DB):

```powershell
# Example: run the SQL scripts using your DB client (pseudo-commands shown)
# mysql -u user -p < database_users.sql
# mysql -u user -p < database_triggers.sql
# mysql -u user -p < database_procedures.sql
# mysql -u user -p < complex_queries.sql
```

For SQLite, a minimal schema may be created by a script in `database.py` or by executing the SQL files through a SQLite client (some procedural SQL may not be supported by SQLite and should be adapted).

## Running the application

From the project root (PowerShell):

```powershell
# Activate virtualenv if created
.\.venv\Scripts\Activate.ps1

# Run the main application (choose the entry point you prefer)
python main.py
# or
python app.py
```

See top of `app.py` / `main.py` for example usage and available commands. If the application requires interactive inputs, it will prompt in the console.

## Exporting and backups

- Use `export_database.py` to export schema and data; produced files are placed in `exports/` with timestamps (see existing files there).
- Example:

```powershell
python export_database.py
# Look in the `exports/` folder for the generated SQL dumps.
```

## Testing

- See `TESTING_GUIDE.md` for the detailed manual testing plan and test cases. The project includes example scripts and SQL queries used during verification.
- Automated tests: none are included by default. Adding unit tests (pytest) for the logic in `bank.py` and integration tests for `database.py` is recommended.

## Known limitations & next steps

- DB portability: Stored procedures and triggers may be written for a specific RDBMS and could require adaptation for full SQLite compatibility.
- No automated test suite is included — adding unit and integration tests is a recommended improvement.
- Consider adding a `requirements.txt` and a small Docker Compose configuration for reproducible DB/server runs.

## Project reports and docs

- Detailed written report: `PROJECT_REPORT.md` and `PROJECT_REPORT_PART2.md` (analysis, ER diagrams, normalization discussion, sample outputs).
- Testing instructions: `TESTING_GUIDE.md`.
- Sharing/packaging: `SHARE_INSTRUCTIONS.md`.

## Authors / Attribution

- Project Author(s): see `PROJECT_REPORT.md` for the author list and institutional info.

## License

This repository does not include a license file. Add a `LICENSE` file if you intend to publish or distribute this project beyond the course.

---

If you want, I can:

- adapt the README to include exact Python dependencies (I can scan files to produce `requirements.txt`),
- create a small `requirements.txt` and a `run.ps1` script to streamline running in PowerShell,
- or produce a Docker Compose setup to run the DB and app together.

Tell me which of those you'd like and I'll add it.
