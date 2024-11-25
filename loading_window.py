import sys
from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class TaskThread(QThread):
    finished = pyqtSignal()  # Signal emitted when the task is complete

    def __init__(self, task, *args, **kwargs):
        super().__init__()
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def run(self):
        # Execute the task function with its arguments
        if self.task:
            self.task(*self.args, **self.kwargs)
        self.finished.emit()  # Notify when the task is complete


class LoadingApp:
    def __init__(self, task=None, *task_args, **task_kwargs):
        self.app = QApplication(sys.argv)
        self.progress_dialog = None
        self.task_thread = TaskThread(task, *task_args, **task_kwargs)

    def show_loading_indicator(self, title: str, content: str):
        # Create a QProgressDialog with an indeterminate progress bar
        self.progress_dialog = QProgressDialog(content, None, 0, 0)
        self.progress_dialog.setFixedWidth(250)
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)  # Block interaction with other windows
        self.progress_dialog.setMinimumDuration(0)  # Show immediately
        self.progress_dialog.setCancelButton(None)  # Remove cancel button
        self.progress_dialog.setWindowIcon(QIcon(str(Path(__file__).parent / "pandasgui/resources/images/icon.ico")))
        # Remove the question mark
        self.progress_dialog.setWindowFlags(self.progress_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.progress_dialog.show()

        # Start the worker thread
        self.task_thread.finished.connect(self.stop_loading_indicator)
        self.task_thread.start()

    def stop_loading_indicator(self):
        if self.progress_dialog:
            self.progress_dialog.close()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    # Example of a task function
    def example_task():
        for i in range(99999999):
            if i % 1000000 == 0:
                print(i)

    loading_app = LoadingApp(task=example_task)
    loading_app.show_loading_indicator("Starting DataViewer", "Fetching data, please wait...")
    sys.exit(loading_app.app.exec_())
