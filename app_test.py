import pytest
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from app import MainWindow


@pytest.fixture
def app(qtbot):
    test_app = QApplication.instance() or QApplication([])
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window


def test_preprocess_function_string():
    main_window = MainWindow()

    # Test replacing implicit multiplication
    func_str = "3x + 2"
    expected = "3*x + 2"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing power operator
    func_str = "x^2"
    expected = "x**2"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing log10
    func_str = "log10(x)"
    expected = "np.log10(x)"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing sqrt
    func_str = "sqrt(x)"
    expected = "np.sqrt(x)"
    assert main_window.preprocess_function_string(func_str) == expected
    # Close the application window
    main_window.close()

def test_plot_function(app, qtbot):
    main_window = app

    # Test plotting a simple function
    qtbot.keyClicks(main_window.function_input, "x**2")
    qtbot.keyClicks(main_window.min_x_input, "-10")
    qtbot.keyClicks(main_window.max_x_input, "10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the plot to update

    assert main_window.error_label.text() == ""  # Check no error
    # Check if a line was plotted
    assert len(main_window.canvas.axes.lines) > 0

    # Test invalid range (min_x >= max_x)
    main_window.function_input.clear()
    main_window.min_x_input.clear()
    main_window.max_x_input.clear()

    qtbot.keyClicks(main_window.function_input, "x**2")
    qtbot.keyClicks(main_window.min_x_input, "10")
    qtbot.keyClicks(main_window.max_x_input, "-10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the error message to update

    assert main_window.error_label.text(
    ) == "Min x should be less than Max x"  # Check error message
    # Close the application window
    qtbot.mouseClick(main_window, Qt.LeftButton)
    main_window.close()
    qtbot.wait(1000)


def test_plot_constant_function(app, qtbot):
    main_window = app

    # Test plotting a constant function
    qtbot.keyClicks(main_window.function_input, "5")
    qtbot.keyClicks(main_window.min_x_input, "0")
    qtbot.keyClicks(main_window.max_x_input, "10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the plot to update

    assert main_window.error_label.text() == ""  # Check no error
    # Check if a line was plotted
    assert len(main_window.canvas.axes.lines) > 0

    # Close the application window
    qtbot.mouseClick(main_window, Qt.LeftButton)
    main_window.close()
    qtbot.wait(1000)
