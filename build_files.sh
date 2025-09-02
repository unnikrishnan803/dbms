# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Make migrations
python manage.py makemigrations
python manage.py migrate
