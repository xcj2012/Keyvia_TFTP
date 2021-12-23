# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Energy.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(887, 413)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_port = QtWidgets.QComboBox(Dialog)
        self.comboBox_port.setObjectName("comboBox_port")
        self.horizontalLayout.addWidget(self.comboBox_port)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_rate = QtWidgets.QComboBox(Dialog)
        self.comboBox_rate.setObjectName("comboBox_rate")
        self.horizontalLayout.addWidget(self.comboBox_rate)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.comboBox_data = QtWidgets.QComboBox(Dialog)
        self.comboBox_data.setObjectName("comboBox_data")
        self.horizontalLayout.addWidget(self.comboBox_data)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBox_var = QtWidgets.QComboBox(Dialog)
        self.comboBox_var.setObjectName("comboBox_var")
        self.horizontalLayout.addWidget(self.comboBox_var)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.comboBox_stop = QtWidgets.QComboBox(Dialog)
        self.comboBox_stop.setObjectName("comboBox_stop")
        self.horizontalLayout.addWidget(self.comboBox_stop)
        self.pushButton_file = QtWidgets.QPushButton(Dialog)
        self.pushButton_file.setObjectName("pushButton_file")
        self.horizontalLayout.addWidget(self.pushButton_file)
        self.pushButton_start = QtWidgets.QPushButton(Dialog)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_stop = QtWidgets.QPushButton(Dialog)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout.addWidget(self.pushButton_stop)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_clear = QtWidgets.QPushButton(Dialog)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout_2.addWidget(self.pushButton_clear)
        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_2.addWidget(self.pushButton_save)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "串口"))
        self.label_2.setText(_translate("Dialog", "波特率"))
        self.label_5.setText(_translate("Dialog", "数据"))
        self.label_3.setText(_translate("Dialog", "校验"))
        self.label_4.setText(_translate("Dialog", "停止"))
        self.pushButton_file.setText(_translate("Dialog", "文件"))
        self.pushButton_start.setText(_translate("Dialog", "开始"))
        self.pushButton_stop.setText(_translate("Dialog", "停止"))
        self.pushButton_clear.setText(_translate("Dialog", "清空"))
        self.pushButton_save.setText(_translate("Dialog", "另存"))
