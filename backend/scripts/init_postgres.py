import os
import subprocess
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import socket

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL not set in .env")

import re
match = re.match(r"postgresql://(.*?):(.*?)@(.+?):(\d+)/(.*)", DB_URL)
if not match:
    raise ValueError("DATABASE_URL format is invalid.")

user, password, host, port, dbname = match.groups()


def is_localhost(hostname: str):
    return hostname in ("localhost", "127.0.0.1", "::1")


def is_postgres_installed():
    try:
        subprocess.run(["psql", "--version"], check=True, stdout=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def try_start_postgres():
    cmds = [
        ["systemctl", "start", "postgresql"],
        ["service", "postgresql", "start"],
        ["pg_ctl", "start", "-D", "/usr/local/var/postgres"]
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True)
            print(f"Started PostgreSQL using: {' '.join(cmd)}")
            return True
        except subprocess.CalledProcessError:
            continue
    print("⚠️  Couldn't automatically start PostgreSQL. It might already be running.")


def ensure_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if DB exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        if not cur.fetchone():
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
            print(f"✅ Created database: {dbname}")
        else:
            print(f"✅ Database '{dbname}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to connect to or create DB: {e}")
        exit(1)


if is_localhost(host):
    print("🔍 Local database detected.")
    if not is_postgres_installed():
        print("❌ PostgreSQL is not installed. Please install it manually.")
        exit(1)
    try_start_postgres()
else:
    print(f"🌐 Remote database detected at {host} — skipping local checks.")

ensure_database()
