from widgets.strengthDisturb.stren_inquiry import Widget_Stren_Inquiry
from PyQt5.QtWidgets import QWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QMessageBox, QCheckBox
from PyQt5 import QtWidgets
from sysManage.strengthDisturb.InquiryResult import Inquiry_Result
from sysManage.strengthDisturb.addStrenthInfo import AddStrenthInfo
from database.strengthDisturbSql import selectAllDataAboutStrengthYear, selectUnitInfoByDeptUper, \
    selectEquipInfoByEquipUper \
    , selectEquipIsHaveChild, selectUnitIsHaveChild, addDataIntoInputInfo
from PyQt5.Qt import Qt

'''
    类功能：
        管理查询结果界面，包含查询结果相关逻辑代码
'''
# 更新
first_treeWidget_dict = {}
second_treeWidget_dict = {}


class Stren_Inquiry(QWidget, Widget_Stren_Inquiry):
    # signalInquiry = pyqtSignal(str, str, name="signalInquiry")
    def __init__(self, parent=None):
        super(Stren_Inquiry, self).__init__(parent)
        self.setupUi(self)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.inquiry_result = Inquiry_Result()  # 右边显示查询结果
        self.add_strenth_info = AddStrenthInfo()  # 录入数据

        # 将查询结果界面和录入数据界面嵌入stackWidget
        self.sw_strenSelectMan.addWidget(self.inquiry_result)
        self.sw_strenSelectMan.addWidget(self.add_strenth_info)

        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        # 设置当前显示查询结果界面
        self.sw_strenSelectMan.setCurrentIndex(0)

        # 设置当前查询的年份的list
        self.yearList = []

        # 初始化界面
        self._initStrenInquiry()

        # 信号连接
        self.signalConnectSlot()

    '''
        功能：
            当选择出厂年份时，设置当前可选项和不可选项,并初始化年份目录
    '''

    def _initStrenInquiry(self):
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(True)
        self.le_second.setDisabled(True)
        self.tw_first.setDisabled(True)
        self.tw_second.setDisabled(True)
        self.inquiry_result.setDisabled(True)
        self.tb_inqury.setDisabled(False)
        self.tb_rechoose.setDisabled(False)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        self.yearList = []
        self.cb_yearAll = QCheckBox(self.sa_yearChoose)

    '''
        功能：
            点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''

    def slotClickedInqury(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.inquiry_result.setDisabled(False)
        self.tb_inqury.setDisabled(True)
        self.tb_rechoose.setDisabled(False)
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)

    # 信号与槽的连接
    def signalConnectSlot(self):
        # 点击查询按钮后显示单位和装备目录
        self.tb_inqury.clicked.connect(self.slotClickedInqury)

        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotInquryStrengthResult)

        # 设置单位目录级联选中
        # self.tw_first.itemChanged.connect(self.slotCheckedChange)
        # self.tw_second.itemChanged.connect(self.slotCheckedChange)

        # 双击某行进入录入界面
        self.inquiry_result.tw_inquiryResult.doubleClicked.connect(self.slotInputStrengthInfo)

        # 录入界面返回按钮
        self.add_strenth_info.pb_back.clicked.connect(self.slotAddWidgetReturn)

        # 录入界面保存按钮
        self.add_strenth_info.pb_Save.clicked.connect(self.slotSaveUpdate)

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass

    def slotSaveUpdate(self):
        Unit_ID = self.add_strenth_info.strgenthInfo[1]
        Equip_ID = self.add_strenth_info.strgenthInfo[0]
        orginRowNum = self.add_strenth_info.orginRowNum
        currentRowNum = self.add_strenth_info.tableWidget.rowCount()
        columnNum = self.add_strenth_info.tableWidget.columnCount()

        for i in range(currentRowNum):
            for j in range(columnNum):
                if self.add_strenth_info.tableWidget.item(i, j).text() == '':
                    reply = QMessageBox.question(self, '保存', '数据不能为空，保存失败', QMessageBox.Yes,
                                                 QMessageBox.Cancel)
                    return

        if columnNum == 8:
            # 添加新增的数据
            for i in range(currentRowNum - orginRowNum):
                addDataIntoInputInfo(Unit_ID, Equip_ID,
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 1).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 3).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 4).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 5).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 7).text())
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()
        else:
            # 添加新增的数据
            for i in range(currentRowNum - orginRowNum):
                addDataIntoInputInfo(Unit_ID, Equip_ID,
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text(),
                                     1,
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 3).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 4).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 5).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 7).text())
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()

    '''
        功能：
            录入界面的返回按钮
    '''

    def slotAddWidgetReturn(self):
        reply = QMessageBox.question(self, '返回', '是否不保存直接返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.sw_strenSelectMan.setCurrentIndex(0)
        else:
            pass

    '''
        功能：
            双击进入录入界面
    '''

    def slotInputStrengthInfo(self):
        self.currentRow = self.inquiry_result.tw_inquiryResult.currentRow()
        self.currentColumn = self.inquiry_result.tw_inquiryResult.currentColumn()

        if self.currentColumn != 2:
            for i, resultRowInfo in self.inquiry_result.currentInquiryResult.items():
                if i == self.currentRow:
                    unitHaveChild = selectUnitIsHaveChild(resultRowInfo[1])
                    equipHaveChild = selectEquipIsHaveChild(resultRowInfo[0])
                    if unitHaveChild or equipHaveChild:
                        reply = QMessageBox.question(self, '录入', '该单位或装备不是末级，无法录入', QMessageBox.Yes,
                                                     QMessageBox.Cancel)
                    else:
                        self.sw_strenSelectMan.setCurrentIndex(1)
                        self.add_strenth_info._initTableWidget_(resultRowInfo, self.yearList)
                    break
        else:
            pass

    '''
        功能：
            设置级目录联选中状态
    '''

    def slotCheckedChange(self, item, num):
        # 如果是顶部节点，只考虑Child：
        if item.childCount() and not item.parent():  # 判断是顶部节点，也就是根节点
            if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
                    item.child(i).setCheckState(num, 0)
            elif item.checkState(num) == 2:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(num, 2)
        # 如果是底部节点，只考虑Parent
        if item.parent() and not item.childCount():
            parent_item = item.parent()  # 获得父节点
            brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
            checked_num = 0  # 设置计数器
            for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(num)
            if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(num, 0)
            elif checked_num / 2 == brother_item_num:
                parent_item.setCheckState(num, 2)
            else:
                parent_item.setCheckState(num, 1)

            # 中间层需要全面考虑
        if item.parent() and item.childCount():
            if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
                    item.child(i).setCheckState(num, 0)
            elif item.checkState(num) == 2:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(num, 2)
            parent_item = item.parent()  # 获得父节点
            brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
            checked_num = 0  # 设置计数器
            for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(num)
            if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(num, 0)
            elif checked_num / 2 == brother_item_num:
                parent_item.setCheckState(num, 2)
            else:
                parent_item.setCheckState(num, 1)

    '''
        功能：
            查询实力结果
    '''

    def slotInquryStrengthResult(self):
        self.yearList = ['2001']
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                self.currentCheckedUnitList.append(unitID)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        self.inquiry_result._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList,
                                                                   self.currentCheckedEquipList, self.yearList)

    '''
        初始化单位目录
    '''

    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root)

        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    '''
        功能：
            初始化装备目录
    '''

    def _initEquipTreeWidget(self, root, mother):
        if root == '':
            result = selectEquipInfoByEquipUper('')
        else:
            result = selectEquipInfoByEquipUper(root)

        # rowData: (装备编号，装备名称，上级装备编号, 录入类型, 装备类型)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initEquipTreeWidget(rowData[0], item)
