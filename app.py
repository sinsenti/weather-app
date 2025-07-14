import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import psycopg2
from dotenv import load_dotenv
# from datetime import datetime

load_dotenv()

app = Flask(__name__)
# In production generate  random key and store it securely.
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY not set in .env or environment variables.")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env or environment variables.")


def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        app.logger.error(f"Failed to connect to database: {e}")
        raise


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"].strip()
        if not city:
            flash("City name cannot be empty!", "error")
            return redirect(url_for("index"))

        try:
            params = {
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            }
            response = requests.get(OPENWEATHER_API_URL, params=params)
            response.raise_for_status()
            weather_data = response.json()

            if weather_data.get("cod") == 200:
                main_info = weather_data.get("main", {})
                weather_details = weather_data.get("weather", [{}])[0]

                temperature = main_info.get("temp")
                weather_description = weather_details.get("description")
                humidity = main_info.get("humidity")
                wind_speed = weather_data.get("wind", {}).get("speed")

                conn = None
                try:
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO queries (city_name, temperature, weather_description, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s)",
                        (city, temperature, weather_description, humidity, wind_speed),
                    )
                    conn.commit()
                    flash(
                        f"Weather for {city}: {temperature}°C, {weather_description}",
                        "success",
                    )
                except psycopg2.Error as db_err:
                    flash(f"Database error saving query: {db_err}", "error")
                    app.logger.error(f"Database error: {db_err}")
                finally:
                    if cur:
                        cur.close()
                    if conn:
                        conn.close()
                return redirect(url_for("index"))
            else:
                flash(
                    f"Could not find weather data for '{city}'. Please check the city name.",
                    "error",
                )

        except requests.exceptions.RequestException as e:
            flash(f"Error fetching weather data: {e}", "error")
            app.logger.error(f"OpenWeatherMap API error: {e}")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "error")
            app.logger.error(f"Unexpected error: {e}")

    return render_template("index.html")


@app.route("/history")
def history():
    queries = []
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT city_name, temperature, weather_description, humidity, wind_speed, timestamp FROM queries ORDER BY timestamp DESC"
        )
        queries = cur.fetchall()
    except psycopg2.Error as e:
        flash(f"Error fetching query history: {e}", "error")
        app.logger.error(f"Database error fetching history: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return render_template("history.html", queries=queries)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
