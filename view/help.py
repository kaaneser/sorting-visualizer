from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class Help(QDialog):
    def __init__(self):
      super().__init__()
      loadUi("view/help.ui", self)