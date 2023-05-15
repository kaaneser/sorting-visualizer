from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from view.help import Help

class Main(QMainWindow):
    def __init__(self):
      super().__init__()
      loadUi("view/main.ui", self)