# Task Manager API

A Django REST Framework-based task management API with user authentication, task organization, and categorization features.

## Project Overview

This project provides a REST API for managing tasks with the following features:
- User authentication with JWT tokens
- Task management (CRUD operations)
- Task categorization
- Task filtering by status and priority
- User-specific task organization

## Tech Stack

- **Backend**: Django 4.2.27
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (SimpleJWT)
- **API Documentation**: drf-spectacular
- **Database**: SQLite (development)

## Local Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Task-Manager
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

### Step 5: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account with username and password.

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

- **POST** `/api/accounts/signup/` - Register a new user
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

- **POST** `/api/accounts/login/` - Get JWT token
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
  Returns: `{"access": "token", "refresh": "token"}`

- **POST** `/api/accounts/refresh/` - Refresh access token
  ```json
  {
    "refresh": "your_refresh_token"
  }
  ```

- **GET** `/api/accounts/me/` - Get current user info (requires authentication)

### Task Endpoints

- **GET** `/api/tasks/tasks/` - List all tasks (requires authentication)
- **POST** `/api/tasks/tasks/` - Create a new task (requires authentication)
- **GET** `/api/tasks/tasks/{id}/` - Get task details
- **PUT** `/api/tasks/tasks/{id}/` - Update task
- **DELETE** `/api/tasks/tasks/{id}/` - Delete task
- **GET** `/api/tasks/tasks/by_status/?status=TODO` - Filter tasks by status

### Category Endpoints

- **GET** `/api/tasks/categories/` - List all categories
- **POST** `/api/tasks/categories/` - Create a new category
- **GET** `/api/tasks/categories/{id}/` - Get category details
- **PUT** `/api/tasks/categories/{id}/` - Update category
- **DELETE** `/api/tasks/categories/{id}/` - Delete category

## API Documentation

Once the server is running, you can access interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/swagger/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Authentication

The API uses JWT (JSON Web Token) authentication. To authenticate:

1. Get an access token from `/api/accounts/login/`
2. Include the token in the `Authorization` header for subsequent requests:
   ```
   Authorization: Bearer YOUR_ACCESS_TOKEN
   ```

### Testing with cURL

```bash
# 1. Sign up
curl -X POST http://localhost:8000/api/accounts/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 2. Login
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 3. Get current user (replace TOKEN with access token from step 2)
curl -X GET http://localhost:8000/api/accounts/me/ \
  -H "Authorization: Bearer TOKEN"
```

## Project Structure

```
Task-Manager/
├── accounts/              # User authentication app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── tasks/                 # Task management app
│   ├── models.py         # Task and Category models
│   ├── serializers.py    # Task and Category serializers
│   ├── views.py          # Task and Category viewsets
│   ├── urls.py
│   └── migrations/
├── taskboard/            # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── utils/                # Utilities
│   └── enums.py          # TaskStatus and TaskPriority enums
├── manage.py
├── requirements.txt
└── db.sqlite3           # SQLite database
```

## Models

### User (from Django's built-in User model)
- username
- email
- password

### Task
- id (UUID)
- user (ForeignKey to User)
- title
- description
- status (TODO, IN_PROGRESS, DONE)
- priority (LOW, MEDIUM, HIGH)
- due_date
- category (ForeignKey to Category)
- created_at
- updated_at

### Category
- id (UUID)
- name
- color

## Development

### Run Tests

```bash
python manage.py test
```

### Create a New Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Admin

1. Create a superuser (if not already done)
2. Go to http://localhost:8000/admin/
3. Log in with superuser credentials

## Troubleshooting

### Port 8000 Already in Use

```bash
python manage.py runserver 8001
```

### Database Errors

```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

## License

This project is open source.

## Support

For issues or questions, please contact the development team.
