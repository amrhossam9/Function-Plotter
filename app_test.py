import pytest
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from app import MainWindow


@pytest.fixture
def app(qtbot):
    """
    Pytest fixture to set up the application and main window for testing.

    Args:
        qtbot: The Qt testing helper provided by pytest-qt.

    Returns:
        MainWindow: An instance of the main application window.
    """
    test_app = QApplication.instance() or QApplication([])
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window


def test_preprocess_function_string():
    """
    Test the preprocessing of the function string to ensure correct syntax replacement.
    """
    main_window = MainWindow()

    # Test replacing implicit multiplication (e.g., 3x to 3*x)
    func_str = "3x + 2"
    expected = "3*x + 2"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing the power operator (e.g., x^2 to x**2)
    func_str = "x^2"
    expected = "x**2"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing log10 with np.log10
    func_str = "log10(x)"
    expected = "np.log10(x)"
    assert main_window.preprocess_function_string(func_str) == expected

    # Test replacing sqrt with np.sqrt
    func_str = "sqrt(x)"
    expected = "np.sqrt(x)"
    assert main_window.preprocess_function_string(func_str) == expected

    # Close the application window
    main_window.close()


def test_plot_function(app, qtbot):
    """
    Test the function plotting capability of the application.

    Args:
        app: The main application window instance provided by the fixture.
        qtbot: The Qt testing helper provided by pytest-qt.
    """
    main_window = app

    # Test plotting a simple quadratic function (x**2)
    qtbot.keyClicks(main_window.function_input, "x**2")
    qtbot.keyClicks(main_window.min_x_input, "-10")
    qtbot.keyClicks(main_window.max_x_input, "10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the plot to update

    assert main_window.error_label.text() == ""  # Ensure no error message
    assert len(main_window.canvas.axes.lines) > 0  # Ensure a line was plotted

    # Test invalid range where min_x >= max_x
    main_window.function_input.clear()
    main_window.min_x_input.clear()
    main_window.max_x_input.clear()

    qtbot.keyClicks(main_window.function_input, "x**2")
    qtbot.keyClicks(main_window.min_x_input, "10")
    qtbot.keyClicks(main_window.max_x_input, "-10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the error message to update

    # Check for the correct error message
    assert main_window.error_label.text() == "Min x should be less than Max x"

    # Close the application window
    main_window.close()
    qtbot.wait(1000)


def test_plot_constant_function(app, qtbot):
    """
    Test plotting a constant function.

    Args:
        app: The main application window instance provided by the fixture.
        qtbot: The Qt testing helper provided by pytest-qt.
    """
    main_window = app

    # Test plotting a constant function (y = 5)
    qtbot.keyClicks(main_window.function_input, "5")
    qtbot.keyClicks(main_window.min_x_input, "0")
    qtbot.keyClicks(main_window.max_x_input, "10")

    qtbot.mouseClick(main_window.plot_button, Qt.LeftButton)
    qtbot.wait(1000)  # Wait for the plot to update

    assert main_window.error_label.text() == ""  # Ensure no error message
    assert len(main_window.canvas.axes.lines) > 0  # Ensure a line was plotted

    # Close the application window
    main_window.close()
    qtbot.wait(1000)
