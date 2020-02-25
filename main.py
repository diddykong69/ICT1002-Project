import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
sys.path.insert(0, os.path.abspath('./ui/'))
sys.path.insert(0, os.path.abspath('./modules/'))
sys.path.insert(0, os.path.abspath('./model/'))
from modules.reader import *
from modules.thread import *
from modules.writer import *
from model.DataModel import *
from ui.MainWindow import Ui_MainWindow

TITLE = "GOTCHA"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, title, dimensions):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(pd.DataFrame([["No file selected."]]))
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.data_table.setSortingEnabled(True)
        self.set_tabs(False)

        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)

        self.log_file_name = self.features_file_name = self.data = self.categories = self.read_success = ''
        self.file_readers = {
            ".csv": read_csv,
            ".xlsx": read_xlsx,
            "": self.none_reader
        }

        self.log_button.pressed.connect(self.open_log_file)
        self.features_button.pressed.connect(self.open_features_file)
        self.read_button.pressed.connect(self.read_file)
        self.export_results_button.pressed.connect(self.export_file)

        self.setGeometry(*dimensions)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle(title)

    def set_model(self, model):
        self.model = model

    @pyqtSlot()
    def export_file(self):
        export_file_name = self.save_file_dialog()
        write_success = write_csv(self.search_model.get_data(), os.path.splitext(export_file_name)[0])
        export_message = 'Export Success' if write_success else 'Export Failed'
        current_label_text = self.search_result_label.text().split()
        current_label_text[-1] = export_message
        self.search_result_label.setText(" ".join(current_label_text))

    @pyqtSlot()
    def open_log_file(self):
        self.log_file_name = self.open_file_name_dialog(self.log_label, "Log")

    @pyqtSlot()
    def open_features_file(self):
        self.features_file_name = self.open_file_name_dialog(self.features_label, "Features")

    @pyqtSlot()
    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(QFileDialog(), "Select Export File", "", "CSV Files (*.csv)", options=options)
        return file_name or ''

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
        return file_name or ''

    @staticmethod
    def none_reader(log, features):
        return None, None, None

    @staticmethod
    def read(reader, log, features):
        return reader(log, features)

    def show_data(self, data):
        self.data, self.categories, self.read_success = data
        self.model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)
        self.set_all_buttons()
        self.set_tabs()

    @staticmethod
    def thread_complete():
        print('Thread complete.')

    def set_all_buttons(self, enable=True):
        self.log_button.setEnabled(enable)
        self.features_button.setEnabled(enable)
        self.read_button.setEnabled(enable)

    def set_tabs(self, enable=True):
        self.tabWidget.setTabEnabled(1, enable)
        self.tabWidget.setTabEnabled(2, enable)

    @pyqtSlot()
    def read_file(self):
        self.model = DataModel(pd.DataFrame([["Reading data..."]]))
        self.search_model = DataModel(pd.DataFrame([["Reading data..."]]))
        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)
        self.set_all_buttons(False)
        log_file_name = self.log_file_name
        features_file_name = self.features_file_name
        if log_file_name != "" and features_file_name != "":
            log_ext = os.path.splitext(log_file_name)[1]
            # features_ext = os.path.splitext(self._features_file_name)
            worker = Worker(self.read, (
                self.file_readers.get(log_ext),
                log_file_name,
                features_file_name))
            worker.signals.result.connect(self.show_data)
            worker.signals.finished.connect(self.thread_complete)
            self.threadpool.start(worker)

    def closeEvent(self, event):
        exit_confirm = QMessageBox.question(self, "Confirm Exit?",
                                            "Are you sure you want to quit the program?",
                                            QMessageBox.Yes | QMessageBox.No)
        if exit_confirm == QMessageBox.Yes:
            print("Quitting application.")
            event.accept()
        else:
            event.ignore()


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


# window = MainWindow()
window.show()

sys.exit(app.exec_())
