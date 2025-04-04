# URL Shortener

A simple and modern URL shortener built with Flask and SQLite.

## Features

- Shorten long URLs to manageable links
- Automatic redirection to original URLs
- Modern, responsive UI using Tailwind CSS
- Copy to clipboard functionality
- SQLite database for URL storage

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter a long URL in the input field
2. Click "Shorten URL"
3. Copy the shortened URL using the copy button
4. Share the shortened URL with others

## Technical Details

- Built with Flask web framework
- Uses SQLite for database storage
- Frontend styled with Tailwind CSS
- Generates 6-character random codes for shortened URLs 