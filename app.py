import sys
from PyQt5.QtWidgets import QApplication
from controller.window_controller import WindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_controller = WindowController()
    sys.exit(app.exec_())