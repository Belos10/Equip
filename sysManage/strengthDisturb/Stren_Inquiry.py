from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox, \
    QListWidgetItem

from database.strengthDisturbSql import *
from sysManage.component import getMessageBox, getIntInputDialog
from sysManage.strengthDisturb.InquiryResult import Inquiry_Result
from sysManage.strengthDisturb.addStrenthInfo import AddStrenthInfo
from sysManage.userInfo import get_value
from widgets.strengthDisturb.stren_inquiry import Widget_Stren_Inquiry

'''
    类功能：
        管理查询结果界面，包含查询结果相关逻辑代码
        实力查询 左边部分 年份、单位、装备xxx
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
        self.tb_input.setDisabled(True)
        self.tb_input.setVisible(False)
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
        # 信号连接
        self.signalConnectSlot()

    # 登录用户权限判断
    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    # 信号与槽的连接
    def signalConnectSlot(self):
        # 点击某个年份后显示单位和装备目录
        self.lw_chooseYear.clicked.connect(self.slotClickedInqury)

        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotInquryStrengthResult)

        # 双击某行进入录入界面
        self.inquiry_result.tw_inquiryResult.doubleClicked.connect(self.slotInputStrengthInfo)

        # 录入界面返回按钮
        self.add_strenth_info.pb_back.clicked.connect(self.slotAddWidgetReturn)

        # 录入界面保存按钮
        self.add_strenth_info.pb_Save.clicked.connect(self.slotSaveUpdate)

        # 新增某个年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        self.tb_del.clicked.connect(self.slotDelYear)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)


    '''
        功能：
            当选择出厂年份时，设置当前可选项和不可选项,并初始化年份目录
    '''
    def initStrenInquiry(self):
        self.inquiry_result.tw_inquiryResult.clear()
        self.initUserInfo()
        self.tw_first.clear()
        self.tw_second.clear()
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
        self.inquiry_result.tw_inquiryResult.setRowCount(0)
        self.yearList = []

        #初始化年份选择列表
        self.initSelectYear()

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
        self.inquiry_result.setDisabled(True)
        self.inquiry_result.allButtonDisabled()

        self.currentYear = self.lw_chooseYear.currentItem().text()
        print("currentYear :", self.currentYear)

        if self.userInfo:
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

    # 删除年份
    def slotDelYear(self):
        currentRow = self.lw_chooseYear.currentRow()
        if currentRow < 0:
            return
        else:
            currentYear = self.lw_chooseYear.currentItem().text()
            reply = getMessageBox('删除', '是否删除当前年份以及当前年份下所有数据？', True, True)
            if reply == QMessageBox.Ok:
                delSuccess = delStrengthYearByYear(currentYear)
                if delSuccess != True:
                    getMessageBox('删除', str(delSuccess) + ',删除失败', True, False)
                    return
                getMessageBox('删除', '删除成功', True, False)
                self.initSelectYear()
            else:
                return


    def slotAddNewYear(self):
        year = 0
        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)
        if ok:
            allyearInfo = selectAllStrengthYear()
            if isHaveStrengthYear(str(year)):
                getMessageBox("新增", "该年份已经存在，拒绝添加！", True, False)
                return
            else:
                insertSuccess = insertIntoStrengthYear(year)
                if insertSuccess == True:
                    getMessageBox( "新增", "新增成功！", True, False)
                else:
                    getMessageBox("新增", str(insertSuccess) + ",新增失败！", True, False)
                self.initSelectYear()

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass


    #初始化年份listwidget
    def initSelectYear(self):
        self.yearList = []
        self.lw_chooseYear.clear()
        allyearList = selectAllStrengthYear()

        for year in allyearList:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_chooseYear.addItem(item)
        if self.yearList:
            self.tb_add.setDisabled(1)
        else:
            self.tb_add.setDisabled(0)


    #当信息录入界面点击保存按钮时
    def slotSaveUpdate(self):
        Unit_ID = self.add_strenth_info.strgenthInfo[1]
        Equip_ID = self.add_strenth_info.strgenthInfo[0]
        orginRowNum = self.add_strenth_info.orginRowNum
        currentRowNum = self.add_strenth_info.tableWidget.rowCount()
        columnNum = self.add_strenth_info.tableWidget.columnCount()
        allYear = selectAllStrengthYear()
        if columnNum == 8:
            for i in range(currentRowNum - orginRowNum):
                # 添加新增的数据
                year = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 2).currentText()
                num = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 1).text()
                ID = self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text()
                haveID = selectIDWhetherExitFromInputInfo(Equip_ID, Unit_ID, self.currentYear, ID)
                if ID == "":
                    getMessageBox("增加", "第 " + str(currentRowNum) + " 添加失败，批次号不能为空", True, False)
                    continue
                if haveID:
                    getMessageBox("增加", "第 " + str(currentRowNum) + " 添加失败，批次号重复", True, False)

                    continue
                if num == "":
                    getMessageBox("增加", "第 " + str(currentRowNum) + " 添加失败，数量不能为空", True, False)

                    continue
                factory = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 3).currentText()
                state = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 4).currentText()
                arrive = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 5).currentText()
                confirm = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 6).currentText()
                other = self.add_strenth_info.tableWidget.item(i + orginRowNum, 7).text()
                addSuccess = addDataIntoInputInfo(Unit_ID, Equip_ID,
                                        ID,
                                        num,
                                        year,
                                        factory,
                                        state,
                                        arrive,
                                        confirm,
                                        other,
                                        self.currentYear)
                if addSuccess != True:
                    getMessageBox("增加", "第 " + currentRowNum + " 添加失败，由于:" + addSuccess, True)

                    continue
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()
        elif columnNum == 7:
            # 添加新增的数据
            for i in range(currentRowNum - orginRowNum):
                # 添加新增的数据
                year = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 1).currentText()
                ID = self.add_strenth_info.tableWidget.item(i + orginRowNum, 0).text()
                haveID = selectIDWhetherExitFromInputInfo(Equip_ID, Unit_ID, self.currentYear, ID)
                if ID == "":
                    getMessageBox("增加", "第 " + str(i + orginRowNum) + " 添加失败，批次号不能为空", True, False)

                    continue
                if haveID:
                    getMessageBox("增加", "第 " + str(i + orginRowNum) + " 添加失败，批次号重复", True, False)

                    continue
                factory = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 2).currentText()
                state = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 3).currentText()
                arrive = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 4).currentText()
                confirm = self.add_strenth_info.tableWidget.cellWidget(i + orginRowNum, 5).currentText()
                other = self.add_strenth_info.tableWidget.item(i + orginRowNum, 6).text()
                addSuccess = addDataIntoInputInfo(Unit_ID, Equip_ID,
                                                  ID,
                                                  "1",
                                                  year,
                                                  factory,
                                                  state,
                                                  arrive,
                                                  confirm,
                                                  other,
                                                  self.currentYear)
                if addSuccess != True:

                    getMessageBox("增加", "第 " + currentRowNum + " 添加失败，由于:" + addSuccess, True, False)
                    haveError = True
                    continue
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.slotInquryStrengthResult()
        self.groupBox.setDisabled(False)
        self.groupBox_2.setDisabled(False)

    '''
        功能：
            录入界面的返回按钮
    '''
    def slotAddWidgetReturn(self):
        reply = getMessageBox('返回', '是否不保存直接返回?', True, True)

        if reply == QMessageBox.Ok:
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
        if self.currentColumn < 0 or self.currentRow < 0:
            return
        if self.currentColumn != 2:
            for i, resultRowInfo in self.inquiry_result.currentInquiryResult.items():
                if i == self.currentRow:
                    unitHaveChild = selectUnitIsHaveChild(resultRowInfo[1])
                    equipHaveChild = selectEquipIsHaveChild(resultRowInfo[0])
                    equipInfo = selectEquipInfoByEquipID(resultRowInfo[0])
                    if unitHaveChild or equipHaveChild:
                        getMessageBox('录入', '该单位或装备不是末级，无法录入', True, False)
                        return
                    if equipInfo:
                        print("--------", equipInfo)
                        if equipInfo[0][3] == "空":
                            getMessageBox('录入', '请设置该装备录入类型，无法录入', True, False)
                            return
                        elif equipInfo[0][3] == "逐批录入信息":
                            self.add_strenth_info.isMutilInput = True
                            print("''''''''''''''", self.add_strenth_info.isMutilInput)
                        elif equipInfo[0][3] == "逐号录入信息":
                            self.add_strenth_info.isMutilInput = False
                    if self.inquiry_result.chooseFactoryYear.selectAll:
                        self.sw_strenSelectMan.setCurrentIndex(1)
                        self.add_strenth_info._initTableWidget_(resultRowInfo, self.currentYear)
                        self.groupBox.setDisabled(True)
                        self.groupBox_2.setDisabled(True)
                        break
                    else:
                        getMessageBox('录入', '请将查看出厂年份修改为全部', True, False)
                        return

        else:
            pass

    '''
        功能：
            查询实力结果
    '''
    def slotInquryStrengthResult(self):
        self.inquiry_result.setDisabled(False)
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                self.currentCheckedUnitList.append(unitID)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)
        if(self.currentCheckedUnitList and self.currentCheckedEquipList):
            self.inquiry_result.allButtonAvailabled()
        # if self.currentCheckedUnitList == [] or self.currentCheckedEquipList == []:
        #     headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力',
        #                   '单独建账',
        #                   '正常到位']
        #     self.inquiry_result.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        #     self.inquiry_result.tw_inquiryResult.setColumnCount(len(headerlist))
        #     self.inquiry_result.tw_inquiryResult.setRowCount(0)
        #     return

        self.inquiry_result._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList,
                                                                   self.currentCheckedEquipList, self.currentYear)
