from widgets.dictSelect.factorySet import Widget_Factory_Set
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTableWidgetItem,QHeaderView, QAbstractItemView,QMessageBox
from PyQt5.Qt import QRegExp, QRegExpValidator
from database.dictSelect.factorySetSql import *
#new
regx = QRegExp("[0-9]*")
class factorySet(QWidget, Widget_Factory_Set):
    def __init__(self, parent=None):
        super(factorySet, self).__init__(parent)
        self.setupUi(self)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.signalConnect()
        validator = QRegExpValidator(regx)
        self.le_tel1.setValidator(validator)
        self.le_tel2.setValidator(validator)

    def initWidget(self):
        self.le_name.clear()
        self.le_id.clear()
        self.le_address.clear()
        self.le_tel1.clear()
        self.le_connect.clear()
        self.le_represent.clear()
        self.le_tel2.clear()
        self.tw_result.clear()
        self.initTableWidget()

    def initTableWidget(self):
        title = ["厂家编号", '厂家名字', '厂家地址','厂家联系人', '厂家联系方式', '军代表', '军代表联系方式']
        self.tw_result.setColumnCount(len(title))
        self.tw_result.setHorizontalHeaderLabels(title)
        result = selectAllDataAboutFactory()
        if result:
            self.tw_result.setRowCount(len(result))
            for i, resultInfo in enumerate(result):
                item = QTableWidgetItem(resultInfo[0])
                self.tw_result.setItem(i, 0, item)
                item = QTableWidgetItem(resultInfo[1])
                self.tw_result.setItem(i, 1, item)
                item = QTableWidgetItem(resultInfo[2])
                self.tw_result.setItem(i, 2, item)
                item = QTableWidgetItem(resultInfo[3])
                self.tw_result.setItem(i, 3, item)
                item = QTableWidgetItem(resultInfo[4])
                self.tw_result.setItem(i, 4, item)
                item = QTableWidgetItem(resultInfo[5])
                self.tw_result.setItem(i, 5, item)
                item = QTableWidgetItem(resultInfo[6])
                self.tw_result.setItem(i, 6, item)
        else:
            self.tw_result.setRowCount(0)

    def signalConnect(self):
        self.tw_result.clicked.connect(self.slotClickedTableWidget)
        self.pb_add.clicked.connect(self.slotAddFactoryInfo)
        self.pb_update.clicked.connect(self.slotUpdateFactoryInfo)
        #self.pb_del.clicked.connect(self.slotDelFactoryInfo)
        #self.pb_input.clicked.connect(self.slotInputFactoryInfo)
        #self.pb_output.clicked.connect(self.slotOutputFactoryInfo)

    def slotAddFactoryInfo(self):
        if haveFactoryID(self.le_id.text()) == True:
            QMessageBox.information(self,"新增", "新增失败，该厂家编号已存在", QMessageBox.Yes)
            return
        else:
            ID = self.le_id.text()
            name = self.le_name.text()
            if name == "":
                QMessageBox.information(self, "新增", "新增失败，厂家名字不能为空", QMessageBox.Yes)
                return
            if haveFactoryName(name) == True:
                QMessageBox.information(self, "新增", "新增失败，厂家名字不能重复", QMessageBox.Yes)
                return
            address = self.le_address.text()
            connect = self.le_connect.text()
            tel1 = self.le_tel1.text()
            represent = self.le_represent.text()
            tel2 = self.le_tel2.text()

            addSuccess = addInfoIntoFactory(ID, name, address, connect, tel1, represent, tel2)
            if addSuccess == True:
                QMessageBox.information(self, "新增", "新增成功", QMessageBox.Yes)
                self.initTableWidget()
                return
            else:
                QMessageBox.information(self, "新增", str(addSuccess) + ",新增失败", QMessageBox.Yes)
                return

    def slotUpdateFactoryInfo(self):
        if self.tw_result.currentRow() < 0:
            return
        else:
            row = self.tw_result.currentRow()
            if self.tw_result.item(row, 0):
                if self.tw_result.item(row, 0).text() != self.le_id.text():
                    QMessageBox.information(self, "修改", "修改失败, 厂家编号不可修改", QMessageBox.Yes)
                    return
            ID = self.le_id.text()
            name = self.le_name.text()
            if name != self.tw_result.item(row, 1).text():
                QMessageBox.information(self, "修改", "修改失败，厂家名字不能修改", QMessageBox.Yes)
                return
            address = self.le_address.text()
            connect = self.le_connect.text()
            tel1 = self.le_tel1.text()
            represent = self.le_represent.text()
            tel2 = self.le_tel2.text()

            addSuccess = updateInfoIntoFactory(ID, name, address, connect, tel1, represent, tel2)
            if addSuccess == True:
                QMessageBox.information(self, "修改", "修改成功", QMessageBox.Yes)
                self.initTableWidget()
                return
            else:
                QMessageBox.information(self, "修改", str(addSuccess) + ",修改失败", QMessageBox.Yes)
                return
    def slotClickedTableWidget(self):
        row = self.tw_result.currentRow()
        if row < 0:
            return
        else:
            id = self.tw_result.item(row, 0).text()
            name = self.tw_result.item(row, 1).text()
            address = self.tw_result.item(row, 2).text()
            connect = self.tw_result.item(row, 3).text()
            tel1 = self.tw_result.item(row, 4).text()
            represent = self.tw_result.item(row, 5).text()
            tel2 = self.tw_result.item(row, 6).text()
            self.le_id.setText(id)
            self.le_name.setText(name)
            self.le_address.setText(address)
            self.le_connect.setText(connect)
            self.le_tel1.setText(tel1)
            self.le_represent.setText(represent)
            self.le_tel2.setText(tel2)