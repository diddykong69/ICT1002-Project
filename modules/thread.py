from PyQt5.QtCore import *


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)


class Worker(QRunnable):
    def __init__(self, func, func_arguments, *args, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.func_arguments = func_arguments
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            arguments = self.func_arguments
            result = self.func(*arguments)
        except:
            self.signals.error.emit(('Error', 'Error'))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
