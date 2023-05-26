import numpy as np
import matplotlib
from PyQt5.QtCore import QTimer, QEventLoop
import functools

matplotlib.use('Qt5Agg')
import utils, time

class GraphModel:
    def __init__(self, elements, graph_type, algorithm, MplWidget, speed, count_lbl, complex_lbl):
        super().__init__()
        self.elements = elements
        self.graph_type = graph_type
        self.algorithm = algorithm
        self.MplWidget = MplWidget
        self.plot = None
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.interval = speed
        self.count_lbl = count_lbl
        self.complex_lbl = complex_lbl

    def print_info(self):
        print(f"The graph has the elements: {self.elements}\nGraph Type: {self.graph_type}\nAlgorithm: {self.algorithm}")

    def algorithm_map(self):
        algorithms = {
            0: self.selection_sort,
            1: self.bubble_sort,
            2: self.insertion_sort,
            3: self.merge_sort,
            4: self.quick_sort
        }

        return algorithms[self.algorithm]

    def graph_map(self, colors):
        if self.graph_type == 0:
            self.graph_name = 'scatter'
            self.MplWidget.canvas.axes.scatter(np.arange(len(self.elements)), self.elements, color=colors)
        elif self.graph_type == 1:
            self.graph_name = 'bar'
            self.MplWidget.canvas.axes.bar(np.arange(len(self.elements)), self.elements, color=colors)
        elif self.graph_type == 2:
            self.graph_name = 'stem'
            self.MplWidget.canvas.axes.stem(np.arange(len(self.elements)), self.elements)

    def prepare(self):
        self.MplWidget.canvas.axes.clear()
        self.plot = self.graph_map(colors='orange')
        self.MplWidget.canvas.draw()

    def start_timer(self):
        print(f"Interval {self.interval}")
        self.timer.start(self.interval)

    # Algorithms
    def insertion_sort(self):
        comparisions = 0
        swaps = 0
        n = len(self.elements)

        for i in range(1, n):
            self.start_timer()
            key = self.elements[i]
            j = i - 1
            while j >= 0 and self.elements[j] > key:
                self.elements[j + 1] = self.elements[j]
                j -= 1
                comparisions += 1
                swaps += 1
            self.elements[j + 1] = key
            swaps += 1
            event_loop = QEventLoop()
            self.timer.timeout.connect(functools.partial(self.update, j+1, i, comparisions))
            self.timer.timeout.connect(event_loop.quit)
            event_loop.exec_()
            print(self.elements)
        self.visualize(None, None)
        print(comparisions, swaps)
        self.complex_lbl.setText(f"Karmaşıklık Analizi: {comparisions+swaps+1}")
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisions}")

    def bubble_sort(self):
        comparisions = 0
        swaps = 0
        n = len(self.elements)

        for i in range(n - 1):
            for j in range(n - 1 -i):
                self.start_timer()
                if self.elements[j] > self.elements[j + 1]:
                    self.elements[j], self.elements[j + 1] = self.elements[j + 1], self.elements[j]
                    swaps += 1
                    event_loop = QEventLoop()
                    self.timer.timeout.connect(functools.partial(self.update, j, j + 1, comparisions))
                    self.timer.timeout.connect(event_loop.quit)
                    event_loop.exec_()
                    print(self.elements)
                comparisions += 1
        self.visualize(None, None)
        print(comparisions, swaps)
        self.complex_lbl.setText(f"Karmaşıklık Analizi: {comparisions + swaps + 1}")
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisions}")

    def visualize(self, x, y):
        colors = ['green' if i == x else 'red' if i == y else 'orange' for i in range(len(self.elements))]
        self.MplWidget.canvas.axes.clear()
        self.plot = self.graph_map(colors)
        self.MplWidget.canvas.draw()

    def merge_sort(self, arr, start=0, end=None):
        if end is None:
            end = len(arr) - 1
        comparisons = 0
        swaps = 0

        if start < end:
            mid = (start + end) // 2
            comparisons += self.merge_sort(arr, start, mid)
            comparisons += self.merge_sort(arr, mid + 1, end)

            i = start
            j = mid + 1
            k = start
            x = -1
            y = -1

            while i <= mid and j <= end:
                self.timer.start()
                comparisons += 1
                if arr[i] < arr[j]:
                    if x != -1:
                        y = j
                    i += 1
                else:
                    if x == -1:
                        x = i
                    y = j
                    temp = arr[j]
                    for k in range(j, i - 1, -1):
                        arr[k] = arr[k - 1]
                    arr[i] = temp
                    swaps += 1
                    i += 1
                    mid += 1
                    j += 1

                event_loop = QEventLoop()
                self.timer.timeout.connect(functools.partial(self.update, x, y, comparisons))
                self.timer.timeout.connect(event_loop.quit)
                event_loop.exec_()

            self.visualize(-1, -1)

            while i <= mid:
                self.timer.start()
                comparisons += 1
                if x != -1:
                    y = i
                event_loop = QEventLoop()
                self.timer.timeout.connect(functools.partial(self.update, x, y, comparisons))
                self.timer.timeout.connect(event_loop.quit)
                event_loop.exec_()
                i += 1

            while j <= end:
                self.timer.start()
                comparisons += 1
                if x == -1:
                    x = j
                y = j
                event_loop = QEventLoop()
                self.timer.timeout.connect(functools.partial(self.update, x, y, comparisons))
                self.timer.timeout.connect(event_loop.quit)
                event_loop.exec_()
                j += 1

        self.visualize(None, None)
        self.complex_lbl.setText(f"Karmaşıklık Analizi: {comparisons + swaps + 1}")
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisons}")
        return comparisons

    def selection_sort(self):
        comparisions = 0
        swaps = 0
        n = len(self.elements)

        for i in range(n - 1):
            self.start_timer()
            min_index = i
            for j in range(i+1, n):
                if self.elements[j] < self.elements[min_index]:
                    min_index = j
                comparisions += 1
            self.elements[i], self.elements[min_index] = self.elements[min_index], self.elements[i]
            swaps += 1
            event_loop = QEventLoop()
            self.timer.timeout.connect(functools.partial(self.update, i, min_index, comparisions))
            self.timer.timeout.connect(event_loop.quit)
            event_loop.exec_()
            print(self.elements)
        print(comparisions, swaps)
        self.complex_lbl.setText(f"Karmaşıklık Analizi: {comparisions + swaps + 1}")
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisions}")

    def partition(self, low, high):
        pivot = self.elements[high]
        i = low - 1
        comparisions = 0
        swaps = 0

        for j in range(low, high):
            self.timer.start()
            if self.elements[j] <= pivot:
                i = i + 1
                (self.elements[i], self.elements[j]) = (self.elements[j], self.elements[i])
                swaps += 1
                self.update(i, j, comparisions)
            comparisions += 1
        (self.elements[i + 1], self.elements[high]) = (self.elements[high], self.elements[i + 1])
        event_loop = QEventLoop()
        self.timer.timeout.connect(functools.partial(self.update, i, high, comparisions))
        self.timer.timeout.connect(event_loop.quit)
        event_loop.exec_()
        swaps += 1
        return i + 1, comparisions, swaps

    def quick_sort(self, low, high):
        comparisions = 0
        swaps = 0
        if low < high:
            pi, comp, swap = self.partition(low, high)
            self.quick_sort(low, pi-1)
            self.quick_sort(pi+1, high)
            comparisions += comp
            swaps += swap

        self.visualize(None, None)
        print(comparisions, swaps)
        self.complex_lbl.setText(f"Karmaşıklık Analizi: {comparisions + swaps + 1}")
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisions}")

    def update(self, x, y, comparisions):
        self.visualize(x, y)
        self.MplWidget.repaint()
        self.count_lbl.setText(f"Karşılaştırma Sayısı: {comparisions}")

    def visualize(self, x, y):
        colors = ['green' if i == x else 'red' if i == y else 'orange' for i in range(len(self.elements))]
        self.MplWidget.canvas.axes.clear()
        self.plot = self.graph_map(colors)
        self.MplWidget.canvas.draw()

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start()
