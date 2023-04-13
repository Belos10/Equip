import io
import sys
import os
import shutil
import json
import PyPDF2
from io import BytesIO
from PIL import Image
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
from widgets.alocatMange.scheduleFinish import widget_ScheduleFinish
from database.alocatMangeSql import *
from PyQt5 import sip
from sysManage.component import getMessageBox

# 完成接装按钮 弹出界面
class ScheduleFinish(QWidget, widget_ScheduleFinish):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ScheduleFinish, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowTitle('完成接装')
        # self.cwd = os.getcwd() # 获取当前程序文件位置
        # self.resize(300,200)   # 设置窗体大小
        # self.signal = QtCore.pyqtSignal(str)
        self.fileName = ""
        self.file = ""
        self.fileWay = ""
        self.UnitDict = {}
        self.equipID = ''
        self.year = -1
        self.unitFlag = -1
        self.layout1 = QHBoxLayout()
        self.signalConnect()
        # self.initUnitFinish()


    def signalConnect(self):
        self.pb_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.pb_openFile.clicked.connect(self.onOpen)


    def initDict(self, unitDict, equipID, year, unitFlag):
        self.UnitDict = unitDict
        self.equipID = equipID
        self.year = year
        self.unitFlag = unitFlag


    def init1(self):
        self.initUnitFinish()
        self.fileName = ""
        self.file = ""
        self.fileWay = ""
        # self.ifUnitScheduleFinish()

    def deleteItemsOfLayout(self,layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())


    def initUnitFinish(self):
        try:
            # self.deleteItemsOfLayout(self.layout1)
            # self.layout1 = QHBoxLayout()
            # while self.layout1.takeAt(0):
            #     print("count()==",self.layout1.count())
            #     self.layout1.removeWidget(QPushButton)
            #     pwid = self.layout1.takeAt(0).widget()
            #     pwid.__delattr__()
            #     pwid.deleteLater()

            # btns = self.layout1.findChildren(QPushButton)
            # for i in btns:
            #     i.delete()
            # btns = self.layout1.findChildren(QPushButton)
            # for btn in btns:
            #     # self.layout1.removeItem(btn)
            #     self.layout1.removeWidget(btn)
            #     # btn.deleteLater()
            #     sip.delete(btn)
            for idx in range(self.layout1.count()+1, 1, -1):
                wid = self.layout1.itemAt(idx-2).widget()
                self.layout1.removeWidget(wid)
                sip.delete(wid)
            # for i in range(self.layout1.count()):
            #     item = self.layout1.itemAt(i)
            #     self.layout1.removeItem(item)
            #     # self.layout1.removeWidget(item)
            #     # item.widget().deleteLater()
            #     sip.delete(item)
            #     self.layout1.itemAt(i).widget().setParent(None)
            # print("Schedule::: self.UnitDict = ", self.UnitDict, "self.equipID = ", self.equipID)
            for key,item in self.UnitDict.items():
                flag = selectIfUnitScheduleFinish(self.UnitDict[key][0], self.equipID, self.year)
                cb = QCheckBox()
                cb.setText(item[1])

                cb.setStyleSheet(
                        '''
                        QCheckBox{ color:black;
    background-color:white;} 
                        '''
                )
                if flag[0][0] == 'TRUE':
                    cb.setChecked(True)
                else:
                    cb.setChecked(False)
                self.layout1.addWidget(cb)

            self.w2_hbox.setLayout(self.layout1)
            # self.w2_hbox.setStyleSheet("color:black；background-color:white")


            # print("self.UnitDict = ", self.UnitDict, "self.equipID = ", self.equipID)
            # for key, item in self.UnitDict.items():
            #     flag = selectIfUnitScheduleFinish(self.UnitDict[key][0], self.equipID, self.year)
            #     pb1 = QPushButton()
            #     if flag[0][0] == 'TRUE':
            #         pb1.setObjectName(item[1])
            #         pb1.setText("已完成")
            #     else:
            #         pb1.setObjectName(item[1])
            #         pb1.setText(item[1])
            #     self.layout1.addWidget(pb1)
            # self.w2_hbox.setLayout(self.layout1)
        except Exception as e:
            print(e)

    def ifUnitScheduleFinish(self):
        aaa = self.layout1.count()
        for i in range(self.layout1.count()):
            self.key = i
            flag = selectIfUnitScheduleFinish(self.UnitDict[i][0], self.equipID, self.year)
            if not flag[0][0] == 'TRUE':
                self.layout1.itemAt(i).widget().clicked.connect(self.setUnitScheduleFinish)


    def setUnitScheduleFinish(self):
        reply = getMessageBox("设置完成接装", "该单位是否完成接装？", True, True)
        if reply == QMessageBox.Ok:
            updateUnitScheduleFinish(self.UnitDict[self.key][0], self.equipID, self.year, True)
            self.layout1.itemAt(self.key).widget().setText("已完成")
            self.initUnitFinish()


    # 选择文件
    def slot_btn_chooseFile(self):
        fileName_choose, filetype = \
            QFileDialog.getOpenFileName(self, "选取文件", "C:/",  # 起始路径
                                        "All Files (*);;PDF Files (*.pdf);;Pictures (*.jpg;*.jpeg;*.bmp)")  # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            return
        file = fileName_choose.split("/")
        self.fileWay = fileName_choose
        self.fileName = file[len(file)-1]
        self.file = self.convertToBinaryData(fileName_choose)
        print("\n你选择的文件为:")
        print(self.fileName)
        print("文件筛选器类型: ", filetype)
        if self.unitFlag == 1:
            updateScheduleFinishUper(self.equipID, self.year, self.fileWay, self.file)
        elif self.unitFlag == 2:
            updateScheduleFinishBase(self.equipID, self.year, self.fileWay, self.file)

    # 查看文件
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
        name = x[len(x)-1]
        str_path = QFileDialog.getExistingDirectory(None, "选取文件夹", "")
        str_path += name
        # if type == "pdf":
        #     res = PyPDF2.PdfReader(BytesIO(file))
        # else:
        #     res = Image.open(BytesIO(file))
        #     res.show()
        self.writeTofile(file, str_path)



    def returnFileName(self):
        return self.fileName, self.file, self.fileWay



    def closeEvent(self, event):
        for idx in range(self.layout1.count()):
            flag = False
            if self.layout1.itemAt(idx).widget().isChecked():
                flag = True
            updateUnitScheduleFinish(self.UnitDict[idx][0], self.equipID, self.year, flag)
            # self.initUnitFinish()
        self.signal.emit('1')
        return


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = ScheduleFinish()
    dic = {0: ('3', '库存', '1', '', '否'), 1: ('4', '六十一基地', '2', '61', '否'),
           2: ('5', '六十二基地', '2', '62', '否'), 3: ('9', '六十三基地', '2', '63', '否'),
           4: ('10', '六十四基地', '2', '64', '否')}
    mainForm.initDict(dic, '5',2000)
    mainForm.initUnitFinish()
    mainForm.show()
    sys.exit(app.exec_())
