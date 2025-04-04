# Dynamic Weather App

A beautiful and interactive weather application built with Flask that displays real-time weather data with dynamic animations based on weather conditions.

## Features

- Real-time weather data from OpenWeatherMap API
- Dynamic weather animations (sun, rain, clouds)
- Responsive design
- Temperature, humidity, and wind speed information
- Beautiful UI with smooth transitions

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
4. Create a `.env` file in the root directory and add your API key:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a city name in the input field
2. Click "Get Weather" or press Enter
3. View the weather information with dynamic animations based on the current weather conditions

## Technologies Used

- Flask
- OpenWeatherMap API
- HTML5
- CSS3 (with animations)
- JavaScript (ES6+)
- Python-dotenv for environment variables

## Note

Make sure to keep your API key secure and never commit it to version control. 