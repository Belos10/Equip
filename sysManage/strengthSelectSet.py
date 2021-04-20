from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem,QTableWidgetItem,QAbstractItemView, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.InquiryResult import Inquiry_Result
from sysManage.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, add_UnitDict, update_Unit_Dict, selectUnitDictByUper, del_Unit_Dict, del_Unit_And_Child
from sysManage.Stren_Inquiry import Stren_Inquiry
from widgets.select_set import Widget_Select_Set



class strengthSelectSet(QWidget, Widget_Select_Set):
    def __init__(self, parent=None):
        super(strengthSelectSet, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.changeFirst = True


        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)

        self.first_treeWidget_dict = {}
        self.signalConnect()


    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)
        self.tb_result.itemClicked.connect(self.slotClickedRow)
        self.pb_update.clicked.connect(self.slotUpdate)
        self.pushButton.clicked.connect(self.slotFirstInit)
        self.pb_del.clicked.connect(self.slotDelDict)

    def slotDisconnect(self):
        self.pb_add.clicked.disconnect(self.slotAddDict)
        self.tb_result.itemClicked.disconnect(self.slotClickedRow)
        self.pushButton.clicked.disconnect(self.slotFirstInit)
        self.pushButton.clicked.disconnect(self.slotFirstInit)

    def slotFirstInit(self):
        self._initTreeWidget("", self.tw_first)
        self._initUnitTableWidget()
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(False)

    def _initUnitTableWidget(self):
        sql = " select * from dept"
        result = Clicked(sql)

        header = ['单位编号', '单位名称', '上级单位编号']
        self.tb_result.setColumnCount(3)
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)

        print(result)

    def _initTreeWidget(self, root, mother):

        if root == '':
            sql = 'select Dept_Name,Dept_ID from dept where Dept_Uper = ""'
        else:
            sql = " select Dept_Name,Dept_ID from dept where Dept_Uper='" + root + "'"

        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            self.first_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initTreeWidget(data[1], item)

    def slotClickedRow(self):
        print(self.tb_result.currentRow())
        currentRow = self.tb_result.currentRow()
        if self.changeFirst:
            self.le_unitID.setText(self.tb_result.item(currentRow, 0).text())
            self.le_unitName.setText(self.tb_result.item(currentRow, 1).text())
            self.le_unitUper.setText(self.tb_result.item(currentRow, 2).text())

    def slotAddDict(self):
        if self.changeFirst:
            if self.le_unitID.text() == "" or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.le_unitUper.text()
                add_UnitDict(Unit_ID, Unit_Name, Unit_Uper)
                self.slotDisconnect()
                self.tb_result.setRowCount(0)
                self.tw_first.setRowCount(0)
                self.signalConnect()
                self._initUnitTableWidget()
                self._initTreeWidget("", self.tw_first)

    def slotUpdate(self):
        if self.changeFirst:
            if (self.tb_result.item(self.tb_result.currentRow(), 0).text() != self.le_unitID.text()) or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.le_unitUper.text()
                update_Unit_Dict(Unit_ID, Unit_Name, Unit_Uper)
                self.slotDisconnect()
                self.tb_result.clear()
                self.tw_first.clear()
                self.signalConnect()
                self._initUnitTableWidget()
                self._initTreeWidget("", self.tw_first)

    def slotDelDict(self):
        if self.changeFirst:
            haveChild = selectUnitDictByUper(self.le_unitID.text())
            if haveChild:
                print("have")
                reply = QMessageBox.question(self, '删除', '该单位有下级单位，是否将下级单位一起删除？', QMessageBox.Yes,
                                                 QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    del_Unit_And_Child(self.le_unitID.text())
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.clear()
                    self.tw_first.clear()
                    self.signalConnect()
                    self._initUnitTableWidget()
                    self._initTreeWidget("", self.tw_first)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
            else:
                reply = QMessageBox.question(self, '删除', '确定删除吗？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    del_Unit_Dict(self.le_unitID.text())
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.setRowCount(0)
                    self.tw_first.setRowCount(0)
                    self.signalConnect()
                    self._initUnitTableWidget()
                    self._initTreeWidget("", self.tw_first)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)

