import sys
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

sys.path.insert(0, os.path.abspath('./modules/'))
from modules.reader import *

TITLE = "GOTCHA"


# Main GUI class
class MainWindow(QMainWindow):
    def __init__(self, title, dimensions, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.log_file_name = self.features_file_name = self.data = self.categories = self.read_success = ''
        self.file_readers = {
            ".csv": read_csv,
            ".xlsx": read_xlsx,
            "": self.none_reader
        }

        widget = QWidget()
        self.layout = QGridLayout()

        self.log_label = QLabel(widget)
        self.log_label.setText('No file selected.')
        self.log_label.adjustSize()

        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum), 1, 0)
        self.layout.addWidget(self.log_label, 1, 1)

        log_button = self.create_btn('Select Log File', widget, self.open_log_file)
        self.layout.addWidget(log_button, 1, 2)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum), 1, 3)

        self.features_label = QLabel(widget)
        self.features_label.setText('No file selected.')
        self.features_label.adjustSize()

        self.layout.addWidget(self.features_label, 2, 1)

        features_button = self.create_btn('Select Features File', widget, self.open_features_file)
        self.layout.addWidget(features_button, 2, 2)

        read_button = self.create_btn('Read Log File', widget, self.read_file)
        self.layout.addWidget(read_button, 3, 2)

        self.setGeometry(*dimensions)
        widget.showFullScreen()
        widget.setLayout(self.layout)

        self.setWindowTitle(title)
        self.setCentralWidget(widget)

    @staticmethod
    def create_btn(btn_text, widget, function):
        button = QPushButton(btn_text, widget)
        button.setToolTip(btn_text)
        button.clicked.connect(function)
        return button

    @pyqtSlot()
    def open_log_file(self):
        self.log_file_name = self.open_file_name_dialog(self.log_label, "Log")

    @pyqtSlot()
    def open_features_file(self):
        self.features_file_name = self.open_file_name_dialog(self.features_label, "Features")

    @pyqtSlot()
    def open_file_name_dialog(self, label, file_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(QFileDialog(), "Select %s File" % file_type, "",
                                                   "All Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)",
                                                   options=options)
        if file_name:
            label.setText(os.path.basename(file_name))
            label.adjustSize()
        return file_name if file_name else ''

    @staticmethod
    def none_reader(log, features):
        return None, None, None

    @staticmethod
    def read(reader, log, features):
        return reader(log, features)

    @pyqtSlot()
    def read_file(self):
        log_file_name = self.log_file_name
        features_file_name = self.features_file_name
        if log_file_name != "" and features_file_name != "":
            log_ext = os.path.splitext(log_file_name)[1]
            print(log_ext)
            # features_ext = os.path.splitext(self._features_file_name)
            print(self.file_readers.get(log_ext))
            self.data, self.categories, self.read_success = self.read(
                self.file_readers.get(log_ext),
                log_file_name,
                features_file_name)
            if self.read_success:
                print(self.categories)

    def closeEvent(self, event):
        exit_confirm = QMessageBox.question(self, "Confirm Exit?",
                                            "Are you sure you want to quit the program?",
                                            QMessageBox.Yes | QMessageBox.No)
        if exit_confirm == QMessageBox.Yes:
            print("Qutting application.")
            event.accept()
        else:
            event.ignore()


# Create the GUI app
app = QApplication(sys.argv)

# Get screen available size
screen = app.primaryScreen()
available_size = screen.availableSize()
width, height = available_size.width(), available_size.height()

# Size of app: 640 x 480
expected_width, expected_height = 640, 480

# Calculate screen position to
# centralise app
position_x, position_y = (width - expected_width) / 2, (height - expected_height) / 2

# Create the Main Window to add to our
# GUI app
window = MainWindow(TITLE, (position_x, position_y, expected_width, expected_height))

# Show the app
window.show()

# When exiting application, exit
# with the exit status code of GUI app
sys.exit(app.exec_())
