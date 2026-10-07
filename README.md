# Cozmo School Management System

A premium, full-stack Django SaaS application for school management, featuring distinct portals for Admins, Teachers, and Parents.

## Features
- **Admin Portal:** Manage students, classes, finances (fees), warnings, and parent invitations. Export reports to CSV and Excel.
- **Teacher Portal:** Manage assigned classes, assign homework, mark daily attendance, send messages to parents, and write evaluations.
- **Parent Portal:** Read-only dashboard with a multi-child toggle to track academic progress, fees, attendance, and school messages.
- **Role-Based Access Control:** Custom user model enforcing strict access policies across the application.

## Tech Stack
- **Backend:** Python, Django 5
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS
- **Database:** SQLite (default for development)

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Populate Mock Data:**
   ```bash
   python manage.py populate_db
   ```

4. **Run Server:**
   ```bash
   python manage.py runserver
   ```

## Test Credentials
- **Admin:** `admin` / `admin123`
- **Teacher:** `mr_ahmed` / `teacher123`
- **Parent:** `ahmed_parent` / `parent123`
