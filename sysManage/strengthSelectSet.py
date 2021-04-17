from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem,QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.InquiryResult import Inquiry_Result
from sysManage.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, insert_Clicked
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

        self.pushButton.clicked.connect(self.slotFirstInit)
        #self.tb_result.currentItemChanged.connect(self.slotClickedRow)
        self.first_treeWidget_dict = {}

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
            sql = 'select Dept_Name,Dept_ID from dept where Dept_Uper is null'
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
        if self.changeFirst:
            print(self.tb_result.setCurrentItem())