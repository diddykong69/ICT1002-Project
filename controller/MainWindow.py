import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
sys.path.insert(0, os.path.abspath('./../ui/'))
sys.path.insert(0, os.path.abspath('./../modules/'))
sys.path.insert(0, os.path.abspath('./../model/'))
from modules.reader import *
from modules.thread import *
from modules.writer import *
from modules.data_to_information import data_to_information
from modules.filter import search_data_frame
from model.DataModel import *
from ui.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, title, dimensions):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.log_file_name = self.features_file_name = self.data = self.search_data = self.categories = self.read_success = ''
        self.file_readers = {
            ".csv": read_csv,
            ".xlsx": read_xlsx,
            "": self.none_reader
        }

        self.model = DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(pd.DataFrame([["No file selected."]]))
        self.thread_pool = QThreadPool()

        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)

        self.log_button.pressed.connect(self.open_log_file)
        self.features_button.pressed.connect(self.open_features_file)
        self.read_button.pressed.connect(self.read_button_clicked)
        self.export_results_button.pressed.connect(self.export_search_results)
        self.export_stats_button.triggered.connect(self.export_stats_button_clicked)
        self.search_button.pressed.connect(self.search_log)

        self.data_table.setSortingEnabled(True)
        self.search_table.setSortingEnabled(True)
        self.initial_ui_state()

        self.setGeometry(*dimensions)
        self.setWindowIcon(QIcon(os.path.abspath('./../icon.png')))
        self.setWindowTitle(title)

    # Setter method for model
    def set_model(self, model):
        self.model = model

    def initial_ui_state(self):
        self.set_all_buttons(False)
        self.set_tabs(False)
        self.set_buttons((self.log_button, self.features_button, self.read_button))

    def after_read(self):
        self.set_all_buttons()
        self.set_tabs()

    @staticmethod
    def set_buttons(buttons, enable=True):
        for button in buttons:
            button.setEnabled(enable)

    def set_all_buttons(self, enable=True):
        self.log_button.setEnabled(enable)
        self.features_button.setEnabled(enable)
        self.read_button.setEnabled(enable)
        self.export_results_button.setEnabled(enable)
        self.search_button.setEnabled(enable)
        self.export_stats_button.setEnabled(enable)

    def set_tabs(self, enable=True):
        non_current_tabs = list(filter(lambda x: x != self.tabWidget.currentIndex(),
                                       range(self.tabWidget.count())))
        for tab in non_current_tabs:
            self.tabWidget.setTabEnabled(tab, enable)

    def edit_search_result_label(self, message):
        current_label_text = self.search_result_label.text().split(': ')
        current_label_text[-1] = message
        self.search_result_label.setText(": ".join(current_label_text))

    @pyqtSlot()
    def open_file_name_dialog(self, label, file_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(QFileDialog(), "Select %s File" % file_type, "",
                                                   "CSV Files (*.csv)",
                                                   options=options)
        if file_name:
            label.setText(os.path.basename(file_name))
            label.adjustSize()
        return file_name or ''

    @pyqtSlot()
    def save_file_dialog(self, file_type, file_ext):
        file_exts = {
            'csv': 'CSV Files (*.csv)',
            'xlsx': 'Excel Files (*.xlsx)'
        }
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(QFileDialog(), "Select %s File" % file_type, "",
                                                   file_exts.get(file_ext, 'All Files (*.csv *.xlsx)'),
                                                   options=options)
        return file_name or ''

    @pyqtSlot()
    def open_log_file(self):
        self.log_file_name = self.open_file_name_dialog(self.log_label, "Log")

    @pyqtSlot()
    def open_features_file(self):
        self.features_file_name = self.open_file_name_dialog(self.features_label, "Features")

    @staticmethod
    def none_reader(log, features):
        return None, None, None

    @staticmethod
    def read(reader, log, features):
        return reader(log, features)

    # Function to handle read_file_click
    @pyqtSlot()
    def read_button_clicked(self):
        log_file_name = self.log_file_name
        features_file_name = self.features_file_name

        if log_file_name != "" and features_file_name != "":
            self.model = DataModel(pd.DataFrame([["Reading data..."]]))
            self.search_model = DataModel(pd.DataFrame([["Reading data..."]]))
            self.data_table.setModel(self.model)
            self.search_table.setModel(self.search_model)
            self.set_all_buttons(False)
            log_ext = os.path.splitext(log_file_name)[1]
            # features_ext = os.path.splitext(self._features_file_name)
            self.create_worker(self.read, ({
                    ".csv": read_csv,
                    ".xlsx": read_xlsx,
                    "": self.none_reader
                }.get(log_ext),
                log_file_name,
                features_file_name), self.show_read_data)
        else:
            QMessageBox.warning(QMessageBox(), "Read Log Error",
                                "Please select a log file and a features (header describing log) file",
                                QMessageBox.Ok)

    def show_read_data(self, data):
        self.data, self.categories, self.read_success = data
        self.search_data = self.data.copy()
        self.model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(data=self.search_data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)
        self.set_all_buttons()
        self.set_tabs()

    @staticmethod
    def calculate_stats(stats_func, data, stats_file_name):
        return stats_func(data, stats_file_name)

    def display_export_stats_status(self, results):
        self.set_all_buttons()
        success = results
        if success:
            QMessageBox.information(QMessageBox(), "Export Statistics Success",
                                    "Statistics successfully exported",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(QMessageBox(), "Export Statistics Failure",
                                "Statistics could not be exported successfully. Try again later.")

    @pyqtSlot()
    def export_stats_button_clicked(self):
        stats_file_name = self.save_file_dialog('Export Statistics', 'xlsx')
        data_to_information(self.data, stats_file_name + '.xlsx')
        self.set_all_buttons()
        self.set_buttons((self.log_button, self.features_button, self.read_button), False)
        self.create_worker(self.calculate_stats,
                           (data_to_information, self.data, os.path.splitext(stats_file_name)[0] + '.xlsx'),
                           self.display_export_stats_status)

    @staticmethod
    def search(search_func, data_set, search_term):
        return pd.DataFrame(search_func(data_set, search_term))

    def display_search_results(self, results):
        if not results.empty:
            results.columns = self.categories.tolist()
            self.search_model = DataModel(data=results)
            search_result_message = 'Search term \'%s\' returned %d results.' % \
                                     (self.search_textedit.text(), self.search_model.get_data().shape[0])
        else:
            self.search_model = DataModel(data=self.data)
            search_result_message = '\'%s\' was not found in data-set.' % self.search_textedit.text()
        self.search_table.setModel(self.search_model)
        self.edit_search_result_label(search_result_message)
        self.set_all_buttons()
        self.set_tabs()

    # Handle click of search button
    @pyqtSlot()
    def search_log(self):
        search_term = self.search_textedit.text()
        if search_term == '':
            self.search_model = DataModel(data=self.search_data)
            self.search_table.setModel(self.search_data)
            self.edit_search_result_label('Table Reset Success. You are now viewing the entire data set.')
            return
        self.search_table.setModel(self.search_model)
        self.set_all_buttons(False)
        self.set_buttons((self.export_stats_button,))
        self.set_tabs(False)

        self.search_model = DataModel(pd.DataFrame([["Searching data..."]]))
        self.create_worker(self.search, (search_data_frame, self.data, search_term), self.display_search_results)

    @staticmethod
    def start_export_search_results(export_search_results_func, search_results, file_name):
        return export_search_results_func(search_results, file_name)

    def display_export_search_results_status(self, write_success):
        export_message = 'Export Success' if write_success else 'Export Failed'
        self.edit_search_result_label(export_message)
        self.set_all_buttons()
        self.set_tabs()

    @pyqtSlot()
    def export_search_results(self):
        export_file_name = self.save_file_dialog('Export Results', 'csv')
        # print("Export File Name for Exporting Search Results: ", export_file_name)
        self.set_all_buttons(False)
        self.set_buttons((self.export_stats_button,))
        self.set_tabs(False)
        self.create_worker(self.start_export_search_results,
                           (write_csv, self.search_model.get_data(), os.path.splitext(export_file_name)[0]),
                           self.display_export_search_results_status)

    # Generic thread related functions
    def create_worker(self, func, arguments, result_func):
        worker = Worker(func, arguments)
        worker.signals.result.connect(result_func)
        worker.signals.finished.connect(self.thread_complete)
        worker.setAutoDelete(True)
        self.thread_pool.start(worker)

    def thread_complete(self):
        self.thread_pool.clear()

    def closeEvent(self, event):
        exit_confirm = QMessageBox.question(QMessageBox(), "Confirm Exit?",
                                            "Are you sure you want to quit the program?",
                                            QMessageBox.Yes | QMessageBox.No)  # , defaultButton=QMessageBox.No
        if exit_confirm == QMessageBox.Yes:
            print("Quitting application.")
            event.accept()
        else:
            event.ignore()
