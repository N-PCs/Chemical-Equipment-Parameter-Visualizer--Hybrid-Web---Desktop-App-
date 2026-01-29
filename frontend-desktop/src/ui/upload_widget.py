from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
import os

class UploadWidget(QWidget):
    upload_success = pyqtSignal(int)  # Signal emitting upload_id

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Drop Zone Frame
        self.drop_frame = QFrame()
        self.drop_frame.setFixedSize(600, 400)
        self.drop_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.drop_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            QFrame:hover {
                border-color: #3b82f6;
                background-color: #fff;
            }
        """)
        self.drop_frame.setAcceptDrops(True)
        self.drop_frame.dragEnterEvent = self.dragEnterEvent
        self.drop_frame.dropEvent = self.dropEvent

        drop_layout = QVBoxLayout(self.drop_frame)
        drop_layout.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel("☁️")
        self.icon_label.setStyleSheet("font-size: 64px;")
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel("Drag & Drop CSV file here\nor")
        self.text_label.setStyleSheet("font-size: 18px; color: #666;")
        self.text_label.setAlignment(Qt.AlignCenter)

        self.browse_btn = QPushButton("Browse File")
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.browse_btn.clicked.connect(self.browse_file)

        drop_layout.addWidget(self.icon_label)
        drop_layout.addWidget(self.text_label)
        drop_layout.addWidget(self.browse_btn)

        layout.addWidget(self.drop_frame)
        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.handle_file(files[0])

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.handle_file(file_path)

    def handle_file(self, file_path):
        if not file_path.endswith('.csv'):
            QMessageBox.warning(self, "Invalid File", "Please select a valid CSV file.")
            return

        self.text_label.setText(f"Processing: {os.path.basename(file_path)}...")
        self.browse_btn.setEnabled(False)
        self.repaint()

        result = self.api_client.upload_csv(file_path)

        if result:
            QMessageBox.information(self, "Success", f"Upload successful! Processed {result.get('count', 0)} records.")
            self.upload_success.emit(result['id'])
        else:
             QMessageBox.critical(self, "Error", "Failed to upload file.")
        
        self.text_label.setText("Drag & Drop CSV file here\nor")
        self.browse_btn.setEnabled(True)
