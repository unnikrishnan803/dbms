# Blood Donation App

A Django-based blood donation management system with user registration, donor management, blood inventory tracking, and statistics.

## Features

- User registration and authentication
- Blood donor management
- Blood inventory tracking
- Blood request system
- Donation tracking
- Statistics and reporting
- Light/Dark theme toggle
- Responsive design

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 2. Clone and Navigate

```bash
cd /home/kali/dbms/blood_donation
```

### 3. Virtual Environment Setup

#### Option 1: Using the activation script (Recommended)
```bash
bash activate_venv.sh
```

#### Option 2: Manual activation
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The app will be available at: http://127.0.0.1:8000/

## Virtual Environment Management

### Activate Virtual Environment
```bash
bash activate_venv.sh
# or
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Install New Packages
```bash
pip install <package_name>
pip freeze > requirements.txt  # Update requirements
```

### Check Installed Packages
```bash
pip list
```

## Project Structure

```
blood_donation/
├── blood_app/           # Main Django app
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # URL routing
│   ├── forms.py        # Form definitions
│   └── templates/      # HTML templates
├── blood_donation/     # Django project settings
├── venv/              # Virtual environment
├── requirements.txt    # Python dependencies
├── activate_venv.sh   # Virtual environment activation script
└── manage.py          # Django management script
```

## Current Dependencies

- **Django**: 5.2.5 (Web framework)
- **Pillow**: 11.3.0 (Image processing)
- **SQLite3**: Built-in database

## Theme System

The app includes a dual theme system:
- **Light Theme**: Clean white background with dark text
- **Dark Theme**: Dark blue background with light text
- **Toggle**: Click the theme button in the navigation bar

## Troubleshooting

### Virtual Environment Issues
- Ensure you're in the correct directory: `/home/kali/dbms/blood_donation`
- Use `bash activate_venv.sh` to activate the environment
- Check if `venv/` directory exists

### Package Installation Issues
- Upgrade pip: `pip install --upgrade pip`
- Install build tools: `pip install --upgrade setuptools wheel`
- Try installing packages individually: `pip install Django`

### Database Issues
- Run migrations: `python manage.py migrate`
- Check database file: `db.sqlite3`

## Support

For issues or questions, check the Django documentation or contact the development team.
