import sys
import os
from PyQt5.QtWidgets import QApplication

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from services.api_client import APIClient

def main():
    app = QApplication(sys.argv)
    
    # Global Style (Premium Feel)
    app.setStyle("Fusion")
    
    # Initialize API Client
    api_client = APIClient()
    
    # Login
    login = LoginDialog(api_client)
    if login.exec_() == LoginDialog.Accepted:
        # Pass already authenticated api_client to MainWindow
        # Note: MainWindow init needs to be updated to accept api_client instead of creating new one
        # wait, MainWindow currently creates its own APIClient. I should change that.
        # But for now I'll just hack it or update MainWindow.
        # Let's update MainWindow to accept api_client.
        window = MainWindow(api_client)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()

if __name__ == "__main__":
    main()
