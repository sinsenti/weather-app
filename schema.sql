CREATE TABLE IF NOT EXISTS queries (
    id SERIAL PRIMARY KEY,
    city_name VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    weather_description VARCHAR(255),
    humidity INTEGER,
    wind_speed REAL
);
