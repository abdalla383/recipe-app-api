import time
import psycopg2
from psycopg2 import OperationalError


def wait_for_db():
    print("Waiting for database...")
    db_up = False
    while not db_up:
        try:
            conn = psycopg2.connect(
                dbname="dev_db",
                user="dev_user",
                password="changeme",
                host="db"
            )
            conn.close()  # Properly close the connection
            db_up = True
        except OperationalError:
            print("Database unavailable, waiting 1 second...")
            time.sleep(1)
    print("Database available!")


if __name__ == '__main__':
    wait_for_db()
