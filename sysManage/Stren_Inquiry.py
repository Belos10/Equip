from PyQt5.QtWidgets import QMainWindow
from widgets.stren_inquiry import Widget_Stren_Inquiry
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.InquiryResult import Inquiry_Result
from sysManage.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, insert_Clicked

'''
    类功能：
        管理查询结果界面，包含查询结果相关逻辑代码
'''

first_treeWidget_dict = {}
second_treeWidget_dict = {}

class Stren_Inquiry(QWidget, Widget_Stren_Inquiry):
    #signalInquiry = pyqtSignal(str, str, name="signalInquiry")
    def __init__(self, parent=None):
        super(Stren_Inquiry, self).__init__(parent)
        self.setupUi(self)
        self.inquiry_result = Inquiry_Result()
        self.add_strenth_info = AddStrenthInfo()
        #初始显示实力查询界面
        self.sw_strenSelectMan.addWidget(self.inquiry_result)
        self.sw_strenSelectMan.setCurrentIndex(0)

        self.sw_strenSelectMan.addWidget(self.add_strenth_info)

        self.signalConnectSlot()
        #初始化TreeWidget
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self._initTreeWidget("", self.tw_first)
        print(first_treeWidget_dict)

    #信号与槽的连接
    def signalConnectSlot(self):
        # 按查询按钮时第一个目录的查询
        self.pb_firstSelect.clicked.connect(self.slotFilterFirstTreeWidget)
        # 按查询按钮时第二个目录的查询
        self.pb_secondSelect.clicked.connect(self.slotFilterSecondTreeWidget)
        # 按搜索框更改第一个目录的查询
        self.le_first.textChanged.connect(self.slotFilterFirstTreeWidget)
        # 按搜索框更改第二个目录的查询
        self.le_second.textChanged.connect(self.slotFilterSecondTreeWidget)
        # 将第一个目录和第二个目录进行关联
        self.tw_first.currentItemChanged.connect(self.slotSelectIndex)
        # 第二个目录选定后进行查询并显示结果
        self.tw_second.currentItemChanged.connect(self.slotInquiry)
        # 点击返回按钮返回第零个界面
        self.add_strenth_info.pb_back.clicked.connect(self.slotBack)
        self.inquiry_result.tw_inquiryResult.itemDoubleClicked.connect(self.slotDoubleClickedTableItem)
        self.add_strenth_info.pb_Save.clicked.connect(self.slotSaveAddInfo)
        self.add_strenth_info.pb_Delete.clicked.connect(self.add_strenth_info.deleteNote)
        self.inquiry_result.pb_clearCheck.clicked.connect(self.inquiry_result.deleteInquiryResult)
        self.inquiry_result.pb_clearAll.clicked.connect(self.inquiry_result.deleteAllInquiryResult)

    #信号与槽连接的断开
    def signalDisconnectSlot(self):
        self.pb_firstSelect.clicked.disconnect(self.slotFilterFirstTreeWidget)
        # 按查询按钮时第二个目录的查询
        self.pb_secondSelect.clicked.disconnect(self.slotFilterSecondTreeWidget)
        # 按搜索框更改第一个目录的查询
        self.le_first.textChanged.disconnect(self.slotFilterFirstTreeWidget)
        # 按搜索框更改第二个目录的查询
        self.le_second.textChanged.disconnect(self.slotFilterSecondTreeWidget)
        # 将第一个目录和第二个目录进行关联
        self.tw_first.currentItemChanged.disconnect(self.slotSelectIndex)
        # 第二个目录选定后进行查询并显示结果
        self.tw_second.currentItemChanged.disconnect(self.slotInquiry)
        # 点击返回按钮返回第零个界面
        self.add_strenth_info.pb_back.clicked.disconnect(self.slotBack)
        self.inquiry_result.tw_inquiryResult.itemDoubleClicked.disconnect(self.slotDoubleClickedTableItem)
        self.add_strenth_info.pb_Save.clicked.disconnect(self.slotSaveAddInfo)
        self.add_strenth_info.pb_Delete.clicked.disconnect(self.add_strenth_info.deleteNote)
        self.inquiry_result.pb_clearCheck.clicked.disconnect(self.inquiry_result.deleteInquiryResult)
        self.inquiry_result.pb_clearAll.clicked.disconnect(self.inquiry_result.deleteAllInquiryResult)

    def slotBack(self,event):
        reply = QtWidgets.QMessageBox.question(self, '提示', '是否退出信息录入?',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.sw_strenSelectMan.setCurrentIndex(0)


    def slotSaveAddInfo(self):
        OrignNum = self.add_strenth_info.OrignNum
        print(self.add_strenth_info.OrignNum, self.add_strenth_info.tableWidget.rowCount())
        if self.add_strenth_info.OrignNum == self.add_strenth_info.tableWidget.rowCount():
            self.sw_strenSelectMan.setCurrentIndex(0)
            return
        Unit_ID = self.add_strenth_info.UnitID
        Equip_ID = self.add_strenth_info.EquipID
        for i in range(self.add_strenth_info.row_num - OrignNum):
            ID = self.add_strenth_info.tableWidget.item(i + OrignNum, 0).text()
            num = self.add_strenth_info.tableWidget.item(i + OrignNum, 1).text()
            year = self.add_strenth_info.tableWidget.item(i + OrignNum, 2).text()
            shop = self.add_strenth_info.tableWidget.item(i + OrignNum, 3).text()
            state = self.add_strenth_info.tableWidget.item(i + OrignNum, 4).text()
            arrive = self.add_strenth_info.tableWidget.item(i + OrignNum, 5).text()
            confirm = self.add_strenth_info.tableWidget.item(i + OrignNum, 6).text()
            other = self.add_strenth_info.tableWidget.item(i + OrignNum, 7).text()
            print(ID, num, year, shop, state, arrive, confirm, other)
            insert_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other)


        self.sw_strenSelectMan.setCurrentIndex(0)

    def slotDoubleClickedTableItem(self):
        currentRow = self.inquiry_result.tw_inquiryResult.currentRow()
        #self._initWeight()
        for key, data in self.inquiry_result.currentInquiryResult.items():
            if key == currentRow:
                self.add_strenth_info._initWeight(data)
                break

        self.sw_strenSelectMan.setCurrentIndex(1)

    def slotFirstChange(self):
        #self.tw_second.clear()
        self.inquiry_result.tw_inquiryResult.clear()

    '''
        初始化TreeWidget
    '''
    def _initTreeWidget(self, root, mother):

        if root == '':
            sql = 'select Dept_Name,Dept_ID from dept where Dept_Uper is null'
        else:
            sql = " select Dept_Name,Dept_ID from dept where Dept_Uper='" + root + "'"

        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            first_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initTreeWidget(data[1], item)

    '''
        功能：
            让第一个目录进行过滤筛选出想选择的项目
    '''
    def slotFilterFirstTreeWidget(self):
        """以text开头作为过滤条件示例"""
        find = False
        text = self.le_first.text()

        cursor = QTreeWidgetItemIterator(self.tw_first)
        while cursor.value():
            item = cursor.value()
            if item.text(0).startswith(text):
                self.tw_first.setCurrentItem(item)
                find = True
                # 需要让父节点也显示,不然子节点显示不出来
                try:
                    self.tw_first.setCurrentItem(item)
                    find = True
                except Exception:
                    pass
            else:
                pass

            cursor = cursor.__iadd__(1)

    '''
        功能：
            让第二个目录进行过滤筛选出想选择的项目
    '''
    def slotFilterSecondTreeWidget(self):
        """以text开头作为过滤条件示例"""
        text = self.le_second.text()
        find = False
        cursor = QTreeWidgetItemIterator(self.tw_second)
        while cursor.value():
            item = cursor.value()
            if item.text(0).startswith(text):
                self.tw_second.setCurrentItem(item)
                # 需要让父节点也显示,不然子节点显示不出来
                try:
                    self.tw_second.setCurrentItem(item)
                except Exception:
                    pass
            else:
                pass

            cursor = cursor.__iadd__(1)

    '''
        功能：
            将第一个目录与第二个目录进行关联
    '''

    def _initSecondTreeWidget(self, root, mother, UnitID):

        if UnitID:
            sql = "select Equip_Name,Equip_ID from equip where Unit_ID ='" + UnitID + "'" + "AND Equip_Uper is NUll"
            #print(sql)
        else:

            sql = "select Equip_Name,Equip_ID from equip where Equip_Uper ='" + root + "'"
            #print(sql)
        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            second_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initSecondTreeWidget(data[1], item, 0)


    def slotSelectIndex(self):
        self.signalDisconnectSlot()
        #在clear前要现将该控件上的信号和槽的连接进行disconnect，不然会发生段错误
        self.inquiry_result.tw_inquiryResult.clear()
        self.tw_second.clear()

        for UnitID, item in first_treeWidget_dict.items():
            if item == self.tw_first.currentItem():

                #print(sql)
                self._initSecondTreeWidget("", self.tw_second, UnitID)
                #break
        self.signalConnectSlot()


    '''
        功能：
            查询想要查询的结果并显示
    '''
    def slotInquiry(self):
        UnitID = 0
        EquitID = 0
        isRoot = True
        for firstID, firstItem in first_treeWidget_dict.items():
            if self.tw_first.currentItem() == firstItem:
                UnitID = firstID
                break

        for secondID, secondItem in second_treeWidget_dict.items():
            if self.tw_second.currentItem() == secondItem:
                EquitID = secondID
                break
        if self.tw_second.currentItem().child(0):
            isRoot = True
            print("True")
        else:
            isRoot = False
            print("False")
        self.inquiry_result.InquiryResult(UnitID, EquitID, isRoot)
