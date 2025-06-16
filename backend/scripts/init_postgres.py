import os
import subprocess
import re
import shutil
from dotenv import load_dotenv

load_dotenv()

DB_URL = str(os.getenv("DATABASE_URL")).rstrip("/")
if not DB_URL:
    raise ValueError("DATABASE_URL not set in .env")

pattern = re.compile(
    r"postgresql://(?P<user>.*?):(?P<password>.*?)@(?P<host>.+?):(?P<port>\d+)/(?P<dbname>.+)"
)
match = pattern.match(DB_URL)
if not match:
    raise ValueError("DATABASE_URL format is invalid.")

user = match["user"]
password = match["password"]
host = match["host"]
port = match["port"]
dbname = match["dbname"]


def is_localhost(hostname: str):
    return hostname in ("localhost", "127.0.0.1", "::1")


def is_postgres_installed():
    return shutil.which("psql") is not None


def try_install_postgres():
    print("PostgreSQL not found. Attempting to install...")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "postgresql", "postgresql-contrib"], check=True)
        print("PostgreSQL installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install PostgreSQL. Install it manually.")
        exit(1)


def try_start_postgres():
    cmds = [
        ["sudo", "systemctl", "start", "postgresql"],
        ["sudo", "service", "postgresql", "start"],
        ["pg_ctl", "start", "-D", "/usr/local/var/postgres"]
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Started PostgreSQL using: {' '.join(cmd)}")
            return
        except subprocess.CalledProcessError:
            continue
    print("Could not start PostgreSQL automatically. It might already be running.")


def run_sql_as_postgres(sql_cmd: str):
    try:
        result = subprocess.run(
            ["sudo", "-u", "postgres", "psql", "-tAc", sql_cmd],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running psql command: {sql_cmd}")
        print(e.stderr)
        exit(1)


def ensure_user_and_db():
    # Check if user exists
    user_exists = run_sql_as_postgres(f"SELECT 1 FROM pg_roles WHERE rolname='{user}'")
    if user_exists != "1":
        run_sql_as_postgres(f"CREATE USER {user} WITH PASSWORD '{password}';")
        print(f"Created DB user '{user}'")
    else:
        print(f"DB user '{user}' already exists")

    # Check if database exists
    db_exists = run_sql_as_postgres(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
    if db_exists != "1":
        run_sql_as_postgres(f"CREATE DATABASE {dbname} OWNER {user};")
        print(f"Created database '{dbname}' owned by '{user}'")
    else:
        print(f"Database '{dbname}' already exists")


if is_localhost(host):
    print("Local PostgreSQL detected.")
    if not is_postgres_installed():
        try_install_postgres()
    try_start_postgres()
    ensure_user_and_db()
else:
    print(f"Remote database detected at {host} — skipping local setup.")

print("Database check complete.")
