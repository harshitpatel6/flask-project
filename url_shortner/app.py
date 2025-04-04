# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify  # Flask web framework and its utilities
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database operations
from datetime import datetime  # For timestamp handling
import os  # For operating system operations

# Initialize Flask application
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'  # Set database file location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance
db = SQLAlchemy(app)  # Initialize database

# Define URL model for database
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each URL
    original_url = db.Column(db.String(500), nullable=False)  # Original long URL
    short_code = db.Column(db.String(10), unique=True, nullable=False)  # Shortened URL code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation
    clicks = db.Column(db.Integer, default=0)  # Counter for number of times URL is accessed

    def __repr__(self):
        return f'<URL {self.original_url}>'  # String representation of URL object

    def to_dict(self):
        # Convert URL object to dictionary for JSON response
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'clicks': self.clicks
        }

def generate_short_code():
    # Generate a random 6-character code for shortened URL
    import random
    import string
    characters = string.ascii_letters + string.digits  # Use letters and numbers
    while True:
        # Generate random code and check if it's unique
        short_code = ''.join(random.choice(characters) for _ in range(6))
        if not URL.query.filter_by(short_code=short_code).first():
            return short_code

@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle both GET and POST requests for the main page
    if request.method == 'POST':
        # Process URL shortening request
        original_url = request.form['url']
        if not original_url:
            return render_template('index.html', error='Please enter a URL')
        
        # Add https:// if protocol is missing
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'https://' + original_url

        # Create new URL entry
        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        
        try:
            # Save to database
            db.session.add(new_url)
            db.session.commit()
            # Generate full shortened URL
            short_url = url_for('redirect_to_url', short_code=short_code, _external=True)
            return render_template('index.html', short_url=short_url)
        except:
            # Handle database errors
            db.session.rollback()
            return render_template('index.html', error='An error occurred. Please try again.')
    
    # Handle GET request - show the form
    return render_template('index.html')

@app.route('/api/urls', methods=['GET'])
def list_urls():
    # API endpoint to get all URLs, sorted by creation date
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return jsonify([url.to_dict() for url in urls])

@app.route('/api/stats/<short_code>')
def url_stats(short_code):
    # API endpoint to get statistics for a specific URL
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    return jsonify(url.to_dict())

@app.route('/<short_code>')
def redirect_to_url(short_code):
    # Handle redirection from short URL to original URL
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    url.clicks += 1  # Increment click counter
    db.session.commit()  # Save the updated click count
    return redirect(url.original_url)  # Redirect to original URL

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    # Run the application
    app.run(host='0.0.0.0', port=8000, debug=True) 