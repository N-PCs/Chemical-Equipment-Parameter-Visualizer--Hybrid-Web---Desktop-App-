# Chemical Equipment Parameter Visualizer

A hybrid Web + Desktop application for chemical equipment data visualization and analytics.

## Structure

- **backend/**: Django REST API
- **frontend-web/**: React application
- **frontend-desktop/**: PyQt5 application
- **shared/**: Shared types and utilities

## Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (optional)

## Setup

### Backend Setup (Local)

1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Create virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations and server:
   ```bash
   cd src
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup

See `frontend-web/README.md` and `frontend-desktop/README.md`.
