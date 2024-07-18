from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QStackedLayout, QWidget, QApplication, QLineEdit, QPushButton, QLabel, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import numpy as np
import re
from PySide2.QtGui import QPalette, QColor, QIcon, QFont


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title("Function Plot")
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("F(x)")

        super(MplCanvas, self).__init__(fig)


def set_style_and_font(widget, height=30, backgroundActive=True):
    custom_font = QFont("", 12, QFont.Light)

    if backgroundActive:
        widget.setStyleSheet(
            "height: {}; color: black; background: white;".format(height))
    else:
        widget.setStyleSheet(
            "height: {}; color: black;".format(height))
    widget.setFont(custom_font)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # The app bar title
        self.setWindowTitle("Function Plotter")
        # the app bar icon
        icon = QIcon()
        icon.addFile('icon.png')
        self.setWindowIcon(icon)
        # minimum width for the application
        self.setMinimumWidth(1100)

        # Input fields
        self.function_input = QLineEdit()
        self.min_x_input = QLineEdit()
        self.max_x_input = QLineEdit()
        self.plot_button = QPushButton("Plot")
        self.error_label = QLabel("")
        self.function_label = QLabel("Function f(x):")
        self.min_x_label = QLabel("Min x:")
        self.max_x_label = QLabel("Max x:")

        # customizing
        set_style_and_font(self.function_input)
        set_style_and_font(self.min_x_input)
        set_style_and_font(self.max_x_input)
        set_style_and_font(self.plot_button, height=30)
        set_style_and_font(self.error_label, backgroundActive=False)
        set_style_and_font(self.function_label, backgroundActive=False)
        set_style_and_font(self.min_x_label, backgroundActive=False)
        set_style_and_font(self.max_x_label, backgroundActive=False)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow(self.function_label, self.function_input)
        form_layout.addRow(self.min_x_label, self.min_x_input)
        form_layout.addRow(self.max_x_label, self.max_x_input)
        form_layout.addRow(self.plot_button)
        form_layout.addRow(self.error_label)

        # Canvas and toolbar
        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.toolbar.setStyleSheet("background-color: white;")

        # Layouts
        main_layout = QStackedLayout()

        # Container widget with background color
        color_container = QWidget()
        # color_container.setStyleSheet("background-color: #2E236C;")

        layout1 = QHBoxLayout(color_container)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.toolbar)
        layout2.addWidget(self.canvas)
        layout1.addLayout(form_layout)
        layout1.addLayout(layout2)

        main_layout.addWidget(color_container)

        # Central widget
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Connect button
        self.plot_button.clicked.connect(self.plot_function)

    def preprocess_function_string(self, func_str):
        # Replace implicit multiplication (e.g., 3x to 3*x)
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)

        # Replace operators and functions
        func_str = func_str.replace("^", "**")
        func_str = func_str.replace("log10", "np.log10")
        func_str = func_str.replace("sqrt", "np.sqrt")

        return func_str

    def plot_function(self):
        try:
            # Validate inputs
            func_str = self.function_input.text()
            min_x = float(self.min_x_input.text())
            max_x = float(self.max_x_input.text())
            if min_x >= max_x:
                raise ValueError("Min x should be less than Max x")

            # Parse function string
            func_str = self.preprocess_function_string(func_str)

            # Generate x values and plot
            x = np.linspace(min_x, max_x, 400)
            y = eval(func_str)

            # to handle constants
            if func_str.isnumeric():
                y = np.full(x.shape, y)

            self.canvas.axes.clear()
            self.canvas.axes.grid(True)
            self.canvas.axes.plot(x, y)
            self.canvas.draw()
            self.error_label.setText("")
            self.canvas.cursor = Cursor(
                self.canvas.axes, useblit=True, color='black', linewidth=0.3)

        except Exception as e:
            self.error_label.setText(f"{e}")


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
