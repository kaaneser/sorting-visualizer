from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow
from view.view import Main
from view.help import Help
from controller.alert_controller import AlertController
from model.graph_model import GraphModel

class GraphController:
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.sorting_algorithm = self.main_window.algorithm_combobox
        self.graph_type = self.main_window.graph_combobox
        self.speed_slider = self.main_window.speed_slider
        self.el_input = self.main_window.element_input
        self.el_count = self.main_window.element_count
        self.is_user_defined = True

        # Graph method implementations
        self.sorting_algorithm.currentIndexChanged.connect(self.select_algorithm)
        self.graph_type.currentIndexChanged.connect(self.select_graph)
        self.speed_slider.valueChanged.connect(self.set_speed)
        self.el_input.textChanged.connect(self.set_elem)
        self.el_count.valueChanged.connect(self.set_rand)
        self.main_window.create_btn.clicked.connect(self.generate_graph)

    def select_algorithm(self):
        print("Selected: ", self.sorting_algorithm.currentText())

    def select_graph(self):
        print("Selected: ", self.graph_type.currentText())

    def set_speed(self):
        print("Speed: ", self.speed_slider.value())

    def set_elem(self):
        if self.el_input.text():
            self.el_count.setEnabled(False)
            self.is_user_defined = True
        else:
            self.el_count.setEnabled(True)
            self.is_user_defined = False

    def set_rand(self):
        if self.el_count.value() > 0:
            self.el_input.setEnabled(False)
            self.is_user_defined = False
        else:
            self.el_input.setEnabled(True)
            self.is_user_defined = True

    def generate_graph(self):
        try:
            elements = [int(x) for x in self.el_input.text().split(',')]
            self.graph = GraphModel(
                elements,
                self.graph_type.currentText(),
                self.sorting_algorithm.currentText()
            )

            self.graph.print_info()
        except ValueError:
            self.alert = AlertController("Hata! Lütfen elementleri doğru formatta girdiğinize emin olunuz.")
            self.alert.open_alert_window()
