# ChemEquip Visualizer: Setup & Installation Guide

This guide provides step-by-step instructions to get the **ChemEquip Visualizer Industrial Analytics Suite** up and running on your local machine.

---

## 📋 Prerequisites

Ensure you have the following installed:

- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **npm**: Version 7 or higher (comes with Node.js)
- **pip**: Python package installer (comes with Python)

---

## 🛠 Step-by-Step Setup

### 1. Backend (Django REST API)

The backend provides centralized data storage, PDF generation, and API endpoints.

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (REQUIRED for authentication)
# This command creates an 'admin' user with password 'admin123'
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"

# Start the development server
python manage.py runserver
```

**API will be available at**: `http://localhost:8000/api/`

---

### 2. Web Frontend (React + Vite)

Modern web-based portal optimized for all browsers.

```bash
# Navigate to frontend-web directory
cd frontend-web

# Install dependencies
npm install

# Start development server
npm run dev
```

**Web application will be available at**: `http://localhost:3000`  
**Default Credentials**: `admin` / `admin123`

---

### 3. Desktop Application (PyQt5)

Native industrial dashboard for Windows/macOS/Linux.

```bash
# Navigate to frontend-desktop directory
cd frontend-desktop

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the desktop application
python main.py
```

---

## 🔧 Troubleshooting

### Backend Issues
- **`ModuleNotFoundError`**: Ensure your virtual environment is activated and you've run `pip install -r requirements.txt`.
- **Database errors**: Run `python manage.py migrate` to apply database migrations.

### Frontend Web Issues
- **`npm install` fails**: Delete `node_modules` and `package-lock.json`, then run `npm install` again.
- **Port 3000 already in use**: Kill the process using port 3000 or configure a different port in `vite.config.ts`.

### Desktop Application Issues
- **PyQt5 installation fails**: You may need system-level dependencies:
  - **Ubuntu/Debian**: `sudo apt-get install python3-pyqt5`
  - **macOS**: `brew install pyqt5`

---

## 🚀 Running All Components Simultaneously

To run the entire suite, open three separate terminals and run:

1. **Terminal 1 (Backend)**: `cd backend && python manage.py runserver`
2. **Terminal 2 (Web)**: `cd frontend-web && npm run dev`
3. **Terminal 3 (Desktop)**: `cd frontend-desktop && python main.py`
