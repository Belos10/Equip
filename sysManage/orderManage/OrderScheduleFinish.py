import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class OrderScheduleFinish(QDialog):
    signal = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(OrderScheduleFinish, self).__init__(parent)
        self.setWindowTitle('完成接装')
        #self.cwd = os.getcwd() # 获取当前程序文件位置
        self.resize(300,200)   # 设置窗体大小
        # btn 1
        # self.btn_chooseDir = QPushButton(self)
        # self.btn_chooseDir.setObjectName("btn_chooseDir")
        # self.btn_chooseDir.setText("选择文件夹")
        self.fileName=""
        # btn 2
        self.btn_chooseFile = QPushButton(self)
        self.btn_chooseFile.setObjectName("btn_chooseFile")
        self.btn_chooseFile.setText("选取文件")



        # btn 3
        # self.btn_chooseMutiFile = QPushButton(self)
        # self.btn_chooseMutiFile.setObjectName("btn_chooseMutiFile")
        # self.btn_chooseMutiFile.setText("多文件选择")



        # btn 4
        # self.btn_saveFile = QPushButton(self)
        # self.btn_saveFile.setObjectName("btn_saveFile")
        # self.btn_saveFile.setText("文件保存")

        self.btn_openFile = QPushButton(self)
        self.btn_openFile.setObjectName("btn_openFile")
        self.btn_openFile.setText("查看文件")

        # 设置布局
        layout = QVBoxLayout()
        #layout.addWidget(self.btn_chooseDir)
        layout.addWidget(self.btn_chooseFile)
        # layout.addWidget(self.btn_chooseMutiFile)
        # layout.addWidget(self.btn_saveFile)
        layout.addWidget(self.btn_openFile)
        self.setLayout(layout)


        # 设置信号
        # self.btn_chooseDir.clicked.connect(self.slot_btn_chooseDir)
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)
        # self.btn_chooseMutiFile.clicked.connect(self.slot_btn_chooseMutiFile)
        # self.btn_saveFile.clicked.connect(self.slot_btn_saveFile)
        self.btn_openFile.clicked.connect(self.onOpen)




    def slot_btn_chooseFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "C:/", # 起始路径
                                    "All Files (*);;PDF Files (*.pdf);;Pictures (*.jpg;*.jpeg;*.bmp)")   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            # print("\n取消选择")
            return

        self.fileName=fileName_choose
        print("\n你选择的文件为:")
        print(fileName_choose)
        print("文件筛选器类型: ",filetype)

    # def slot_btn_chooseMutiFile(self):
    #     files, filetype = QFileDialog.getOpenFileNames(self,
    #                                 "多文件选择",
    #                                 "C:/", # 起始路径
    #                                 "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt)")
    #
    #     if len(files) == 0:
    #         #print("\n取消选择")
    #         return
    #
    #     #print("\n你选择的文件为:")
    #     #for file in files:
    #         #print(file)
    #     #print("文件筛选器类型: ",filetype)


    def onOpen(self):
        print(self.fileName)
        if self.fileName == "":
            QMessageBox.information(self, "提示", "未存放文件")
            return
        os.startfile(self.fileName)

    def returnFileName(self):
        return self.fileName

    def closeEvent(self, event):
        self.signal.emit('1')

if __name__=="__main__":
    app = QApplication(sys.argv)
    mainForm = OrderScheduleFisish()
    mainForm.show()
    sys.exit(app.exec_())