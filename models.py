import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        current_app.logger.error(f"Failed to connect to database: {e}")
        raise


def save_query(city, temperature, weather_description, humidity, wind_speed):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO queries 
            (city_name, temperature, weather_description, humidity, wind_speed) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (city, temperature, weather_description, humidity, wind_speed),
        )
        conn.commit()
    except psycopg2.Error as e:
        current_app.logger.error(f"Database error saving query: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_query_history():
    conn = None
    cur = None
    queries = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT city_name, temperature, weather_description, humidity, wind_speed, timestamp
            FROM queries
            ORDER BY timestamp DESC
            """
        )
        queries = cur.fetchall()
    except psycopg2.Error as e:
        current_app.logger.error(f"Database error fetching history: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return queries
