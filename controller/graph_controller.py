import asyncio
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QMainWindow
from view.view import Main
from view.help import Help
from controller.alert_controller import AlertController
from model.graph_model import GraphModel
from random import randint

class GraphController:
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.graph = GraphModel([], '', '', self.main_window.MplWidget, 10000, self.main_window.count_lbl, self.main_window.complex_lbl)

        self.sorting_algorithm = self.main_window.algorithm_combobox
        self.graph_type = self.main_window.graph_combobox
        self.speed_slider = self.main_window.speed_slider
        self.el_input = self.main_window.element_input
        self.el_count = self.main_window.element_count
        self.is_user_defined = True
        self.elements = []

        self.main_window.start_btn.setEnabled(False)
        self.main_window.stop_btn.setEnabled(False)

        # Graph method implementations
        self.sorting_algorithm.currentIndexChanged.connect(self.select_algorithm)
        self.graph_type.currentIndexChanged.connect(self.select_graph)
        self.speed_slider.valueChanged.connect(self.set_speed)
        self.el_input.textChanged.connect(self.set_elem)
        self.el_count.valueChanged.connect(self.set_rand)
        self.main_window.create_btn.clicked.connect(self.generate_graph)
        self.main_window.start_btn.clicked.connect(self.play)
        self.main_window.stop_btn.clicked.connect(self.start_stop)

    def select_algorithm(self):
        print("Selected: ", self.sorting_algorithm.currentText())

    def select_graph(self):
        print("Selected: ", self.graph_type.currentText())

    def set_speed(self):
        print("Speed: ", self.speed_slider.value() * 100)
        self.graph.interval = (self.speed_slider.value() * 100)

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
            if (self.main_window.create_btn.text() == "SIFIRLA"):
                self.main_window.MplWidget.canvas.axes.clear()
                self.main_window.MplWidget.canvas.draw()
                self.main_window.create_btn.setText("OLUŞTUR")
                self.main_window.stop_btn.setText('DURDUR')
                self.main_window.count_lbl.setText("Karşılaştırma Sayısı:")
                self.main_window.complex_lbl.setText("Karmaşıklık Analizi:")
            else:
                if (self.is_user_defined):
                    self.elements = [int(x) for x in self.el_input.text().split(',')]
                else:
                    self.elements = [randint(1, 100) for _ in range(self.el_count.value())]

                self.graph = GraphModel(
                    self.elements,
                    self.graph_type.currentIndex(),
                    self.sorting_algorithm.currentIndex(),
                    self.main_window.MplWidget,
                    (self.speed_slider.value() * 100),
                    self.main_window.count_lbl,
                    self.main_window.complex_lbl
                )

                self.graph.print_info()
                self.graph.prepare()
                self.main_window.create_btn.setText("SIFIRLA")
                self.main_window.start_btn.setEnabled(True)
                self.main_window.stop_btn.setEnabled(True)
        except ValueError:
            self.alert = AlertController("Hata! Lütfen elementleri doğru formatta girdiğinize emin olunuz.")
            self.alert.open_alert_window()

    def play(self):
        self.main_window.create_btn.setEnabled(False)

        if self.sorting_algorithm.currentIndex() == 4:
            method = self.graph.algorithm_map()
            method(0, len(self.elements) - 1)
        elif self.sorting_algorithm.currentIndex() == 3:
            method = self.graph.algorithm_map()
            comparisions = method(self.elements)
            print(self.elements)
        else:
            method = self.graph.algorithm_map()
            method()
        self.main_window.stop_btn.setEnabled(False)
        self.main_window.start_btn.setEnabled(False)
        self.main_window.create_btn.setEnabled(True)

    def start_stop(self):
        if (self.main_window.stop_btn.text() == 'DURDUR'):
            self.graph.stop()
            self.main_window.stop_btn.setText('DEVAM ET')
            self.main_window.create_btn.setEnabled(True)
        elif (self.main_window.stop_btn.text() == 'DEVAM ET'):
            self.graph.start()
            self.main_window.stop_btn.setText('DURDUR')
            self.main_window.create_btn.setEnabled(False)