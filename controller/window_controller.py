from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow
from view.view import Main
from view.help import Help
from controller.graph_controller import GraphController

class WindowController(QObject):
    def __init__(self):
        super().__init__()
        self.main_window = Main()
        self.graph_controller = GraphController(self.main_window)
        self.help_window = Help()
        self.main_window.show()

        # Button implementation
        self.main_window.help_btn.clicked.connect(self.open_help_window)

    def open_help_window(self):
        self.help_window.show()
        self.help_window.ok_btn.clicked.connect(self.close_help_window)

    def close_help_window(self):
        self.help_window.close()