# StorySpace - Advanced Blog System (ECU4311)

**GitHub Repository:** [https://github.com/NadeeraBinoli/StorySpace](https://github.com/NadeeraBinoli/StorySpace)

A full-featured blog application built with Django 5.0, focusing on modern UI/UX, real-time interactions, and secure authentication.

## Setup Instructions

Follow these steps to run the project on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Setup Virtual Environment
Open your terminal in the project root and run:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`

---

##  Test Credentials
If you wish to test with pre-existing data:
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin` (Create your own using `python manage.py createsuperuser`)
- **Password**: `admin123`
