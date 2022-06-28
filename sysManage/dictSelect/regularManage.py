import os
import sys
import zipfile

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QHeaderView, QTableWidgetItem, \
    QAbstractItemView, QCheckBox
from sysManage.component import getMessageBox
from database.regularManageSql import getResultFromRegularManage, savaFile, deleteFile
from widgets.dictSelect.regularManage import Widget_Regular_Manage


class regularManage(QWidget, Widget_Regular_Manage):
    def __init__(self, parent=None):
        super(regularManage, self).__init__(parent)
        self.setupUi(self)
        self.basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.dirctorPath = self.basepath + '\\' + 'resource' + '\\'
        self.signalConnect()
        self.init()

    def signalConnect(self):
        self.pb_input.clicked.connect(self.soltInputFile)
        self.pb_output.clicked.connect(self.soltOutputFiles)
        self.pb_search.clicked.connect(self.soltSearchFile)
        self.pb_delete.clicked.connect(self.soltDeleteFile)
        self.lw_file.itemActivated.connect(self.soltOpenFile)
        pass
        # self.pb_input.clicked.connect(self.onOpenFile)
    def init(self):

        self.lw_file.clear()
        self.result = []
        self.displayData()
    def displayData(self):
        fileName = self.le_fileName.text()
        self.result = getResultFromRegularManage(fileName)
        self.lw_file.setColumnCount(5)
        self.lw_file.setRowCount(len(self.result))
        header = ['序号','名称','文件类型','导入日期','选择']
        self.lw_file.verticalHeader().setVisible(False)
        # self.lw_file.horizontalHeader().setVisible(False)
        self.lw_file.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lw_file.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.lw_file.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.lw_file.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.lw_file.resizeColumnsToContents()
        # self.lw_file.resizeRowsToContents()
        self.lw_file.setHorizontalHeaderLabels(header)
        for i,info in enumerate(self.result):
            item = QTableWidgetItem(str(info[0] + 1))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.lw_file.setItem(i,0,item)

            item = QTableWidgetItem(info[1])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.lw_file.setItem(i, 1, item)

            item = QTableWidgetItem(info[2])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.lw_file.setItem(i, 2, item)

            item = QTableWidgetItem(info[4])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.lw_file.setItem(i, 3, item)

            checkBox = QCheckBox('选择')
            checkBox.setCheckState(Qt.Unchecked)
            self.lw_file.setCellWidget(i, 4, checkBox)




        if len(self.result) == 0:
            self.pb_output.setDisabled(True)
            self.pb_delete.setDisabled(True)
        else:
            self.pb_output.setDisabled(False)
            self.pb_delete.setDisabled(False)

    def soltInputFile(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, '请选择文件', '', 'word(*.docx *.doc);;pdf(*.pdf)')
        if not paths:
            return
        if _.find('*.doc') or _.find('*.pdf'):
            if len(paths) > 0:
                for path in paths:
                    strings = path.split('/')
                    lastString = strings[-1]
                    names = lastString.split('.')
                    type = names[-1]
                    name = '.'.join(names[0:-1])
                    dirctorFilePath = self.dirctorPath + name + '.' + type
                    date = QDateTime.currentDateTime()
                    stringDate = date.toString("yyyy-MM-dd")

                    with open(path, "rb") as root_file:
                        with open(dirctorFilePath, "wb") as copy_file:
                            while True:
                                data = root_file.read(1024)
                                if data:
                                    copy_file.write(data)
                                else:
                                    # count += 1
                                    # self.progerss.setValue(count)
                                    break
                    if savaFile(name,type,dirctorFilePath,stringDate) == False:
                        getMessageBox("警告", "导入失败！", True, False)
                        self.init()
                        return
                getMessageBox("提醒", "导入成功！", True, False)
                self.init()

        else:
            getMessageBox("警告", "该文件导入不支持！", True, False)

    def soltOpenFile(self,item):
        row = self.lw_file.row(item)
        if row != -1:
            fileInfo = self.result[row];
            import win32api
            try:
                win32api.ShellExecute(0, 'open', fileInfo[3], '', '', 1)
            except:
                getMessageBox("警告", "找不到指定文件", True, False)



    def soltOutputFiles(self):
        reply = getMessageBox('导出选中', '确定导出选中文件？', True, True)
        if reply == QMessageBox.Ok:
            directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
            if len(directoryPath) > 0:
                date = QDateTime.currentDateTime()
                zipDate = date.toString("yyyy年MM月dd日hh时mm分ss秒")# hh:mm:ss
                zipName = "/" + zipDate + " 导出法规.zip"
                directoryPathName = (directoryPath + zipName)
                createdZipFile = zipfile.ZipFile(directoryPath + zipName,"w",zipfile.ZIP_DEFLATED)
                for i in range(self.lw_file.rowCount()):
                    item = self.lw_file.cellWidget(i, 4)
                    if item != None and item.checkState() == 2:
                        fileInfo = self.result[i]
                        createdZipFile.write(fileInfo[3],fileInfo[1] + '.' + fileInfo[2],zipfile.ZIP_DEFLATED)
                createdZipFile.close()
                getMessageBox('成功', '成功导出！', True, False)
            pass

    def soltSearchFile(self):
        self.init()


    def soltDeleteFile(self):
        reply = getMessageBox('删除', '确定删除选中导入的文件？', True, True)
        if reply == QMessageBox.Ok:
            for i in range(self.lw_file.rowCount()):
                item = self.lw_file.cellWidget(i, 4)
                if item != None and item.checkState() == 2:
                    fileInfo = self.result[i]
                    try:
                        os.remove(fileInfo[3])
                    except Exception as e:
                        print(e)
                        try:
                            if os.path.isfile(fileInfo[3]):
                                cmd = 'del "' + fileInfo[3] + '" /F'
                                print(cmd)
                                os.system(cmd)
                        except Exception as e:
                            print(e)
                    deleteFile(fileInfo[0])
            self.init()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = regularManage()
    widget.show()
    sys.exit(app.exec_())
