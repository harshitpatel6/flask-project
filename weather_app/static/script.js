document.addEventListener('DOMContentLoaded', () => {
    const weatherForm = document.getElementById('weather-form');
    const cityInput = document.getElementById('city-input');
    const weatherContent = document.getElementById('weather-content');
    const temperature = document.querySelector('.temperature');
    const description = document.querySelector('.description');
    const humidityValue = document.querySelector('.humidity-value');
    const windValue = document.querySelector('.wind-value');

    weatherForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const city = cityInput.value.trim();

        if (!city) return;

        try {
            const formData = new FormData();
            formData.append('city', city);

            const response = await fetch('/weather', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                updateWeatherUI(data);
            } else {
                showError(data.error || 'Failed to fetch weather data');
            }
        } catch (error) {
            showError('An error occurred while fetching weather data');
            console.error('Error:', error);
        }
    });

    function updateWeatherUI(data) {
        // Update text content
        temperature.textContent = `${data.temperature}°C`;
        description.textContent = data.description;
        humidityValue.textContent = `${data.humidity}%`;
        windValue.textContent = `${data.wind_speed} m/s`;

        // Update weather animation
        updateWeatherAnimation(data.description.toLowerCase());
    }

    function showError(message) {
        // Create error message element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;

        // Add error message to the weather content
        weatherContent.insertBefore(errorDiv, weatherContent.firstChild);

        // Remove error message after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    function updateWeatherAnimation(weatherDescription) {
        const weatherIcon = document.querySelector('.weather-icon');
        weatherIcon.innerHTML = ''; // Clear existing content

        if (weatherDescription.includes('rain')) {
            // Create rain animation
            const rain = document.createElement('div');
            rain.className = 'rain';
            
            // Create multiple rain drops
            for (let i = 0; i < 20; i++) {
                const drop = document.createElement('div');
                drop.className = 'rain-drop';
                drop.style.left = `${Math.random() * 100}%`;
                drop.style.animationDelay = `${Math.random() * 2}s`;
                rain.appendChild(drop);
            }

            // Create cloud
            const cloud = document.createElement('div');
            cloud.className = 'cloud';

            weatherIcon.appendChild(cloud);
            weatherIcon.appendChild(rain);
        } else if (weatherDescription.includes('cloud')) {
            // Create cloud
            const cloud = document.createElement('div');
            cloud.className = 'cloud';
            weatherIcon.appendChild(cloud);
        } else if (weatherDescription.includes('clear') || weatherDescription.includes('sun')) {
            // Create sun
            const sun = document.createElement('div');
            sun.className = 'sun';
            weatherIcon.appendChild(sun);
        } else {
            // Default to sun for unknown weather conditions
            const sun = document.createElement('div');
            sun.className = 'sun';
            weatherIcon.appendChild(sun);
        }
    }
}); 