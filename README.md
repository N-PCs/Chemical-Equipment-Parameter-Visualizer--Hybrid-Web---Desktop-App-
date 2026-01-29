# Chemical Equipment Parameter Visualizer

A hybrid Web (React) and Desktop (PyQt5) application for visualizing and analyzing chemical equipment parameters from CSV data.

## Features
- **Data Upload**: Drag & Drop CSV upload for equipment data.
- **Analysis**: Automatic calculation of flowrate, pressure, and temperature averages.
- **Visualization**: Interactive Charts (Bar & Pie) using Chart.js (Web) and Matplotlib (Desktop).
- **Authentication**: Secure Token Authentication.
- **Reporting**: PDF generation and download.
- **Hybrid Access**: Use via Web Browser or Native Desktop App.

## Project Structure
- `backend/`: Django REST Framework (API, Auth, PDF Service).
- `frontend-web/`: Vite + React + TypeScript (Modern Dark Theme).
- `frontend-desktop/`: PyQt5 + Matplotlib.
- `docker-compose.yml`: Containerized setup.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (optional)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
pip install reportlab
cd src
python manage.py migrate
python manage.py runserver
```
*Create a user:* `python create_user.py` (Default: admin/password123)

### Web Frontend
```bash
cd frontend-web
npm install
npm run dev
```
Access at: `http://localhost:5173`

### Desktop Frontend
```bash
cd frontend-desktop
pip install -r requirements.txt
python src/main.py
```

### Docker Deployment
```bash
docker-compose up --build
```

## License
MIT
