from PyQt5.QtCore import *


class DataModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
        print(self._data)

    def get_data(self):
        return self._data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    @pyqtSlot(int, Qt.Orientation, result=str)
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[section]
            else:
                return str(self._data.index[section])
        return QVariant()

    def sort(self, column, order):
        col_name = self._data.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._data.sort_values(col_name, ascending=order == Qt.AscendingOrder, inplace=True)
        self._data.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
