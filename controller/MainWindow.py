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
        self.model = DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(pd.DataFrame([["No file selected."]]))
        self.thread_pool = QThreadPool()
        self.data_table.setSortingEnabled(True)
        self.set_tab(1, False)
        self.export_stats_button.setEnabled(False)

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
        self.export_stats_button.triggered.connect(self.export_stats)
        self.search_button.pressed.connect(self.search_log)

        self.setGeometry(*dimensions)
        self.setWindowIcon(QIcon('./../icon.png'))
        self.setWindowTitle(title)

    def set_model(self, model):
        self.model = model

    @pyqtSlot()
    def export_file(self):
        export_file_name = self.save_file_dialog('Export Results', 'csv')
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

    @staticmethod
    def none_reader(log, features):
        return None, None, None

    @staticmethod
    def read(reader, log, features):
        return reader(log, features)

    @pyqtSlot()
    def export_stats(self):
        stats_file_name = self.save_file_dialog('Export Statistics', 'xlsx')
        data_to_information(self.data, stats_file_name)

    def show_data(self, data):
        self.data, self.categories, self.read_success = data
        self.model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.search_model = DataModel(data=self.data) if self.read_success else DataModel(pd.DataFrame([["No file selected."]]))
        self.data_table.setModel(self.model)
        self.search_table.setModel(self.search_model)
        self.set_all_buttons()
        self.set_tab(1)
        self.export_stats_button.setEnabled(True)

    @staticmethod
    def thread_complete():
        pass

    def search(self, search_func, data_set, search_term):
        return pd.DataFrame(search_func(data_set, search_term))
        # if search_term == '':
        #     search_results = self.data
        # else:
        #     search_results = pd.DataFrame(search_data_frame(self.search_model.get_data(), search_term))
        #     search_results.columns = self.categories.iloc[:, 1].tolist()
        # # print(search_results)
        # # print(search_results)
        # return {'results': search_results, 'search_term': search_term}

    def display_search_results(self, results):
        current_label_text = self.search_result_label.text().split()
        if not results.empty:
            results.columns = self.categories.tolist()
            self.search_model = DataModel(data=results)
            current_label_text[-1] = 'Search Success - Search term \'%s\' yield %d results.' % \
                                     (self.search_textedit.toPlainText(), self.search_model.get_data().shape[0])
        else:
            self.search_model = DataModel(data=self.data)
            current_label_text[-1] = 'Search Failure - \'%s\' was not found in data-set.' % self.search_textedit.toPlainText()
        self.search_table.setModel(self.search_model)
        self.search_result_label.setText(" ".join(current_label_text))
        self.set_all_buttons()
        self.set_tab(0)

    @pyqtSlot()
    def search_log(self):
        search_term = self.search_textedit.toPlainText()
        if search_term == '':
            self.search_model = DataModel(data=self.data)
            self.search_table.setModel(self.search_model)
            current_label_text = self.search_result_label.text().split()
            current_label_text[-1] = 'Table Reset Success'
            self.search_result_label.setText(" ".join(current_label_text))
            return

        self.search_model = DataModel(pd.DataFrame([["Reading data..."]]))
        self.search_table.setModel(self.search_model)
        self.set_all_buttons(False)
        self.set_tab(0, False)

        worker2 = Worker(self.search, (search_data_frame, self.data, search_term))
        worker2.signals.result.connect(self.display_search_results)
        worker2.signals.finished.connect(self.thread_complete)
        self.thread_pool.start(worker2)

    def set_all_buttons(self, enable=True):
        self.log_button.setEnabled(enable)
        self.features_button.setEnabled(enable)
        self.read_button.setEnabled(enable)
        self.export_results_button.setEnabled(enable)
        self.search_button.setEnabled(enable)

    def set_tab(self, tab_num, enable=True):
        self.tabWidget.setTabEnabled(tab_num, enable)

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
            self.thread_pool.start(worker)

    def closeEvent(self, event):
        exit_confirm = QMessageBox.question(self, "Confirm Exit?",
                                            "Are you sure you want to quit the program?",
                                            QMessageBox.Yes | QMessageBox.No)
        if exit_confirm == QMessageBox.Yes:
            print("Quitting application.")
            event.accept()
        else:
            event.ignore()
