# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.features_button = QtWidgets.QPushButton(self.centralwidget)
        self.features_button.setObjectName("features_button")
        self.gridLayout.addWidget(self.features_button, 5, 2, 1, 1)
        self.log_button = QtWidgets.QPushButton(self.centralwidget)
        self.log_button.setObjectName("log_button")
        self.gridLayout.addWidget(self.log_button, 3, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.features_label = QtWidgets.QLabel(self.centralwidget)
        self.features_label.setObjectName("features_label")
        self.gridLayout.addWidget(self.features_label, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        self.log_label = QtWidgets.QLabel(self.centralwidget)
        self.log_label.setObjectName("log_label")
        self.gridLayout.addWidget(self.log_label, 3, 1, 1, 1)
        self.read_button = QtWidgets.QPushButton(self.centralwidget)
        self.read_button.setObjectName("read_button")
        self.gridLayout.addWidget(self.read_button, 6, 1, 1, 2)
        self.data_table = QtWidgets.QTableView(self.centralwidget)
        self.data_table.setObjectName("data_table")
        self.gridLayout.addWidget(self.data_table, 0, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        self.menu_options = QtWidgets.QMenu(self.menubar)
        self.menu_options.setObjectName("menu_options")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.search_log = QtWidgets.QAction(MainWindow)
        self.search_log.setObjectName("search_log")
        self.menu_options.addAction(self.search_log)
        self.menubar.addAction(self.menu_options.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GOTCHA"))
        self.features_button.setText(_translate("MainWindow", "Select Features File"))
        self.log_button.setText(_translate("MainWindow", "Select Log File"))
        self.features_label.setText(_translate("MainWindow", "No features file selected."))
        self.log_label.setText(_translate("MainWindow", "No log file selected."))
        self.read_button.setText(_translate("MainWindow", "Read Log File"))
        self.menu_options.setTitle(_translate("MainWindow", "Options"))
        self.search_log.setText(_translate("MainWindow", "Search Log"))
