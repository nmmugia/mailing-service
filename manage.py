from flask.cli import FlaskGroup

from src import db, create_app, Config
from src.models import Event

import psycopg2


app = create_app()
cli = FlaskGroup(app)


@cli.command("init_database")
def init_database():
    try:
        # create database if not exist
        conn = psycopg2.connect(
            host=Config.DB_URL,
            database=Config.DB_USERNAME,
            user=Config.DB_USERNAME,
            password=Config.DB_PASSWORD
        )
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {Config.DB}")
        cur.close()
        conn.close()
    except Exception as e:
        print("Database Existed, skipped")
    try:
        db.drop_all()
        db.create_all()
        db.session.add_all([
            Event(event_name="KAA 2022"),
            Event(event_name="KAA 2010"),
        ])
        db.session.commit()
        print("database initiated")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    cli()