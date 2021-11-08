import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from widgets.alocatMange.scheduleFinish import widget_ScheduleFinish
from database.alocatMangeSql import selectIfUnitScheduleFinish, updateUnitScheduleFinish


class ScheduleFinish(QWidget, widget_ScheduleFinish):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ScheduleFinish, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowTitle('完成接装')
        # self.cwd = os.getcwd() # 获取当前程序文件位置
        # self.resize(300,200)   # 设置窗体大小
        self.fileName = ""
        self.UnitDict = {}
        self.equipID = ''
        self.year = -1

        # self.btn_chooseFile = QPushButton(self)
        # self.btn_chooseFile.setObjectName("btn_chooseFile")
        # self.btn_chooseFile.setText("选取文件")
        #
        # self.btn_openFile = QPushButton(self)
        # self.btn_openFile.setObjectName("btn_openFile")
        # self.btn_openFile.setText("查看文件")
        self.layout1 = QHBoxLayout()
        self.signalConnect()
        # self.initUnitFinish()


    def signalConnect(self):

        self.pb_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        self.pb_openFile.clicked.connect(self.onOpen)


    def initDict(self, unitDict, equipID, year):
        self.UnitDict = unitDict
        self.equipID = equipID
        self.year = year


    def init1(self):
        self.initUnitFinish()
        self.ifUnitScheduleFinish()


    def initUnitFinish(self):
        aaa= self.layout1.count()
        print("aaa====",aaa)
        # while self.layout1.takeAt(0):
        #     print("count()==",self.layout1.count())
        #     self.layout1.removeWidget(QPushButton)
        #     pwid = self.layout1.takeAt(0).widget()
        #     pwid.__delattr__()
        #     pwid.deleteLater()

        # btns = self.layout1.findChildren(QPushButton)
        # for i in btns:
        #     i.delete()
        for i in range(self.layout1.count()):
            self.layout1.removeWidget(self.layout1.itemAt(i).widget())
        #     self.layout1.itemAt(i).widget().setParent(None)
        bbb = self.layout1.count()
        print("bbb=",bbb)
        print("self.UnitDict = ", self.UnitDict, "self.equipID = ", self.equipID)
        for key, item in self.UnitDict.items():
            flag = selectIfUnitScheduleFinish(self.UnitDict[key][0], self.equipID, self.year)
            pb1 = QPushButton()
            if flag[0][0] == 'TRUE':
                pb1.setObjectName(item[1])
                pb1.setText("已完成")
            else:
                pb1.setObjectName(item[1])
                pb1.setText(item[1])
            self.layout1.addWidget(pb1)
        self.w2_hbox.setLayout(self.layout1)
        ccc = self.layout1.count()
        print("ccc=",ccc)


    def ifUnitScheduleFinish(self):
        aaa= self.layout1.count()
        print("self.layout1.count()=", aaa)
        for i in range(self.layout1.count()):
            self.key = i
            print("i=====",i)
            # flag = 'TRUE'
            flag = selectIfUnitScheduleFinish(self.UnitDict[i][0], self.equipID, self.year)
            print("flag = ",flag)
            if not flag[0][0] == 'TRUE':
                self.layout1.itemAt(i).widget().clicked.connect(self.setUnitScheduleFinish)


    def setUnitScheduleFinish(self):
        reply = QMessageBox.question(self, "设置完成接装", "该单位是否完成接装？", QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            updateUnitScheduleFinish(self.UnitDict[self.key][0], self.equipID, self.year)
            self.layout1.itemAt(self.key).widget().setText("已完成")
            self.initUnitFinish()


    def slot_btn_chooseFile(self):
        fileName_choose, filetype = \
            QFileDialog.getOpenFileName(self,"选取文件","C:/",  # 起始路径
                                        "All Files (*);;PDF Files (*.pdf);;Pictures (*.jpg;*.jpeg;*.bmp)")  # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            # print("\n取消选择")
            return
        self.fileName = fileName_choose
        print("\n你选择的文件为:")
        print(fileName_choose)
        print("文件筛选器类型: ", filetype)

    def onOpen(self):
        print(self.fileName)
        if self.fileName == "":
            QMessageBox.information(self, "提示", "未存放文件")
            return
        os.startfile(self.fileName)

    def returnFileName(self):
        return self.fileName


    def closeEvent(self,event):
        self.signal.emit('1')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainForm = ScheduleFinish()
    dic = {0: ('3', '库存', '1', '', '否'), 1: ('4', '六十一基地', '2', '61', '否'),
           2: ('5', '六十二基地', '2', '62', '否'), 3: ('9', '六十三基地', '2', '63', '否'),
           4: ('10', '六十四基地', '2', '64', '否')}
    mainForm.initDict(dic, '5')
    mainForm.initUnitFinish()
    mainForm.show()
    sys.exit(app.exec_())
