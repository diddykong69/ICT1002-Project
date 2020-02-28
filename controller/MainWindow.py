"""
Author      : Harish S/O Balamurugan
Description : The "controller" file to handle the GUI interactions and respond accordingly.
              This file also handles the integration of all the various modules.
"""

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
    # Constructor method for MainWindow
    def __init__(self, title, dimensions):
        """
        Constructor method for MainWindow
        :param title: the title of the MainWindow of the GUI
        :param dimensions: the dimensions of the MainWindow of the GUI
        """
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.log_file_name = self.features_file_name = self.data = self.search_data = self.categories = self.read_success = ''

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
        """
        Setter method for model
        :param model: the model to set self.model to
        :return: N.A.
        """
        self.model = model

    # Set the buttons and tabs to initial UI state
    def initial_ui_state(self):
        """
        Set the buttons and tabs to initial UI state
        :return: N.A.
        """
        self.set_all_buttons(False)
        self.set_tabs(False)
        self.set_buttons((self.log_button, self.features_button, self.read_button))

    # Set buttons to enable status
    @staticmethod
    def set_buttons(buttons, enable=True):
        """
        Set buttons to enable status
        :param buttons: The tuple of buttons to set the enable status
        :param enable: Whether to enable buttons (True for enable, False for disable)
        :return: N.A.
        """
        for button in buttons:
            button.setEnabled(enable)

    # Set all buttons to enable status
    def set_all_buttons(self, enable=True):
        """
        Set all buttons to enable status
        :param enable: Whether to enable buttons (True for enable, False for disable)
        :return: N.A.
        """
        self.log_button.setEnabled(enable)
        self.features_button.setEnabled(enable)
        self.read_button.setEnabled(enable)
        self.export_results_button.setEnabled(enable)
        self.search_button.setEnabled(enable)
        self.export_stats_button.setEnabled(enable)

    # Set non-current tabs to enable status
    def set_tabs(self, enable=True):
        """
        Set non-current tabs to enable status
        :param enable: Whether to enable tabs (True for enable, False for disable)
        :return: N.A.
        """
        non_current_tabs = list(filter(lambda x: x != self.tabWidget.currentIndex(),
                                       range(self.tabWidget.count())))
        for tab in non_current_tabs:
            self.tabWidget.setTabEnabled(tab, enable)

    # Edits the search label with message
    def edit_search_result_label(self, message):
        """
        Edits the search label with message
        :param message: The message to write to the search label
        :return: N.A.
        """
        current_label_text = self.search_result_label.text().split(': ')
        current_label_text[-1] = message
        self.search_result_label.setText(": ".join(current_label_text))

    # Opens File Dialog to ask for the file name to read
    @pyqtSlot()
    def open_file_name_dialog(self, label, file_type):
        """
        Opens File Dialog to ask for the file name to read
        :param label: The label to update with the name of the file about to be read
        :param file_type: The text to display on the title of the File Dialog
        :return: file_name The name of the file to read, as requested by the user, or ''
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(QFileDialog(), "Select %s File" % file_type, "",
                                                   "All Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)",
                                                   options=options)
        if file_name:
            label.setText(os.path.basename(file_name))
            label.adjustSize()
        return file_name or ''

    # Opens File Dialog to ask for the file name to save to
    @pyqtSlot()
    def save_file_dialog(self, file_type, file_ext):
        """
        Opens File Dialog to ask for the file name to save to
        :param file_type: Text to display on the title of the File Dialog
        :param file_ext: The file extension to request for
        :return: file_name The name of the file to save to, as requested by the user, or ''
        """
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

    # Handles the click of "Select Log File" button
    @pyqtSlot()
    def open_log_file(self):
        """
        Handles the click of "Select Log File" button
        :return: N.A.
        """
        self.log_file_name = self.open_file_name_dialog(self.log_label, "Log")

    # Handles the click of "Select Features File" button
    @pyqtSlot()
    def open_features_file(self):
        """
        Handles the click of "Select Features File" button
        :return: N.A.
        """
        self.features_file_name = self.open_file_name_dialog(self.features_label, "Features")

    @staticmethod
    def none_reader(log, features):
        return None, None, False

    # Read Files
    # Read Files - Thread input func - read log function for create_worker
    @staticmethod
    def read(reader, log, features):
        """
        Function to be passed to create_worker for read log function
        :param reader: The reader function to read the log and feature file
        :param log: The name of the log file to read
        :param features: The name of the features file to read
        :return: output of reader --> To be accessed by show_read_data
        """
        return reader(log, features)

    # Read Files - Thread output func - display log data read
    def show_read_data(self, data):
        """
        Displays the log data read to the table in GUI
        To be passed to create_worker to handle the output from read
        :param data: The read log data, encapsulated into a pandas DataFrame
        :return: N.A.
        """
        self.data, self.categories, self.read_success = data
        self.search_data = self.data.copy()
        self.model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(data=self.search_data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)
        self.set_all_buttons()
        self.set_tabs()

    # Read Files - Handles the click of "Read Log File" button
    @pyqtSlot()
    def read_button_clicked(self):
        """
        Handles the click of "Read Log File" button
        :return: N.A.
        """
        log_file_name = self.log_file_name
        features_file_name = self.features_file_name

        if log_file_name != "" and features_file_name != "":
            self.model = DataModel(pd.DataFrame([["Reading data..."]]))
            self.search_model = DataModel(pd.DataFrame([["Reading data..."]]))
            self.data_table.setModel(self.model)
            self.search_table.setModel(self.search_model)
            self.set_all_buttons(False)
            log_ext = os.path.splitext(log_file_name)[1]
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

    # Export Statistics
    # Export Statistics - Thread input func - exporting statistics function for create_worker
    @staticmethod
    def export_stats(stats_func, data, stats_file_name):
        """
        Function to be passed to create_worker for exporting statistics function
        :param stats_func: The export statistics function
        :param data: The statistics data to be exported
        :param stats_file_name: Name of the file to export to
        :return: output of stats_func --> To be accessed by display_export_stats_status
        """
        return stats_func(data, stats_file_name)

    # Export Statistics - Thread output func - displays the success status of export statistics operation
    def display_export_stats_status(self, write_success):
        """
        Displays the success status of export statistics operation
        To be passed to create_worker to handle the output from export_stats
        :param write_success: Boolean value indicating status of exporting of statistics.
                              (True for success and False for otherwise)
        :return: N.A.
        """
        self.set_all_buttons()
        if write_success:
            QMessageBox.information(QMessageBox(), "Export Statistics Success",
                                    "Statistics successfully exported",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(QMessageBox(), "Export Statistics Failure",
                                "Statistics could not be exported successfully. Try again later.")

    # Export Statistics - Handles the click of "Export Statistics" button under "Options"
    @pyqtSlot()
    def export_stats_button_clicked(self):
        """
        Handles the click of "Export Statistics" button
        :return: N.A.
        """
        stats_file_name = self.save_file_dialog('Export Statistics', 'xlsx')
        if stats_file_name == '':
            QMessageBox.warning(QMessageBox(), "Export Statistics Failure",
                                "Please select an Excel File if you wish to export statistics related to your data set.")
            return
        self.set_all_buttons()
        self.set_buttons((self.log_button, self.features_button, self.read_button), False)
        self.create_worker(self.export_stats,
                           (data_to_information, self.data, os.path.splitext(stats_file_name)[0] + '.xlsx'),
                           self.display_export_stats_status)

    # Search Results
    # Search Results - Thread input func - search function for create_worker
    @staticmethod
    def search(search_func, data_set, search_term):
        """
        Function to be passed to create_worker for search function
        :param search_func: The search function
        :param data_set: The data_set to search from (See search_data_frame in filter.py)
        :param search_term: The search term to be used in the search (See search_data_frame in filter.py)
        :return: The search results, encapsulated into a pandas DataFrame --> To be accessed by display_search_results
        """
        return pd.DataFrame(search_func(data_set, search_term))

    # Search Results - Thread output func - display search results
    def display_search_results(self, results):
        """
        Displays the search results to the table in GUI
        To be passed to create_worker to handle the output from search
        :param results: The search results, encapsulated into a pandas DataFrame
        :return: N.A.
        """
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

    # Search Results - Handles the click of "Search" button
    @pyqtSlot()
    def search_log(self):
        """
        Handles the click of "Search" button
        :return: N.A.
        """
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

    # Export Search Results
    # Export Search Results - Thread input func - exporting search results function for create_worker
    @staticmethod
    def start_export_search_results(export_search_results_func, search_results, file_name):
        """
        Function to be passed to create_worker for exporting search results function
        :param export_search_results_func: The export search results function
        :param search_results: The search results to be passed to export_search_results_func for export
        :param file_name: Name of the file to export to
        :return: output of export_search_results_func --> To be accessed by display_export_search_results_status
        """
        return export_search_results_func(search_results, file_name)

    # Export Search Results - Thread output func - displays the success status of export search results operation
    def display_export_search_results_status(self, write_success):
        """
        Displays the success status of export search results operation
        To be passed to create_worker to handle the output from start_export_search_results
        :param write_success: Boolean value indicating status of exporting of search results.
                              (True for success and False for otherwise)
        :return: N.A.
        """
        export_message = 'Export Success' if write_success else 'Export Failed'
        self.edit_search_result_label(export_message)
        self.set_all_buttons()
        self.set_tabs()

    # Export Search Results - Handles the click of "Export Results" button in "Search Data" tab
    @pyqtSlot()
    def export_search_results(self):
        """
        Handles the click of "Export Results" button
        :return: N.A.
        """
        export_file_name = self.save_file_dialog('Export Results', 'csv')
        if export_file_name == '':
            QMessageBox.warning(QMessageBox(), "Export Statistics Failure",
                                "Please select an Excel File if you wish to export statistics related to your data set.")
            return
        self.set_all_buttons(False)
        self.set_buttons((self.export_stats_button,))
        self.set_tabs(False)
        self.create_worker(self.start_export_search_results,
                           (write_csv, self.search_model.get_data(), os.path.splitext(export_file_name)[0]),
                           self.display_export_search_results_status)

    # Generic thread related functions
    # Create a new thread to execute a task (function) separately from the main GUI thread
    def create_worker(self, func, arguments, result_func):
        """
        Create a new thread to execute a task (function) separately from the main GUI thread

        This is to avoid the "Not Responding" message that is usually caused by a long
        running process clogging the main GUI process.

        :param func: The name of the function to execute in the new thread
        :param arguments: The *tuple* of arguments to be passed on to the function
        :param result_func: The name of the function to handle the data returned from func
        :return: N.A.
        """
        worker = Worker(func, arguments)
        worker.signals.result.connect(result_func)
        worker.signals.finished.connect(self.thread_complete)
        worker.setAutoDelete(True)
        self.thread_pool.start(worker)

    # Clears up resources once a thread has finished its task
    def thread_complete(self):
        """
        Clears up resources once a thread has finished its task
        :return: N.A.
        """
        self.thread_pool.clear()

    # Handles the Close Event
    def closeEvent(self, event):
        """
        Handles the Close Event
        :param event:
        :return: N.A.
        """
        exit_confirm = QMessageBox.question(QMessageBox(), "Confirm Exit?",
                                            "Are you sure you want to quit the program?",
                                            QMessageBox.Yes | QMessageBox.No)  # , defaultButton=QMessageBox.No
        if exit_confirm == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
