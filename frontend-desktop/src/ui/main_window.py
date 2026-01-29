from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QAction, QToolBar, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from .upload_widget import UploadWidget
from .dashboard_widget import DashboardWidget
from ..services.api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1000, 700)
        
        # Services
        self.api_client = api_client

        # UI Components
        self.upload_widget = UploadWidget(self.api_client)
        self.dashboard_widget = DashboardWidget(self.api_client)

        self.init_ui()
        self.connect_signals()
        
        # Apply Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)

    def init_ui(self):
        # 1. Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Actions
        nav_upload = QAction("Upload Data", self)
        nav_upload.triggered.connect(lambda: self.switch_view(0))
        toolbar.addAction(nav_upload)

        nav_dashboard = QAction("Dashboard", self)
        nav_dashboard.triggered.connect(lambda: self.switch_view(1))
        toolbar.addAction(nav_dashboard)

        # 2. Central Widget (Stacked)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        self.stack = QStackedWidget()
        self.stack.addWidget(self.upload_widget)
        self.stack.addWidget(self.dashboard_widget)
        
        self.layout.addWidget(self.stack)

        # Status Bar
        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)

    def connect_signals(self):
        self.upload_widget.upload_success.connect(self.on_upload_success)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        view_name = "Upload" if index == 0 else "Dashboard"
        self.status_label.setText(f"View: {view_name}")

    def on_upload_success(self, upload_id):
        self.status_label.setText(f"Data Loaded: ID {upload_id}")
        self.dashboard_widget.load_data(upload_id)
        self.switch_view(1)  # Switch to Dashboard
