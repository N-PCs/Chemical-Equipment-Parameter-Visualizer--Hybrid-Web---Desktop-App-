
"""
ARCHITECTURE: /frontend-desktop/src/
Purpose: Production-grade PyQt5 Desktop application for chemical equipment visualization.
Features: CSV loading via Pandas, Table views, and Matplotlib integration.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QLabel, QFrame, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class EquipmentDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemEquip Visualizer Desktop v2.1")
        self.setGeometry(100, 100, 1280, 850)
        self.data = None
        self.init_ui()

    def init_ui(self):
        # Set Global Style
        self.setStyleSheet("""
            QMainWindow { background-color: #f8fafc; }
            QLabel { color: #1e293b; }
            QPushButton { 
                background-color: #3b82f6; 
                color: white; 
                border-radius: 8px; 
                font-weight: bold; 
                padding: 10px; 
                font-size: 13px;
            }
            QPushButton:hover { background-color: #2563eb; }
            QTableWidget { 
                background-color: white; 
                border: 1px solid #e2e8f0; 
                border-radius: 12px;
                gridline-color: #f1f5f9;
            }
            QHeaderView::section {
                background-color: #f1f5f9;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: #64748b;
                text-transform: uppercase;
                font-size: 10px;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 1. Navbar / Header
        header = QHBoxLayout()
        logo_container = QVBoxLayout()
        title = QLabel("CHEMEQUIP VISUALIZER")
        title.setFont(QFont("Inter", 16, QFont.Bold))
        subtitle = QLabel("Industrial Data Ingestion & Analytics Suite")
        subtitle.setFont(QFont("Inter", 9))
        subtitle.setStyleSheet("color: #64748b;")
        logo_container.addWidget(title)
        logo_container.addWidget(subtitle)
        header.addLayout(logo_container)
        
        header.addStretch()
        
        self.upload_btn = QPushButton("IMPORT CSV DATASET")
        self.upload_btn.setFixedWidth(200)
        self.upload_btn.clicked.connect(self.handle_upload)
        header.addWidget(self.upload_btn)
        
        main_layout.addLayout(header)

        # 2. Main Content Splitter
        content_area = QHBoxLayout()
        content_area.setSpacing(25)

        # LEFT PANEL: Table and Metadata
        left_panel = QVBoxLayout()
        
        self.table_label = QLabel("Active Asset Registry")
        self.table_label.setFont(QFont("Inter", 11, QFont.Bold))
        left_panel.addWidget(self.table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Equipment Name", "Type", "Flow (m3/h)", "Pressure (bar)", "Temp (C)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        left_panel.addWidget(self.table)
        
        content_area.addLayout(left_panel, 3)

        # RIGHT PANEL: Advanced Visualization
        right_panel = QVBoxLayout()
        viz_label = QLabel("Analytical Visualizations")
        viz_label.setFont(QFont("Inter", 11, QFont.Bold))
        right_panel.addWidget(viz_label)

        self.viz_frame = QFrame()
        self.viz_frame.setStyleSheet("background-color: white; border: 1px solid #e2e8f0; border-radius: 12px;")
        viz_layout = QVBoxLayout(self.viz_frame)
        
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvas(self.figure)
        viz_layout.addWidget(self.canvas)
        
        right_panel.addWidget(self.viz_frame)
        content_area.addLayout(right_panel, 2)

        main_layout.addLayout(content_area)

    def handle_upload(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Equipment Dataset", "", "CSV Files (*.csv)", options=options)
        
        if file_name:
            try:
                # Actual production parsing using Pandas
                self.data = pd.read_csv(file_name)
                
                # Validation
                required = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
                if not all(col in self.data.columns for col in required):
                    QMessageBox.critical(self, "Invalid Format", f"CSV must contain columns: {', '.join(required)}")
                    return
                
                self.update_ui()
                self.table_label.setText(f"Active Asset Registry ({os.path.basename(file_name)})")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to process dataset: {str(e)}")

    def update_ui(self):
        if self.data is None: return

        # 1. Update Table Registry
        self.table.setRowCount(len(self.data))
        for i, row in self.data.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['Equipment Name'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['Type'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['Flowrate']:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['Pressure']:.2f}"))
            
            # Highlight high temp rows
            temp_item = QTableWidgetItem(f"{row['Temperature']:.1f}")
            if row['Temperature'] > 200:
                temp_item.setForeground(QColor("#ef4444"))
                temp_item.setFont(QFont("Inter", weight=QFont.Bold))
            self.table.setItem(i, 4, temp_item)

        # 2. Update Matplotlib Charts
        # Chart 1: Flowrate Distribution
        self.ax1.clear()
        self.data.plot(kind='bar', x='Equipment Name', y='Flowrate', ax=self.ax1, color='#3b82f6', legend=False)
        self.ax1.set_title("Flowrate by Equipment Unit", fontsize=10, fontweight='bold', color='#475569')
        self.ax1.tick_params(axis='x', labelsize=8, labelrotation=45)
        self.ax1.set_xlabel("")
        self.ax1.grid(axis='y', linestyle='--', alpha=0.3)
        
        # Chart 2: Type Distribution
        self.ax2.clear()
        counts = self.data['Type'].value_counts()
        self.ax2.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, 
                     colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'])
        self.ax2.set_title("Asset Type Composition", fontsize=10, fontweight='bold', color='#475569')
        
        plt.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 10))
    window = EquipmentDashboard()
    window.show()
    sys.exit(app.exec_())
