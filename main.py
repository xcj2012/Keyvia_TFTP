#!/usr/bin/python
# coding:utf-8

"""
@author:xiangj
@contact:34112429@qq.com
@software:PyCharm
@file: main.py.py
@time:2021/7/7 10:29
"""

import os
import sys
import time, struct
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog, QMessageBox, QInputDialog, QLineEdit, QMainWindow
from PyQt5.QtCore import QThread, QSize, QTimer, QTime, QCoreApplication, QEventLoop, QByteArray, QPoint
from PyQt5.QtGui import QImage, QPainter, QRgba64, QPixmap, qRgb, QPolygon
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush, QPalette
from telnetlib import Telnet
from MainDialog import Ui_Dialog as TFTPDialog
import PyQt5.QtCore as QtCore
import socket
import serial
from socket import *
from FilesInfo import Ui_Dialog as InfoDialog
from Energy import Ui_Dialog as EnergyDlg
from Telenet import Ui_Dialog as TelnetDlg
import serial.tools.list_ports
import zipfile
# import telnetlib

from shutil import copyfile

RRQ = 1
WRQ = 2
DATA = 3
ACK = 4
ERROR = 5


class TSysTime():
    def __init__(self):
        self.Year = 0
        self.month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.Week = 0
        self.MSecond = 0

    def __init__(self, pdata: bytes):
        self.Year = 0
        self.month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.Week = 0
        self.MSecond = 0
        if pdata:
            self.Year = int.from_bytes(pdata[0:2], byteorder='little', signed=False)
            self.month = int.from_bytes(pdata[2:3], byteorder='little', signed=False)
            self.Day = int.from_bytes(pdata[3:4], byteorder='little', signed=False)
            self.Hour = int.from_bytes(pdata[4:5], byteorder='little', signed=False)
            self.Minute = int.from_bytes(pdata[5:6], byteorder='little', signed=False)
            self.Second = int.from_bytes(pdata[6:7], byteorder='little', signed=False)
            self.Week = int.from_bytes(pdata[7:8], byteorder='little', signed=False)
            self.MSecond = int.from_bytes(pdata[8:10], byteorder='little', signed=False)


class TFileHead():
    def __init__(self, pdata: bytes):
        self.dwSize = None
        self.wVersion = None
        self.dwMagic = None
        self.cVer = None
        self.bFlagNew1 = None
        self.bFlagNew2 = None
        self.wrsv = None
        self.wCheck = None
        if pdata:
            self.dwSize = int.from_bytes(pdata[0:4], byteorder='little', signed=False)  # DWORD       	dwSize;			//?????????
            self.dwMagic = int.from_bytes(pdata[8:8 + 4], byteorder='little',
                                          signed=False)  # DWORD       	dwMagic;		//????????????,?????????????????????????????????
            self.cVer = pdata[12:12 + 10]  # char            cVer[REV_SIZE_10];
            self.bFlagNew1 = pdata[22:23]  # BYTE			bFlagNew1;
            if self.bFlagNew1 == '0x40':
                self.wVersion = int.from_bytes(pdata[4:4 + 4], byteorder='little',
                                               signed=False)  # DWORD           wVersion;		//?????????
            else:
                self.wVersion = int.from_bytes(pdata[4:4 + 4], byteorder='big',
                                               signed=False)  # DWORD           wVersion;		//?????????

            self.bFlagNew2 = pdata[23:24]  # BYTE			bFlagNew2;
            self.wrsv = int.from_bytes(pdata[24:24 + 2], byteorder='little', signed=False)  # WORD			wrsv;
            self.wCheck = pdata[26:26 + 2]  # WORD			wCheck;			//?????????


class TFileHeadOS():
    def __init__(self, pdata: bytes):
        self.dwSize = bytes(4)
        self.Version = bytes(16)
        self.dwMagic = bytes(4)
        self.sysTime = TSysTime(bytes(10))
        self.wRev = bytes(2)
        self.dwCheck = bytes(4)
        if pdata:
            self.dwSize = int.from_bytes(pdata[0:4], byteorder='little', signed=False)  # DWORD       	dwSize;			//?????????
            self.Version = pdata[4:4 + 16]  # char            cVer[REV_SIZE_10];
            self.dwMagic = int.from_bytes(pdata[20:20 + 4], byteorder='little',
                                          signed=False)  # DWORD       	dwMagic;		//????????????,?????????????????????????????????
            self.sysTime = TSysTime(pdata[24:24 + 10])
            # self.wRev = int.from_bytes(pdata[34:34+2], byteorder='little', signed=False) #WORD			wrsv;
            self.dwCheck = int.from_bytes(pdata[36:36 + 4], byteorder='little', signed=False)  # WORD			wCheck;			//?????????


