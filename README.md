# Flask Todo List Application

A simple Todo List application built with Flask, SQLite, and Bootstrap.

## Features

- Create, Read, Update, and Delete tasks
- Mark tasks as complete/incomplete
- Mobile-responsive UI with Bootstrap

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Ensure your virtual environment is activated
2. Run the application:
   ```
   python run.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`

## File Structure

- `app/`: Application package
  - `__init__.py`: Flask application factory
  - `models.py`: Database models
  - `routes.py`: Application routes and views
  - `templates/`: HTML templates
- `run.py`: Entry point to run the application
- `requirements.txt`: Project dependencies
- `todo.db`: SQLite database (created when application runs)
