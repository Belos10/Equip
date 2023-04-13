import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sysManage.component import getMessageBox
from database.OrderManageSql import *

class OrderScheduleFinish(QDialog):
    signal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(OrderScheduleFinish, self).__init__(parent)
        self.setWindowTitle('完成接装')
        self.resize(300,200)   # 设置窗体大小
        self.fileName = ""
        self.file = ""
        self.fileWay = ""
        self.UnitDict = {}
        self.equipID = ''
        self.year = -1
        self.unitFlag = -1

        self.initSche()
        self.signalConnect()


    def initSche(self):
        # btn 2
        self.btn_chooseFile = QPushButton(self)
        self.btn_chooseFile.setObjectName("btn_chooseFile")
        self.btn_chooseFile.setText("选取文件")

        self.btn_openFile = QPushButton(self)
        self.btn_openFile.setObjectName("btn_openFile")
        self.btn_openFile.setText("下载文件")
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_chooseFile)
        layout.addWidget(self.btn_openFile)
        self.setLayout(layout)


    def signalConnect(self):
        # 设置信号
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.btn_openFile.clicked.connect(self.onOpen)


    def init1(self):
        self.fileName = ""
        self.file = ""
        self.fileWay = ""
        # self.ifUnitScheduleFinish()

    def initDict(self, unitDict, equipID, year, unitFlag):
        self.UnitDict = unitDict
        self.equipID = equipID
        self.year = year
        self.unitFlag = unitFlag


    def slot_btn_chooseFile(self):
        fileName_choose, filetype = \
            QFileDialog.getOpenFileName(self, "选取文件", "C:/",  # 起始路径
                                        "All Files (*);;PDF Files (*.pdf);;Pictures (*.jpg;*.jpeg;*.bmp)")  # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            return
        file = fileName_choose.split("/")
        self.fileWay = fileName_choose
        self.fileName = file[len(file) - 1]
        self.file = self.convertToBinaryData(fileName_choose)
        print("\n你选择的文件为:")
        print(self.fileName)
        print("文件筛选器类型: ", filetype)
        if self.unitFlag == 1:
            updateScheduleFinishUper(self.equipID, self.year, self.fileWay, self.file)
        elif self.unitFlag == 2:
            updateScheduleFinishBase(self.equipID, self.year, self.fileWay, self.file)


    def onOpen(self):
        if self.unitFlag == 1:
            result = selectFileUper(self.equipID, self.year)
        elif self.unitFlag == 2:
            result = selectFileBase(self.equipID, self.year)
        else:
            return
        file = result[0][0]
        fileType = result[0][1]
        if file == "" or file == '0':
            getMessageBox("提示", "未存放文件", True, False)
            return
        x = fileType.split("/")
        name = x[len(x) - 1]
        str_path = QFileDialog.getExistingDirectory(None, "选取文件夹", "")
        str_path += name
        self.writeTofile(file, str_path)


    def returnFileName(self):
        return self.fileName, self.file, self.fileWay


    def closeEvent(self, event):
        self.signal.emit('1')


    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData


    def writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = OrderScheduleFinish()
    mainForm.show()
    sys.exit(app.exec_())