class TFTPReadWriteRequest():
    # @staticmethod
    def encode(op, file_name, mode='octet'):
        opcode_select = {'r': RRQ, 'w': WRQ}
        opcode = opcode_select[op]
        packet = struct.pack('!H%dsb%dsb' % (len(file_name), len(mode)), opcode, file_name.encode(), 0, mode.encode(),
                             0)
        return packet

    # @staticmethod
    def decode(msg_bytes):
        size = 512
        opcode = struct.unpack('!H', msg_bytes[:2])[0]
        fileName = msg_bytes[2:].decode('utf-8').split('\x00')[0]
        mode = msg_bytes[2:].decode('utf-8').split('\x00')[1]
        timeout = msg_bytes[2:].decode('utf-8').split('\x00')[2]
        time = msg_bytes[2:].decode('utf-8').split('\x00')[3]
        blksize = msg_bytes[2:].decode('utf-8').split('\x00')[4]
        if (len(blksize)):
            size = msg_bytes[2:].decode('utf-8').split('\x00')[5]
        print('=== Transfer mode is %s' % mode)
        return opcode, fileName, size


class TFTPServer(QThread):
    # ?????????
    DOWNLOAD = 1
    UPLOAD = 2
    DATA = 3
    ACK = 4
    ERROR = 5
    self_msg = QtCore.pyqtSignal(str)  # ????????????????????????str???????????????
    trans_maxvalue = QtCore.pyqtSignal(int)  # ????????????????????????str???????????????
    trans_curvalue = QtCore.pyqtSignal(int)  # ????????????????????????str???????????????

    def __init__(self):
        super(TFTPServer, self).__init__()
        self.recvData = None
        self.recvAddr = None
        self.serverSocket = socket(AF_INET, SOCK_DGRAM)
        # self.serverSocket.bind(("", 69))
        self.blksize = 512
        self.path = ""
        self.ip = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def setIP(self, ip):
        self.ip = ip
        self.serverSocket.bind((self.ip, 69))
        self.RunFlag = False

    def timeout(self):
        print("Timeout")
        self.setState(False)
        self.setState(True)

    def setPath(self, path):
        self.path = path

    def setState(self, value):
        self.RunFlag = value
        if not self.RunFlag:
            self.serverSocket.close()
            self.serverSocket = None
        else:
            self.serverSocket = socket(AF_INET, SOCK_DGRAM)
            self.serverSocket.bind((self.ip, 69))

    def run(self):
        while self.RunFlag:
            # print("#" * 30)
            print("????????????????????????")
            self.self_msg.emit("????????????????????????")
            ret = self.listen()
            if not ret:
                return
            if self.cmdType == self.DOWNLOAD:
                self.download()
            elif self.cmdType == self.UPLOAD:
                self.upload()

    def listen(self):
        # ??????client??????
        try:

            self.recvData, self.recvAddr = self.serverSocket.recvfrom(1024)
            print("??????????????????%s" % self.recvAddr[0] + str(self.recvAddr[1]))
            self.self_msg.emit("??????????????????%s" % self.recvAddr[0] + " ??????:%d" % self.recvAddr[1])
            self.cmdType = struct.unpack("!H", self.recvData[:2])[0]
            return True
        except Exception as e:
            # self.serial.close()
            print("?????????????????????????????????%s" % e)
            self.self_msg.emit("?????????????????????????????????%s" % e)
            return False

    # ?????????????????????
    def download(self):
        # ??????????????????
        udpSocket = socket(AF_INET, SOCK_DGRAM)

        fileReq = None
        try:
            # ????????????????????????????????????
            # print("receive:", self.recvData.decode())
            opcode, file_name, blksize = TFTPReadWriteRequest.decode(self.recvData)
            self.blksize = int(blksize)
            info = struct.unpack('!b5sb', self.recvData[-7:])
            # if info == (101, b'octet', 0):
            self.fileReqName = file_name  # ?????????
            # fileReqName = self.recvData[2:-7].decode()
            print(self.fileReqName)
            print("??????????????????????????????%s" % self.fileReqName)
            self.self_msg.emit("??????????????????????????????%s" % self.fileReqName)
            # ????????????
            try:
                fileReq = open(os.path.join(self.path, self.fileReqName), "rb")
            except:
                print("?????? ???%s??? ?????????" % os.path.join(self.path, self.fileReqName))
                self.self_msg.emit("?????? ???%s??? ?????????" % os.path.join(self.path, self.fileReqName))
                # ??? client ??????????????????
                errInfo = struct.pack("!HHHb", 5, 5, 5, 0)
                udpSocket.sendto(errInfo, self.recvAddr)
                return False

            # ??????????????????
            frameNum = 1
            while True:
                fileData = fileReq.read(512)
                self.trans_maxvalue.emit(os.path.getsize(os.path.join(self.path, self.fileReqName)) // 512 + 1)
                # ??????
                # frameData = struct.pack(str("!HH%ds" % len(fileData)), 3, frameNum, fileData)
                frameData = struct.pack(str("!HH"), 3, frameNum) + fileData
                # ??????
                for i in range(0, 2):
                    udpSocket.sendto(frameData, self.recvAddr)
                    # ????????????????????????
                    if len(fileData) < 512:
                        print("?????????????????????")
                        self.self_msg.emit("?????????????????????????????????%d" % os.path.getsize(os.path.join(self.path, self.fileReqName)))
                        fileReq.close()
                        fileReq = None
                        return True

                    # ??????client??????
                    self.timer.start(200)
                    # ????????????
                    self.recvData, self.recvAddr = udpSocket.recvfrom(1024)
                    cmdType, recvFrameNum = struct.unpack("!HH", self.recvData[:4])
                    self.timer.stop()
                    if cmdType == self.ACK and recvFrameNum == frameNum:
                        self.trans_curvalue.emit(recvFrameNum + 1)

                        # print("?????????????????????")
                        break
                    elif i == 2:
                        print("???????????????????????????")
                        self.self_msg.emit("???????????????????????????")
                        # ??? client ??????????????????
                        errInfo = struct.pack("!HHHb", 5, 5, 5, 0)
                        udpSocket.sendto(errInfo, self.recvAddr)
                        exit()

                # ??????+1
                frameNum += 1
        finally:
            if fileReq != None:
                fileReq.close()

    # ?????????????????????
    def upload(self):
        # ??????????????????
        udpSocket = socket(AF_INET, SOCK_DGRAM)

        # ?????????????????????????????????
        ack = struct.pack("!HH", self.ACK, 0)
        udpSocket.sendto(ack, self.recvAddr)

        # ??????????????????????????????
        recvFrameNum = 1
        # ?????? client ??????
        while True:
            # ????????????
            recvData, recvAddr = udpSocket.recvfrom(1024)
            # ???????????? ?????????2 ?????????2 ??????n
            cmdType, frameNum = struct.unpack("!HH", recvData[:4])
            # ????????????????????????????????????
            if cmdType == self.DATA and frameNum == recvFrameNum:
                print("????????????%d????????????" % frameNum)  # for test
                # ????????????
                if frameNum == 1:
                    fileRecv = open("upload.txt", "ab")
                    fileRecv.write(b"#" * 30 + time.strftime("%Y-%m-%d %H:%M:%S").encode() + b"#" * 30 + b"\n")

                fileRecv.write(recvData[4:])

                # ?????? : ?????????2 ?????????2
                ack = struct.pack("!HH", self.ACK, frameNum)
                udpSocket.sendto(ack, recvAddr)

                # ?????????????????????
                if len(recvData) < 516:
                    fileRecv.close()
                    fileRecv = None
                    print("??????????????? ???????????????")
                    break

                # ??????+1
                recvFrameNum += 1

            elif cmdType == self.ERROR:
                print("?????????????????????????????????")
                break


class SerialClient(QThread):
    self_msg = QtCore.pyqtSignal(str)  # ????????????????????????str???????????????

    def __init__(self):
        super(SerialClient, self).__init__()

    def closeport(self):
        self.run = False
        # self.sleep(100)
        self.serial.close()
        self.serial = None

    def init_serial(self, name, rate, size, par, stop):
        try:
            self.serial = serial.Serial(name, rate)
            self.run = True
        except Exception as e:
            # self.serial.close()
            print("????????????????????????????????????%s" % e)
            self.self_msg.emit("????????????????????????????????????%s\n" % e)
            return False
        if self.serial.isOpen():
            print("?????????????????????%s" % name)
            self.self_msg.emit("?????????????????????%s\n" % name)
            return True
        else:
            print("?????????????????????%s" % name)
            self.self_msg.emit("?????????????????????%s\n" % name)
            return False

    def run(self):
        while self.run:
            try:
                count = self.serial.inWaiting()
                if count > 0:
                    data = self.serial.read(count)
                    print("receive:", data)
                    msg = data.decode('utf-8')
                    if "password" in msg or "ond" in msg or "seconds" in msg or "Press" in msg:
                        self.serial.write(b'kf')
                    if "=>" in msg:
                        self.serial.write(b'bootvx tftp\n')

                    self.self_msg.emit(msg)

            except KeyboardInterrupt:
                if self.serial != None:
                    self.serial.close()
        self.serial.close()


class TelnetClient(QThread):
    self_msg = QtCore.pyqtSignal(str)  # ????????????????????????str???????????????

    def __init__(self, ip, port):
        super(SerialClient, self).__init__()
        self.tn = Telnet(ip, port)

    def closeport(self):
        self.run = False
        self.tn.close()
        # self.sleep(100)
        # self.serial.close()

    def init_serial(self, ip, port):
        try:
            self.tn = Telnet(ip, port)
            self.run = True
        except Exception as e:
            # self.serial.close()
            print("Telnet ??????????????????????????????%s" % e)
            self.self_msg.emit("Telnet ??????????????????????????????%s\n" % e)
            return False
        if self.serial.isOpen():
            print("Telnet ???????????????%s" % ip + "??????%d" % port)
            self.self_msg.emit("Telnet ???????????????%s" % ip + "??????%d" % port)
            return True
        else:
            print("Telnet ???????????????%s" % ip + "??????%d" % port)
            self.self_msg.emit("Telnet ???????????????%s" % ip + "??????%d" % port)
            return False

    def run(self):
        while self.run:
            try:
                count = self.serial.inWaiting()
                if count > 0:
                    data = self.serial.read(count)
                    print("receive:", data)
                    msg = data.decode('utf-8')
                    if "password" in msg or "ond" in msg or "seconds" in msg or "Press" in msg:
                        self.serial.write(b'kf')
                    if "=>" in msg:
                        self.serial.write(b'bootvx tftp\n')

                    self.self_msg.emit(msg)

            except KeyboardInterrupt:
                if self.serial != None:
                    self.serial.close()
        self.serial.close()


class EnergyForm(EnergyDlg, QDialog):
    def __init__(self):
        super(EnergyForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("????????????")
        self.init_device()
        self.init_connect()

    def init_connect(self):
        self.pushButton_start.clicked.connect(self.pushbutton_start_click)
        self.pushButton_stop.clicked.connect(self.pushbutton_stop_click)
        self.pushButton_clear.clicked.connect(self.pushbutton_clear_click)
        self.pushButton_save.clicked.connect(self.pushbutton_save_click)
        self.pushButton_file.clicked.connect(self.pushbutton_file_click)
        return

    def init_device(self):

        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
            print('???????????????')
            self.pushButton_start.setEnabled(False)
            self.comboBox_var.setEnabled(False)
            self.comboBox_rate.setEnabled(False)
            self.comboBox_stop.setEnabled(False)
            self.comboBox_data.setEnabled(False)
            self.textBrowser.append("???????????????")
        else:
            for label in port_list:
                self.comboBox_port.addItem(label.device, label.device)
        rates = ["9600", "14400", "19200", "38400", "56000", "57600", "115200"]
        for rate in rates:
            self.comboBox_rate.addItem(rate, (rate))
        self.comboBox_rate.setCurrentText("115200")
        datas = ["5", "6", "7", "8"]
        for date in datas:
            self.comboBox_data.addItem(date, (date))
        self.comboBox_data.setCurrentText("8")
        stops = ["1", "2"]
        for stop in stops:
            self.comboBox_stop.addItem(stop, (stop))
        self.comboBox_stop.setCurrentText("1")
        vars = ["?????????", "?????????", "?????????", "??????????????????1", "??????????????????0"]
        self.comboBox_var.addItems(vars)
        self.comboBox_var.setCurrentText("?????????")
        return

    def pushbutton_clear_click(self):
        self.textBrowser.clear()

    def pushbutton_save_click(self):
        text = self.textBrowser.toPlainText()
        filename, path = QFileDialog.getSaveFileName(self, "????????????", "/", "???????????? (*.txt)")  # ???????????????????????????,????????????????????????
        if not filename:
            return
        with open(filename, "w") as f:
            f.write(text)
        f.close()
        return

    def update_msg(self, text):
        self.textBrowser.insertPlainText(text)
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    def pushbutton_file_click(self):
        filename, path = QFileDialog.getOpenFileName(self, "????????????", "/",
                                                     "????????????????????? (vxworks main.bin main.os)")  # ???????????????????????????,????????????????????????
        if filename.endswith("main.os"):
            try:
                f = zipfile.ZipFile(filename)
                for file in f.namelist():
                    if "main.bin" in file:
                        f.extract(f, os.path.join(os.getcwd(), "bootvx"))
                        copyfile(os.path.join(os.getcwd(), "bootvx/main.bin"),
                                 os.path.join(os.getcwd(), "bootvx/vxworks"))
                        return
            except Exception as e:
                print("?????????????????????????????????%s" % e)
                with open(filename, "rb") as f:
                    datas = f.read()
                    fileheader = TFileHeadOS(datas)
                    index = 0
                    index += 40
                    count = int.from_bytes(datas[index:index + 2], byteorder='little', signed=False)
                    print("????????????%d" % count)
                    index += 2
                    pos = index + count * 36
                    size = 0
                    for i in range(count):
                        name = datas[index + i * 36:index + 32 + i * 36].decode("utf-8").rstrip(b'\x00'.decode())
                        n = len(name.rstrip(b'\x00'.decode()))
                        size = int.from_bytes(datas[index + i * 36 + 32:index + 36 + i * 36], byteorder='little',
                                              signed=False)
                        print("????????????%s" % name.rstrip(b'\x00'.decode()))
                        print("????????????%d" % size)
                        if "main.bin" in name.lower():
                            break
                        else:
                            pos += size
                file = open(os.path.join(os.getcwd(), "bootvx/vxworks"), "wb")
                file.write(datas[pos:pos + size])
                file.close()
            return
        if filename.endswith("main.bin") or filename.endswith("vxworks"):
            try:
                copyfile(filename, os.path.join(os.getcwd(), "bootvx/vxworks"))
            except IOError as e:
                print("Unable to copy file. %s" % e)
                return
            except:
                print("Unexpected error:", sys.exc_info())
                return

        # self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        return

    def pushbutton_start_click(self):
        self.comboBox_stop.setEnabled(False)
        self.comboBox_rate.setEnabled(False)
        self.comboBox_data.setEnabled(False)
        self.comboBox_var.setEnabled(False)
        self.comboBox_port.setEnabled(False)
        self.pushButton_start.setEnabled(False)
        self.serial = SerialClient()
        self.serial.self_msg.connect(self.update_msg)
        ret = self.serial.init_serial(self.comboBox_port.currentData(), int(self.comboBox_rate.currentText()),
                                      int(self.comboBox_data.currentText()),
                                      self.comboBox_var.currentIndex(), int(self.comboBox_stop.currentData()))
        if not ret:
            self.pushbutton_stop_click()
            return
        self.serial.start()

    def pushbutton_stop_click(self):
        self.comboBox_stop.setEnabled(True)
        self.comboBox_rate.setEnabled(True)
        self.comboBox_data.setEnabled(True)
        self.comboBox_var.setEnabled(True)
        self.comboBox_port.setEnabled(True)
        self.pushButton_start.setEnabled(True)
        self.serial.closeport()


class InfForm(InfoDialog, QDialog):

    def __init__(self):
        super(InfForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("??????????????????")
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        headers = ["?????????", "????????????", "????????????"]
        self.model.setHorizontalHeaderLabels(headers)

    def show_files(self, path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                rows = []
                item1 = QStandardItem(file)
                item1.setEnabled(False)
                rows.append(item1)
                item1 = QStandardItem(str(os.path.getsize(os.path.join(path, file))))
                item1.setEnabled(False)
                rows.append(item1)
                item1 = QStandardItem(str(time.ctime(os.path.getatime(os.path.join(path, file)))))
                item1.setEnabled(False)
                rows.append(item1)
                self.model.appendRow(rows)
        self.tableView.resizeColumnsToContents()


class MainForm(TFTPDialog, QDialog):
    # self_Finish = QtCore.pyqtSignal(str) #????????????????????????str???????????????
    self_Finish = QtCore.pyqtSignal(str)  # ????????????????????????str???????????????

    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("????????????????????????")
        self.server = TFTPServer()
        self.files = []
        self.init_files()
        self.init_Device()
        self.init_dialog()
        self.init_IP()
        self.combox_Device_change(0)

    def init_dialog(self):
        self.progressBar.setValue(0)
        self.pushButton.clicked.connect(self.pushbutton_Enery)
        self.pushButton_Browse.clicked.connect(self.pushbutton_Enery)
        self.pushButton_ShowDir.clicked.connect(self.pushbutton_showDir)
        self.comboBox_IP.currentIndexChanged.connect(self.combox_IP_change)
        self.comboBox_Device.currentIndexChanged.connect(self.combox_Device_change)
        self.server.self_msg.connect(self.update_msg)
        self.server.trans_maxvalue.connect(self.init_processbar)
        self.server.trans_curvalue.connect(self.update_bar)

    def init_IP(self):
        # addrs = socket.getaddrinfo(socket.gethostname(), None)
        addrs = getaddrinfo(gethostname(), None)
        print(addrs)
        # ?????????????????????IPV4??????
        for item in addrs:
            if ':' not in item[4][0]:
                self.comboBox_IP.addItem(item[4][0])
                print('????????????IPV4?????????:' + item[4][0])

    def init_files(self):
        with open("file.txt", "r") as f:
            self.files = f.readlines()

    def init_processbar(self, value):
        self.progressBar.setRange(0, value)

    def update_bar(self, value):
        self.progressBar.setValue(value)

    def update_msg(self, text):
        self.textBrowser.append(text)

    def init_Device(self):
        for path in self.files:
            if os.path.exists(path[:-1]):
                if "DCP3V2" in path[:-1]:
                    device_path = os.path.join(path[:-1], "App\\prj")
                else:
                    device_path = os.path.join(path[:-1], "App\\src\\relay")
                find = False
                for file in os.listdir(device_path):
                    file_path = os.path.join(device_path, file)
                    if os.path.isfile(file_path):
                        continue
                    if file_path.endswith("common"):
                        continue
                    default_path = ""
                    if os.path.exists(os.path.join(file_path, "compile\default")):
                        default_path = os.path.join(file_path, "compile\default")
                    elif os.path.exists(os.path.join(file_path, "prj\compile\default")):
                        default_path = os.path.join(file_path, "prj\compile\default")
                    elif os.path.exists(os.path.join(file_path, "prj-debug\compile\default")):
                        default_path = os.path.join(file_path, "prj-debug\compile\default")
                    if len(default_path) != 0:
                        self.comboBox_Device.addItem(file, default_path)
                        print(file_path)
                        find = True
                if not find:
                    self.textBrowser.append(path + "?????????????????????:vxworks")

    def pushbutton_Enery(self):
        self.Serialdlg = EnergyForm()
        self.Serialdlg.show()

    def pushbutton_showDir(self):
        dlg = InfForm()
        dlg.show_files(self.lineEdit.text())
        dlg.exec()
        return

    def combox_IP_change(self, index):

        return

    def combox_Device_change(self, index):
        self.update_bar(0)
        path = self.comboBox_Device.currentData()
        self.lineEdit.setText(path)
        self.textBrowser.append("????????????%s" % self.comboBox_Device.currentText() + " ??????:%s" % path)
        self.server.setPath(self.lineEdit.text())
        # self.server.setIP(self.comboBox_IP.currentText())
        self.server.setState(False)
        self.server.quit()
        self.server.setState(True)
        self.server.start()

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_pyqt_form = MainForm()
    my_pyqt_form.show()

    sys.exit(app.exec_())
