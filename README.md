# dormitory-report

A command-line tool that loads student and room data from JSON files into a PostgreSQL database and generates reports in JSON or XML format.

## Requirements

- Python 3.9+
- PostgreSQL

## Setup

1. Clone the repository
```bash
git clone <repo-url>
cd dormitory-report
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your database credentials
```
host=localhost
dbname=dormitory
user=your_user
password=your_password
```

5. Create the database in PostgreSQL
```sql
CREATE DATABASE dormitory;
```

## Usage

```bash
python main.py --rooms data/rooms.json --students data/students.json --extension json
```

### Arguments

| Argument | Required | Description |
|---|---|---|
| `--rooms` | Yes | Path to the rooms JSON file |
| `--students` | Yes | Path to the students JSON file |
| `--extension` | No | Output format: `json` or `xml` (default: `json`) |

## What it does

1. Connects to the PostgreSQL database
2. Creates the schema (tables + indexes) if it doesn't exist
3. Drops and recreates tables on each run to ensure clean data
4. Loads rooms first, then students (respecting the foreign key constraint)
5. Runs 4 reports against the database
6. Outputs results to `results/report.json` or `results/report.xml`

## Reports

- **Headcount** — number of students in each room
- **Lowest average age** — 5 rooms with the lowest average student age
- **Largest age difference** — 5 rooms with the biggest age gap between students
- **Mixed gender rooms** — rooms where students of both genders live

## Project Structure

```
dormitory-report/
│
├── data/
│   ├── students.json
│   └── rooms.json
│
├── db/
│   ├── connection.py       # DatabaseConnection class
│   ├── schema.py           # SchemaManager class
│   └── loader.py           # DataLoader class
│
├── reports/
│   └── runner.py           # ReportRunner class
│
├── output/
│   └── formatter.py        # Formatter class (JSON/XML)
│
├── results/                # Generated reports go here
├── main.py                 # CLI entry point
├── .env                    # Database credentials (not committed)
├── .gitignore
├── indexes.sql             # Index creation queries
└── requirements.txt
```

## Indexes

Indexes are created automatically on:
- `students.room_id` — used in every JOIN
- `students.birthday` — used in age calculations
