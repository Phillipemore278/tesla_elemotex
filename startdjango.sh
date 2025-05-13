#!/bin/bash

# Set default project name if not provided
PROJECT_NAME=${1:-myproject}

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment with virtualenv..."
  python -m virtualenv venv
fi

# Step 2: Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Step 3: Upgrade pip
echo "Upgrading pip..."
python.exe -m pip install --upgrade pip

# Step 4: Install requirements or Django
if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Installing Django only..."
  pip install django

  echo "Generating requirements.txt..."
  pip freeze > requirements.txt
fi

# Step 5: Create Django project if manage.py is missing
if [ ! -f "manage.py" ]; then
  echo "No Django project found. Creating project '$PROJECT_NAME'..."
  django-admin startproject "$PROJECT_NAME" .

  # Move manage.py to the root if needed
  if [ -f "$PROJECT_NAME/manage.py" ]; then
    mv "$PROJECT_NAME/manage.py" .
    echo "Moved manage.py to root."
  fi
fi

# Step 6: starting a new app
echo "Starting a new app named frontend..."
python manage.py startapp frontend


