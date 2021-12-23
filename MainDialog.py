# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(591, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_Browse = QtWidgets.QPushButton(Dialog)
        self.pushButton_Browse.setObjectName("pushButton_Browse")
        self.horizontalLayout_2.addWidget(self.pushButton_Browse)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_Telnet = QtWidgets.QPushButton(Dialog)
        self.pushButton_Telnet.setObjectName("pushButton_Telnet")
        self.horizontalLayout_2.addWidget(self.pushButton_Telnet)
        self.comboBox_Device = QtWidgets.QComboBox(Dialog)
        self.comboBox_Device.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_Device.setObjectName("comboBox_Device")
        self.horizontalLayout_2.addWidget(self.comboBox_Device)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_IP = QtWidgets.QComboBox(Dialog)
        self.comboBox_IP.setObjectName("comboBox_IP")
        self.horizontalLayout.addWidget(self.comboBox_IP)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_ShowDir = QtWidgets.QPushButton(Dialog)
        self.pushButton_ShowDir.setObjectName("pushButton_ShowDir")
        self.horizontalLayout.addWidget(self.pushButton_ShowDir)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "路径"))
        self.pushButton_Browse.setText(_translate("Dialog", "浏览"))
        self.pushButton.setText(_translate("Dialog", "应急"))
        self.pushButton_Telnet.setText(_translate("Dialog", "Telnet"))
        self.label_2.setText(_translate("Dialog", "IP 地址"))
        self.pushButton_ShowDir.setText(_translate("Dialog", "显示文件列表"))
