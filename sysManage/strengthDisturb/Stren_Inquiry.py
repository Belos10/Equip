from database.SD_EquipmentBanlanceSql import deleteByYear
from widgets.strengthDisturb.stren_inquiry import Widget_Stren_Inquiry
from PyQt5.QtWidgets import QWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QMessageBox, \
    QCheckBox, QListWidgetItem, QInputDialog
from PyQt5 import QtWidgets
from sysManage.strengthDisturb.InquiryResult import Inquiry_Result
from sysManage.strengthDisturb.addStrenthInfo import AddStrenthInfo
from database.strengthDisturbSql import *
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from sysManage.userInfo import get_value

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
        #设置当前查询的年份
        self.currentYear = None

        # 初始化界面
        self._initStrenInquiry()

        # 信号连接
        self.signalConnectSlot()

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    '''
        功能：
            当选择出厂年份时，设置当前可选项和不可选项,并初始化年份目录
    '''

    def _initStrenInquiry(self):
        self.initUserInfo()
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(True)
        self.le_second.setDisabled(True)
        self.tw_first.setDisabled(True)
        self.tw_second.setDisabled(True)
        self.inquiry_result.setDisabled(True)
        #self.tb_inqury.setDisabled(False)
        #self.tb_rechoose.setDisabled(False)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        self.yearList = []

        #初始化年份选择列表
        self._initSelectYear_()
        #self.cb_yearAll = QCheckBox(self.sa_yearChoose)

    '''
        功能：
            点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''

    def slotClickedInqury(self):
        self.initUserInfo()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.inquiry_result.setDisabled(False)
#        self.tb_inqury.setDisabled(True)
#        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_chooseYear.currentItem().text()
        print("currentYear :", self.currentYear)

        self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self.initUnitTreeWidget(stack, root)

        equipInfo = None
        equipInfo = selectEquipInfoByEquipUper("")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self.initEquipTreeWidget(stack, root)
            # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
            # self._initUnitTreeWidget("", self.tw_first)

    def initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

    '''
                功能：
                    单位目录的初始化，显示整个单位表
                    参数表：root为上级单位名字，mother为上级节点对象
        '''

    def initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
            item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

    # 信号与槽的连接
    def signalConnectSlot(self):
        #点击某个年份后显示单位和装备目录
        self.lw_chooseYear.clicked.connect(self.slotClickedInqury)

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

        #新增某个年份
        self.tb_add.clicked.connect(self.slotAddNewYear)

        self.tb_del.clicked.connect(self.slotDelYear)

        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)

    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break
    def slotSelectEquip(self):
        findText = self.le_second.text()
        for i, item in self.second_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_second.setCurrentItem(item)
                break

    def slotDelYear(self):
        currentRow = self.lw_chooseYear.currentRow()
        if currentRow == 0:
            reply = QMessageBox.question(self, '删除', '是否删除所有年份以及年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
        if currentRow < 0:
            reply = QMessageBox.question(self, '删除', '请选中某年进行删除', QMessageBox.Yes)
        else:
            currentYear = self.lw_chooseYear.currentItem().text()
            reply = QMessageBox.question(self, '删除', '是否删除当前年份以及当前年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delStrengthYearByYear(currentYear)
                deleteByYear(currentYear)
                deleteByYear(str(int(currentYear) + 1))
                self._initSelectYear_()
            else:
                return

    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if ok:
            reply = QMessageBox.question(self, '新增', '是否将去年的数据同时导入今年？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                insertIntoStrengthYear(year)
                self._initSelectYear_()
            else:
                allyearInfo = selectAllStrengthYear()
                haveBefore = False
                for yearInfo in allyearInfo:
                    if int(yearInfo[1]) - 1 == year:
                        haveBefore = True
                if haveBefore:
                    insertBeforYearIntoStrength(year)
                else:
                    insertIntoStrengthYear(year)
                self._initSelectYear_()


    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass

    #初始化年份listwidget
    def _initSelectYear_(self):
        self.currentYearListItem = {}
        self.yearList = []
        self.lw_chooseYear.clear()
        allyearList = selectAllStrengthYear()

        for year in allyearList:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_chooseYear.addItem(item)
            self.currentYearListItem[year] = item

    #当信息录入界面点击保存按钮时
    def slotSaveUpdate(self):
        Unit_ID = self.add_strenth_info.strgenthInfo[1]
        Equip_ID = self.add_strenth_info.strgenthInfo[0]
        orginRowNum = self.add_strenth_info.orginRowNum
        currentRowNum = self.add_strenth_info.tableWidget.rowCount()
        columnNum = self.add_strenth_info.tableWidget.columnCount()
        allYear = selectAllStrengthYear()
        for i in range(currentRowNum):
            for j in range(columnNum):
                if self.add_strenth_info.tableWidget.item(i, j).text() == '':
                    reply = QMessageBox.question(self, '保存', '数据不能为空，保存失败', QMessageBox.Yes,
                                                 QMessageBox.Cancel)
                    return
        if columnNum == 8:
            for i in range(currentRowNum - orginRowNum):
                print("data:", Unit_ID, Equip_ID,
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 1).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 3).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 4).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 5).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text(),
                      self.add_strenth_info.tableWidget.item(i + orginRowNum, 7).text(),
                      self.currentYear)
                haveYear = False
                # 添加新增的数据
                year = self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text()
                if year.isdigit() == False:
                    reply = QMessageBox.question(self, '增加', '第' + str(i + orginRowNum + 1) + "行年份不是整数，添加失败",QMessageBox.Yes)
                    continue
                for y in allYear:
                    if y == year:
                        haveYear = True
                #if haveYear == False:
                    #print("meiyounian")
                    #reply = QMessageBox.question(self, '增加', '第' + str(i + orginRowNum + 1) + "行年份不存在，添加失败",
                                                 #QMessageBox.Yes)
                #else:
                addDataIntoInputInfo(Unit_ID, Equip_ID,
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 1).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 3).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 4).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 5).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text(),
                                        self.add_strenth_info.tableWidget.item(i + orginRowNum, 7).text(),
                                        self.currentYear)

            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()
        elif columnNum == 7:
            # 添加新增的数据
            for i in range(currentRowNum - orginRowNum):
                year = self.add_strenth_info.tableWidget.item(i + orginRowNum, 1).text()
                if year.isdigit() == False:
                    reply = QMessageBox.question(self, '增加', '第' + str(i + orginRowNum + 1) + "行年份不是整数，添加失败",QMessageBox.Yes)
                    continue
                for y in allYear:
                    if y == year:
                        haveYear = True
                #if haveYear == False:
                   # reply = QMessageBox.question(self, '增加', '第' + str(i + orginRowNum + 1) + "行年份不存在，添加失败",
                                                 #QMessageBox.Yes)
                #else:
                addDataIntoInputInfo(Unit_ID, Equip_ID,
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text(),
                                     "1",
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 1).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 2).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 3).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 4).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 5).text(),
                                     self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text(),
                                     self.yearList[0])
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()
        self.groupBox.setDisabled(False)
        self.groupBox_2.setDisabled(False)

    '''
        功能：
            录入界面的返回按钮
    '''
    def slotAddWidgetReturn(self):
        reply = QMessageBox.question(self, '返回', '是否不保存直接返回？', QMessageBox.Yes,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.groupBox.setDisabled(False)
            self.groupBox_2.setDisabled(False)
            self.slotInquryStrengthResult()
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
                        self.add_strenth_info._initTableWidget_(resultRowInfo, self.currentYear, self.inquiry_result.currentFactoryYear)
                        self.groupBox.setDisabled(True)
                        self.groupBox_2.setDisabled(True)
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
                                                                   self.currentCheckedEquipList, self.currentYear)

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
            else:
                return None

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
            else:
                return None
