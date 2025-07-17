# Weather Query Flask App

A Flask web application that allows users to query current weather information for any city using the OpenWeatherMap API, and stores the query history in a PostgreSQL database.

## Features

- Search for current weather by city name.
- Display weather info: temperature, description, humidity, wind speed.
- Backend built with Flask, PostgreSQL, and OpenWeatherMap API.
- Fully dockerized for easy setup and deployment.
- Automated testing with pytest.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- An [OpenWeatherMap API Key](https://openweathermap.org/api).

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:sinsenti/weather-app.git
cd  weather-app
```

### 2. Create `.env` file

Create a `.env` file in the root directory with your environment variables for API and database access:

```env
OPENWEATHER_API_KEY=your_openweather_api_key_here
DATABASE_URL=postgresql://weather_user:sin@db:5432/weather_db
```

 **Note:** Make sure `DATABASE_URL` matches the credentials in `docker-compose.yml`.

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

- This command builds your app image and starts the PostgreSQL and Flask containers.
- Database schema is initialized automatically when the DB container starts.

### 4. Access the Application

Open your browser and visit:

[http://localhost:5000](http://localhost:5000)

- Use the input form on the homepage to search weather by city.
- Visit `/history` to see the saved query history.

## Project Structure

```
.
├── app.py                 # Flask application & routes
├── models.py              # Database connection and queries
├── weather.py             # Weather API integration
├── Dockerfile             # Defines the Flask app container image
├── docker-compose.yml     # Docker Compose config for app + DB
├── requirements.txt       # Python dependencies
├── schema.sql             # Database schema initialization
├── .env                   # Environment variables (not version controlled)
├── tests/                 # Directory with tests
│   └── conftest.py        # Foundation to the falsk app testing
│   └── test_app.py        # Testing Flask app behavior
│   └── test_models.py     # Testing DB part
│   └── test_weather.py    # Testing work of API
├── conftest.py            # Foundation to the falsk app testing
├── test_app.py            # Testing Flask app behavior
├── test_models.py         # Testing DB part
├── test_weather.py        # Testing work of API
├── templates/             # HTML templates (index, history)
└── static/                # Static assets (if any)
```

## Running Tests

Tests are written with pytest and mock external dependencies.

To run all tests:

```bash
docker-compose run web pytest
```

Or locally after installing dependencies:

```bash
pip install -r requirements.txt
pytest
```

## Environment Variables

| Variable            | Description                            | Required |
|---------------------|-------------------------------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key               | Yes      |
| `DATABASE_URL`        | PostgreSQL connection string         | Yes      |
| `FLASK_SECRET_KEY`    | Flask session secret key (for security) | No (recommended) |

## Notes

- The PostgreSQL password is `sin` per default, synchronized in `.env` and `docker-compose.yml`.
- For production, **change passwords and secret keys** to secure values.
- Flask runs in debug mode by default for development; disable in production.
- Health check makes sure Postgres container is ready before starting the web app.
- Tests mock the database and API calls to keep tests reliable and fast.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [PostgreSQL](https://www.postgresql.org/) as the database.
- [OpenWeatherMap](https://openweathermap.org/api) for weather data.
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) for containerization.
- [pytest](https://docs.pytest.org/) for testing support.
