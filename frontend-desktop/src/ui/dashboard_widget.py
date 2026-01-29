from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DashboardWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_upload_id = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # 1. Summary Cards Area
        self.stats_layout = QHBoxLayout()
        self.total_card = self.create_card("Total Equipment", "0")
        self.flow_card = self.create_card("Avg Flowrate", "0 m³/h")
        self.pressure_card = self.create_card("Avg Pressure", "0 atm")
        self.temp_card = self.create_card("Avg Temperature", "0 °C")

        self.stats_layout.addWidget(self.total_card)
        self.stats_layout.addWidget(self.flow_card)
        self.stats_layout.addWidget(self.pressure_card)
        self.stats_layout.addWidget(self.temp_card)
        
        main_layout.addLayout(self.stats_layout)

        # 2. Charts Area
        charts_layout = QHBoxLayout()
        
        # Bar Chart
        self.bar_figure = Figure(figsize=(5, 4), dpi=100)
        self.bar_canvas = FigureCanvas(self.bar_figure)
        charts_layout.addWidget(self.bar_canvas)

        # Pie Chart
        self.pie_figure = Figure(figsize=(4, 4), dpi=100)
        self.pie_canvas = FigureCanvas(self.pie_figure)
        charts_layout.addWidget(self.pie_canvas)

        main_layout.addLayout(charts_layout)

        # 3. Data Table (Simplified)
        self.table_label = QLabel("Recent Data")
        self.table_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(self.table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Flowrate", "Pressure", "Temperature"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(card)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #666; font-size: 12px; text-transform: uppercase;")
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet("color: #333; font-size: 24px; font-weight: bold;")
        value_lbl.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        return card

    def update_card(self, card, value):
        # Value label is the second widget in layout
        card.layout().itemAt(1).widget().setText(str(value))

    def load_data(self, upload_id):
        self.current_upload_id = upload_id
        
        # 1. Get Stats
        stats = self.api_client.get_summary_stats(upload_id)
        if stats:
            self.update_card(self.total_card, stats['total_count'])
            self.update_card(self.flow_card, f"{stats['averages']['flowrate']} m³/h")
            self.update_card(self.pressure_card, f"{stats['averages']['pressure']} atm")
            self.update_card(self.temp_card, f"{stats['averages']['temperature']} °C")
            self.plot_charts(stats)

        # 2. Get List
        equipment = self.api_client.get_equipment_list(upload_id)
        if equipment:
            self.populate_table(equipment)

    def plot_charts(self, stats):
        # Bar Chart
        self.bar_figure.clear()
        ax1 = self.bar_figure.add_subplot(111)
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            stats['averages']['flowrate'], 
            stats['averages']['pressure'], 
            stats['averages']['temperature']
        ]
        ax1.bar(params, values, color=['#3b82f6', '#10b981', '#ef4444'])
        ax1.set_title('Average Parameters')
        self.bar_canvas.draw()

        # Pie Chart
        self.pie_figure.clear()
        ax2 = self.pie_figure.add_subplot(111)
        labels = [d['equipment_type'] for d in stats['type_distribution']]
        sizes = [d['count'] for d in stats['type_distribution']]
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Equipment Types')
        self.pie_canvas.draw()

    def populate_table(self, data):
        self.table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(item['equipment_name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['flowrate'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['pressure'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item['temperature'])))
