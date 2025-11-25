import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

# Add the base path for PyInstaller
if getattr(sys, 'frozen', False):
    # Running in a bundle (PyInstaller)
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.dirname(os.path.abspath(__file__))

# Add base_path to sys.path to help with imports
sys.path.insert(0, base_path)

# Now import MainWindow
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    # Set default modern icon
    app.setWindowIcon(QIcon('icons/default_icon.png'))
    # Launch main window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
