import sys
import os
from PyQt5.QtWidgets import QApplication

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Global Style (Premium Feel)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
