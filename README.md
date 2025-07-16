# Weather App

A Flask-based web application that allows users to fetch current weather information for cities using the OpenWeatherMap API and stores query history in a PostgreSQL database.

## Features

- Search current weather by city name.
- Display temperature, weather description, humidity, and wind speed.
- Persist weather query history in a PostgreSQL database.
- View past queries with timestamps.
- Dockerized for easy deployment and development.

## Prerequisites

- Docker and Docker Compose installed on your machine.
- An [OpenWeatherMap API key](https://openweathermap.org/api).
- Git (optional, to clone this repository).

## Getting Started

### 1. Clone the Repository

```bash
git clone 
cd 
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATABASE_URL=postgresql://weather_user:sin@db:5432/weather_db
```

- **OPENWEATHER_API_KEY**: Required to access OpenWeatherMap API.
- **DATABASE_URL**: Connection string for PostgreSQL database.
- **FLASK_SECRET_KEY**: Used by Flask for sessions and security. Defaults to a random key if not set.

### 3. Build and Run the Application with Docker Compose

```bash
docker-compose up --build
```

This command will:
- Spin up a PostgreSQL container initialized with the schema.
- Build and launch the Flask web app container.
- Map ports `5432` for PostgreSQL and `5000` for Flask app.

### 4. Access the Application

Open your browser and go to:

[http://localhost:5000](http://localhost:5000)

You can:

- Enter a city name to fetch current weather.
- View query history via the "History" page.

## Project Structure

```
.
├── app.py                 # Flask application code, interaction between modules
├── models.py              # handles external API logic only
├── weather.py             # handles database connection and queries
├── Dockerfile             # Dockerfile for Flask app container
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── schema.sql             # SQL schema for PostgreSQL
├── .env                   # Environment variables file (not tracked by Git)
├── .gitignore             # Git ignore rules
├── README.md              # This README file
├── templates/             # HTML templates (index.html, history.html)
└── static/                # Static assets (if any)
```


## Environment Variables Detail

| Variable           | Description                                   | Required         |
|--------------------|-----------------------------------------------|------------------|
| `OPENWEATHER_API_KEY` | API key for OpenWeatherMap service           | Yes              |
| `DATABASE_URL`        | PostgreSQL connection URL                     | Yes              |

## Notes

- The database password is currently set to `sin` (in both `.env` and `docker-compose.yml`). Change this if deploying in production.
- Flask app runs in development mode by default (`debug=True` in `app.py`). Disable debug mode and set a secure secret key in production.
