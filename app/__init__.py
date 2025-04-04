from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../todo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Initialize the app with the extension
    db.init_app(app)
    
    # Import and register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 