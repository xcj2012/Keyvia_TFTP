# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Telenet.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(926, 667)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_IP = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.horizontalLayout.addWidget(self.lineEdit_IP)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_Port = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_Port.setObjectName("lineEdit_Port")
        self.horizontalLayout.addWidget(self.lineEdit_Port)
        self.pushButton_Connect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect.setObjectName("pushButton_Connect")
        self.horizontalLayout.addWidget(self.pushButton_Connect)
        self.pushButton_Disconnect = QtWidgets.QPushButton(Dialog)
        self.pushButton_Disconnect.setObjectName("pushButton_Disconnect")
        self.horizontalLayout.addWidget(self.pushButton_Disconnect)
        self.pushButton_Clear = QtWidgets.QPushButton(Dialog)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.horizontalLayout.addWidget(self.pushButton_Clear)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_Connect_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_Connect_2.setObjectName("pushButton_Connect_2")
        self.horizontalLayout_2.addWidget(self.pushButton_Connect_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "IP地址"))
        self.label_2.setText(_translate("Dialog", "端口"))
        self.pushButton_Connect.setText(_translate("Dialog", "连接"))
        self.pushButton_Disconnect.setText(_translate("Dialog", "断开"))
        self.pushButton_Clear.setText(_translate("Dialog", "清空"))
        self.label_3.setText(_translate("Dialog", "命令"))
        self.pushButton_Connect_2.setText(_translate("Dialog", "发送"))
