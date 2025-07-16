import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import save_query, get_query_history
from weather import fetch_weather

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            flash("City name cannot be empty!", "error")
            return redirect(url_for("index"))

        weather_data, error = fetch_weather(city)
        if error:
            flash(f"Could not retrieve weather data: {error}", "error")
            return redirect(url_for("index"))

        if weather_data:
            try:
                save_query(
                    city,
                    weather_data["temperature"],
                    weather_data["weather_description"],
                    weather_data["humidity"],
                    weather_data["wind_speed"],
                )
                flash(
                    f"Weather for {city}: {weather_data['temperature']}°C, "
                    f"{weather_data['weather_description']}",
                    "success",
                )
            except Exception as e:
                flash(f"Failed to save query to database: {e}", "error")
        else:
            flash(
                f"Could not find weather data for '{city}'. Please check the city name.",
                "error",
            )

        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/history")
def history():
    try:
        queries = get_query_history()
    except Exception as e:
        flash(f"Error fetching query history: {e}", "error")
        queries = []

    return render_template("history.html", queries=queries)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
