from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QStackedLayout, QWidget, QApplication, QLineEdit, QPushButton, QLabel, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import numpy as np
import re
from PySide2.QtGui import QPalette, QColor, QIcon, QFont


class MplCanvas(FigureCanvas):
    """
    A Matplotlib canvas that integrates with Qt.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title("Function Plot")
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("F(x)")

        super(MplCanvas, self).__init__(fig)


def set_style_and_font(widget, height=30, backgroundActive=True):
    """
    Apply custom style and font to a Qt widget.

    Args:
        widget (QWidget): The widget to style.
        height (int): The height of the widget.
        backgroundActive (bool): Whether to apply a background color.
    """
    custom_font = QFont("", 12, QFont.Light)

    if backgroundActive:
        widget.setStyleSheet(
            "height: {}; color: black; background: white;".format(height))
    else:
        widget.setStyleSheet(
            "height: {}; color: black;".format(height))
    widget.setFont(custom_font)


class MainWindow(QMainWindow):
    """
    The main window of the application, providing the GUI for function plotting.
    """

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

        # Input fields and plotting button
        self.function_input = QLineEdit()
        self.min_x_input = QLineEdit()
        self.max_x_input = QLineEdit()
        self.plot_button = QPushButton("Plot")
        self.error_label = QLabel("")
        self.function_label = QLabel("Function f(x):")
        self.min_x_label = QLabel("Min x:")
        self.max_x_label = QLabel("Max x:")

        # Apply custom style and font to widgets
        set_style_and_font(self.function_input)
        set_style_and_font(self.min_x_input)
        set_style_and_font(self.max_x_input)
        set_style_and_font(self.plot_button, height=30)
        set_style_and_font(self.error_label, backgroundActive=False)
        set_style_and_font(self.function_label, backgroundActive=False)
        set_style_and_font(self.min_x_label, backgroundActive=False)
        set_style_and_font(self.max_x_label, backgroundActive=False)

        # Create and set up the layout for the form
        form_layout = QFormLayout()
        form_layout.addRow(self.function_label, self.function_input)
        form_layout.addRow(self.min_x_label, self.min_x_input)
        form_layout.addRow(self.max_x_label, self.max_x_input)
        form_layout.addRow(self.plot_button)
        form_layout.addRow(self.error_label)

        # Create the Matplotlib canvas and toolbar
        self.canvas = MplCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: white;")

        # Create main layout
        main_layout = QStackedLayout()

        # Container widget with background color
        color_container = QWidget()
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

        # Connect the plot button click event to the plotting function
        self.plot_button.clicked.connect(self.plot_function)

    def preprocess_function_string(self, func_str):
        """
        Preprocess the function string to replace unsupported syntax with supported ones.

        Args:
            func_str (str): The function string input by the user.

        Returns:
            str: The preprocessed function string.
        """
        # Replace implicit multiplication (e.g., 3x to 3*x)
        func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)

        # Replace operators and functions
        func_str = func_str.replace("^", "**")
        func_str = func_str.replace("log10", "np.log10")
        func_str = func_str.replace("sqrt", "np.sqrt")

        return func_str

    def plot_function(self):
        """
        Plot the function based on the user input and update the canvas.
        """
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

            # Handle constant functions
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


# Create the application and main window
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
