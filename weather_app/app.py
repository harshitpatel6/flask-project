from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# OpenWeatherMap API configuration
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class WeatherSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    
    if not city:
        return jsonify({'error': 'Please enter a city name'}), 400
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'temperature': round(data['main']['temp']),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed']
        }
        
        # Save search to database
        search = WeatherSearch(
            city=city,
            temperature=weather_info['temperature'],
            humidity=weather_info['humidity'],
            description=weather_info['description'],
            wind_speed=weather_info['wind_speed']
        )
        db.session.add(search)
        db.session.commit()
        
        return jsonify(weather_info)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    searches = WeatherSearch.query.order_by(WeatherSearch.timestamp.desc()).all()
    return render_template('admin/dashboard.html', searches=searches)

# Create database tables
with app.app_context():
    db.create_all()
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123'))
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True) 