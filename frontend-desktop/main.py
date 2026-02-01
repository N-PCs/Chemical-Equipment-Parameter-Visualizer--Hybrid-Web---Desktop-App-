
"""
ARCHITECTURE: /frontend-desktop/src/
Purpose: Production-grade PyQt5 Desktop application for chemical equipment visualization.
Features: CSV loading via Pandas, Table views, and Matplotlib integration.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from fpdf import FPDF
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QLabel, QFrame, QHeaderView, QMessageBox,
                             QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap

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
            #stat_card {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
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
        
        self.export_btn = QPushButton("EXPORT PDF REPORT")
        self.export_btn.setFixedWidth(200)
        self.export_btn.setStyleSheet("background-color: #10b981;") # Green for export
        self.export_btn.clicked.connect(self.export_to_pdf)
        self.export_btn.setEnabled(False)
        header.addWidget(self.export_btn)

        self.upload_btn = QPushButton("IMPORT CSV DATASET")
        self.upload_btn.setFixedWidth(200)
        self.upload_btn.clicked.connect(self.handle_upload)
        header.addWidget(self.upload_btn)
        
        main_layout.addLayout(header)

        # 1.5 Statistics Overview
        stats_label = QLabel("Enterprise Metrics Dashboard")
        stats_label.setFont(QFont("Inter", 11, QFont.Bold))
        main_layout.addWidget(stats_label)

        self.stats_layout = QGridLayout()
        self.stats_layout.setSpacing(15)
        main_layout.addLayout(self.stats_layout)
        self.init_stats_cards()

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
        viz_scroll = QScrollArea()
        viz_scroll.setWidgetResizable(True)
        viz_scroll.setFrameShape(QFrame.NoFrame)
        
        viz_content = QWidget()
        viz_layout = QVBoxLayout(viz_content)
        
        # Increased height and used constrained_layout for better spacing
        self.figure, self.axes = plt.subplots(4, 1, figsize=(6, 20), constrained_layout=True)
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvas(self.figure)
        
        # Ensure the canvas has a minimum height to force scrolling
        self.canvas.setMinimumHeight(1500)
        
        viz_layout.addWidget(self.canvas)
        
        viz_scroll.setWidget(viz_content)
        QVBoxLayout(self.viz_frame).addWidget(viz_scroll)
        
        right_panel.addWidget(self.viz_frame)
        content_area.addLayout(right_panel, 2)

        main_layout.addLayout(content_area)

    def init_stats_cards(self):
        metrics = [
            ("Avg Pressure", "0.0 bar", "#3b82f6"),
            ("Avg Temp", "0.0 C", "#ef4444"),
            ("Total Flow", "0.0 m3/h", "#10b981"),
            ("Unit Count", "0", "#8b5cf6")
        ]
        self.card_widgets = {}
        for i, (label, val, color) in enumerate(metrics):
            card = QFrame()
            card.setObjectName("stat_card")
            card_layout = QVBoxLayout(card)
            
            l = QLabel(label)
            l.setFont(QFont("Inter", 9, QFont.Bold))
            l.setStyleSheet("color: #64748b; border: none;")
            
            v = QLabel(val)
            v.setFont(QFont("Inter", 14, QFont.Bold))
            v.setStyleSheet(f"color: {color}; border: none;")
            
            card_layout.addWidget(l)
            card_layout.addWidget(v)
            self.stats_layout.addWidget(card, 0, i)
            self.card_widgets[label] = v

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
                self.export_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to process dataset: {str(e)}")

    def update_ui(self):
        if self.data is None: return

        # 1. Update Stats
        self.card_widgets["Avg Pressure"].setText(f"{self.data['Pressure'].mean():.2f} bar")
        self.card_widgets["Avg Temp"].setText(f"{self.data['Temperature'].mean():.1f} C")
        self.card_widgets["Total Flow"].setText(f"{self.data['Flowrate'].sum():.1f} m3/h")
        self.card_widgets["Unit Count"].setText(str(len(self.data)))

        # 2. Update Table Registry
        self.table.setRowCount(len(self.data))
        for i, row in self.data.iterrows():
            self.table.setItem(i, 0, QTableWidgetItem(str(row['Equipment Name'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['Type'])))
            self.table.setItem(i, 2, QTableWidgetItem(f"{row['Flowrate']:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['Pressure']:.2f}"))
            
            temp_item = QTableWidgetItem(f"{row['Temperature']:.1f}")
            if row['Temperature'] > 200:
                temp_item.setForeground(QColor("#ef4444"))
                temp_item.setFont(QFont("Inter", weight=QFont.Bold))
            self.table.setItem(i, 4, temp_item)

        # 3. Update Matplotlib Charts
        for ax in self.axes: ax.clear()
        
        # Chart 1: Flowrate Distribution
        self.data.plot(kind='bar', x='Equipment Name', y='Flowrate', ax=self.axes[0], color='#3b82f6', legend=False)
        self.axes[0].set_title("Flowrate by Equipment Unit", fontsize=9, fontweight='bold')
        self.axes[0].tick_params(axis='x', labelsize=7, labelrotation=45)
        
        # Chart 2: Type Distribution
        counts = self.data['Type'].value_counts()
        self.axes[1].pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, 
                         colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'])
        self.axes[1].set_title("Asset Type Composition", fontsize=9, fontweight='bold')
        
        # Chart 3: Pressure vs Temperature Scatter
        sns.scatterplot(data=self.data, x='Pressure', y='Temperature', hue='Type', ax=self.axes[2])
        self.axes[2].set_title("Pressure vs Temperature Correlation", fontsize=9, fontweight='bold')
        self.axes[2].legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Chart 4: Temperature Distribution Boxplot
        sns.boxplot(data=self.data, x='Type', y='Temperature', ax=self.axes[3], palette="Set2")
        self.axes[3].set_title("Temperature Variance by Type", fontsize=9, fontweight='bold')
        self.axes[3].tick_params(axis='x', labelsize=7)

        self.canvas.draw()

    def export_to_pdf(self):
        if self.data is None: return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"ChemEquip_Report_{datetime.now().strftime('%Y%m%d')}.pdf", "PDF Files (*.pdf)")
        if not file_path: return

        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(30, 41, 59) # #1e293b
            pdf.cell(0, 15, "CHEMEQUIP INDUSTRIAL REPORT", ln=True, align="C")
            
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(100, 116, 139) # #64748b
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            pdf.ln(10)

            # Summary Stats
            pdf.set_fill_color(241, 245, 249)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, " 1. EXECUTIVE SUMMARY", ln=True, fill=True)
            pdf.ln(5)
            
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(90, 8, f"Total Equipment Units: {len(self.data)}")
            pdf.cell(90, 8, f"Average Pressure: {self.data['Pressure'].mean():.2f} bar", ln=True)
            pdf.cell(90, 8, f"Average Temperature: {self.data['Temperature'].mean():.1f} C")
            pdf.cell(90, 8, f"Total System Flow: {self.data['Flowrate'].sum():.1f} m3/h", ln=True)
            pdf.ln(10)

            # Asset Table
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 10, " 2. ASSET REGISTRY DETAILS", ln=True, fill=True)
            pdf.ln(5)
            
            # Table Header
            pdf.set_font("Helvetica", "B", 10)
            cols = ["Name", "Type", "Flow", "Pres", "Temp"]
            widths = [50, 40, 30, 30, 30]
            for col, w in zip(cols, widths):
                pdf.cell(w, 8, col, border=1, align="C")
            pdf.ln()
            
            # Table Data
            pdf.set_font("Helvetica", "", 9)
            for _, row in self.data.iterrows():
                pdf.cell(widths[0], 7, str(row['Equipment Name']), border=1)
                pdf.cell(widths[1], 7, str(row['Type']), border=1)
                pdf.cell(widths[2], 7, f"{row['Flowrate']:.1f}", border=1, align="C")
                pdf.cell(widths[3], 7, f"{row['Pressure']:.1f}", border=1, align="C")
                pdf.cell(widths[4], 7, f"{row['Temperature']:.1f}", border=1, align="C")
                pdf.ln()

            # Save Visuals (Optional/Bonus: In progress)
            # For simplicity in this v1, we focus on data and stats. 
            # To add charts, we'd save the figure to a temp file and pdf.image() it.
            
            pdf.output(file_path)
            QMessageBox.information(self, "Export Successful", f"Report saved to: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to generate PDF: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Inter", 10))
    window = EquipmentDashboard()
    window.show()
    sys.exit(app.exec_())
