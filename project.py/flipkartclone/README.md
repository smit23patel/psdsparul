# Flipkart Clone

A Flask-based e-commerce clone of Flipkart with search functionality.

## Features

- User authentication (register/login)
- Product catalog with search
- Shopping cart functionality
- Checkout process
- Responsive design

## Deployment

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the application:
```bash
python app.py
```

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. For production with nginx:
```bash
docker-compose --profile production up --build
```

### Manual Production Deployment

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///database.db"
export FLASK_ENV="production"
```

3. Run with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## Environment Variables

- `SECRET_KEY`: Flask secret key (required)
- `DATABASE_URL`: Database connection string (default: sqlite:///database.db)
- `FLASK_ENV`: Environment (development/production)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)

## Project Structure

```
├── app.py              # Main Flask application
├── wsgi.py             # WSGI entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── nginx.conf          # Nginx configuration
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
├── static/             # Static files (CSS, images)
├── templates/          # HTML templates
└── instance/           # Database files (created automatically)
```

## Security Notes

- Change the default secret key in production
- Use HTTPS in production
- Consider using PostgreSQL for production databases
- Implement proper password hashing (currently using plain text for demo)
