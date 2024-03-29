from PyQt5.Qt import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QMessageBox, QListWidgetItem, QHeaderView, \
    QFileDialog

from database.OrderApplySql import *
from database.strengthDisturbSql import *
from sysManage.component import getMessageBox, getIntInputDialog
from sysManage.userInfo import get_value
from utills.Search import selectUnit
from utills.utillsComponent import CheckableComboBox
from widgets.strengthDisturb.retirement import Widget_Retirement

'''
   订购申请
'''



class OrderApply(QWidget, Widget_Retirement):
    def __init__(self, parent=None):
        super(OrderApply, self).__init__(parent)
        self.setupUi(self)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.userInfo = None
        self.initAll()
        self.signalConnect()

        # 初始化编制数维护界面
    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    def initAll(self):
        self.getUserInfo()
        self.tw_result.setRowCount(0)
        self.tw_result.setColumnCount(0)
        self.tw_first.clear()
        self.tw_second.clear()
        self.le_first.clear()
        self.le_second.clear()
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        self._initUnitTreeWidget('', self.tw_first)
        self._initStrenInquiry()
        self.currentYear = None
        self.currentInquiryResult = {}
        self.resultList = []
        self.unitList = []
        self.equipList = []
        self.year = '全部'
        self.groupBox_2.setDisabled(True)
        self.groupBox_3.setDisabled(True)
        self.pb_input.setVisible(False)
        self.pb_output.setVisible(False)

        # 信号连接
    def signalConnect(self):
        # 点击某个年份后显示单位和装备目录
        self.lw_year.clicked.connect(self.slotClickedInqury)

        # 当前单位目录被点击
        self.tw_first.clicked.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.clicked.connect(self.slotInquryStrengthResult)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)

        self.pb_save.clicked.connect(self.slotSaveRetire)
        self.tb_add.clicked.connect(self.slotAddNewYear)
        self.tb_del.clicked.connect(self.slotDelYear)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.tw_result.itemChanged.connect(self.soltCheckData)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)

    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)


    def slotSelectEquip(self):
        selectUnit(self, self.le_second, self.second_treeWidget_dict, self.tw_second)

    def slotDelYear(self):
        currentRow = self.lw_year.currentRow()

        if currentRow == 0:
            reply = getMessageBox('删除', '是否删除所有年份以及年份下所有数据？', True, True)
            if reply == QMessageBox.Cancel:
                return
            else:
                clearOrderApply()
                self.initAll()
                return
        if currentRow < 0:
            getMessageBox('删除', '请选中某年进行删除', True, False)
        else:
            currentYear = self.lw_year.currentItem().text()
            reply = getMessageBox('删除', '是否删除当前年份以及当前年份下所有数据？', True, True)
            if reply == QMessageBox.Ok:
                deleteOrderApplyYearByYear(currentYear)
                self.initAll()
            else:
                return

    def slotAddNewYear(self):
        year = 0
        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)

        if ok:
            allyearInfo = selectAllOrderApplyYearInfo()
            haveYear = False
            for yearInfo in allyearInfo:
                if str(year) == yearInfo:
                    haveYear = True
                    break
            if haveYear:
                getMessageBox("新增", "年份已存在，新增失败", True, False)
                return
            insertIntoOrderApplyYear(year)
            self._initSelectYear_()


    '''
           功能：
               点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''
    def slotClickedInqury(self):
        self.getUserInfo()
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
        self.groupBox_2.setDisabled(False)
        self.groupBox_3.setDisabled(False)
        self.pb_save.setDisabled(True)
        #        self.tb_inqury.setDisabled(True)
        #        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_year.currentItem().text()
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
            item.setData(0,Qt.UserRole,QVariant(EquipInfo[0]))
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectSpecialEquipmentInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
        self.tw_second.expandAll()

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
            #item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
        self.tw_first.expandAll()

        # 查看当前被选中的单位和装备并初始化
    def slotInquryStrengthResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
                break
        self.currentCheckedEquipList = self.get_checked(self.tw_second.topLevelItem(0))
        self.tw_second.expandAll()
        if self.currentCheckedEquipList == [] or self.currentCheckedUnitList == []:
            self.tw_result.setRowCount(2)
            self.tw_result.horizontalHeader().setVisible(False)
            self.tw_result.verticalHeader().setVisible(False)
            return
        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
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

    '''
            功能：
                当选择年份时，设置当前可选项和不可选项,并初始化年份目录
    '''

    def _initStrenInquiry(self):
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(True)
        self.le_second.setDisabled(True)
        self.tw_first.setDisabled(True)
        self.tw_second.setDisabled(True)
        # self.tb_inqury.setDisabled(False)
        # self.tb_rechoose.setDisabled(False)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        self.yearList = []

        # 初始化年份选择列表
        self._initSelectYear_()
        # self.cb_yearAll = QCheckBox(self.sa_yearChoose)

    # 初始化年份listwidget
    def _initSelectYear_(self):
        self.currentYearListItem = {}
        self.yearList = []
        self.lw_year.clear()
        allyearList = selectAllOrderApplyYearInfo()

        for year in allyearList:
            self.yearList.append(year[0])

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_year.addItem(item)
            self.currentYearListItem[year] = item

    # 初始化单位目录
    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root)

            # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.first_treeWidget_dict[rowData[0]] = item
            self._initUnitTreeWidget(rowData[0], item)

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


    def _initTableWidgetByUnitListAndEquipList(self, currentCheckedUnitList, currentCheckedEquipList,currentYear):
        self.tw_result.itemChanged.disconnect(self.soltCheckData)
        self.checkBoxListItems = {}
        self.pb_save.setDisabled(True)
        currentClass = 0
        self.tw_result.clear()
        self.tw_result.setRowCount(0)
        self.unitList = currentCheckedUnitList
        self.equipList = currentCheckedEquipList
        self.year = currentYear
        self.resultList = []
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)
        self.currentInquiryResult.clear()

        self.tw_result.setColumnCount(9)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText("%s年%s专用装备订购申请表"%(self.year,selectUnitNameByUnitID(self.currentCheckedUnitList[0])))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 10)

        item = QTableWidgetItem()
        item.setText("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 0, item)


        item = QTableWidgetItem()
        item.setText("装备名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 1, item)

        item = QTableWidgetItem()
        item.setText("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)

        item = QTableWidgetItem('编制数')
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)

        item = QTableWidgetItem()
        item.setText("实力数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)


        item = QTableWidgetItem()
        item.setText("拟退役数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)


        item = QTableWidgetItem()
        item.setText("现有数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)


        item = QTableWidgetItem()
        item.setText("申请需求")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 7, item)


        item = QTableWidgetItem()
        item.setText("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 8, item)

        self.resultList = selectAboutOrderApplyByEquipAndUnit(currentCheckedUnitList, currentCheckedEquipList, currentYear)

        self.tw_result.setRowCount(len(self.resultList) + 2)
        classID = 1

        for i, LineInfo in enumerate(self.resultList):
            m_isSecond = isSecondDict(LineInfo[2])
            if m_isSecond:
                currentClass = currentClass + 1
                ID = chinese[currentClass]
                classID = 1
                LineInfo.append(False)
            else:
                if selectEquipIsHaveChild(LineInfo[2]):
                    ID = ""
                    LineInfo.append(False)
                else:
                    ID = str(classID)
                    classID = classID + 1
                    LineInfo.append(True)

            item = QTableWidgetItem(ID)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 0, item)
            # 名称
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 1, item)
            # 单位
            item = QTableWidgetItem(LineInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 2, item)

            # 编制数
            item = QTableWidgetItem(str(LineInfo[5]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 3, item)
            # 实力数
            item = QTableWidgetItem(str(LineInfo[6]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 4, item)

            # 现有数
            item = QTableWidgetItem(str(LineInfo[8]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 6, item)

            if len(str(LineInfo[7])) < 1:
                LineInfo[7] = 0
            if len(ID) == 0 or ID.isdigit() == False:
                #拟退役数
                item = QTableWidgetItem(str(LineInfo[7]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(i + 2, 5, item)
                #申请需求
                item = QTableWidgetItem(str(LineInfo[9]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(i + 2, 7, item)
                #备注
                item = QTableWidgetItem(LineInfo[10])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(i + 2, 8, item)
            else:
                checkBox = CheckableComboBox()
                checkBox.addItem(str(LineInfo[7]), LineInfo[7])
                from PyQt5.QtCore import QVariant
                v = QVariant(0)
                checkBox.setItemData(0, v, Qt.UserRole - 1)
                checkBox.setItemData(0, Qt.lightGray, Qt.BackgroundRole)
                # 拟退役数
                planToRetireItems = findPlanToRetireItem(LineInfo[1], LineInfo[2], LineInfo[12])
                if planToRetireItems != None:
                    for index,element in enumerate(planToRetireItems):
                            checkBox.addItem(element['ID'],element['num'] )
                            cell = checkBox.model().item(index + 1, 0)
                            cell.setCheckState(Qt.Unchecked)
                    checkBox.activated.connect(self.soltCheckData)
                self.tw_result.setCellWidget(i + 2, 5, checkBox)

                # 申请需求
                item = QTableWidgetItem(str(LineInfo[9]))
                # item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(i + 2, 7, item)
                # 备注
                item = QTableWidgetItem(LineInfo[10])
                # item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(i + 2, 8, item)
            self.currentInquiryResult[i] = LineInfo
        self.tw_result.itemChanged.connect(self.soltCheckData)

    def slotSaveRetire(self):
        item = self.tw_result.currentItem()
        reply = getMessageBox('修改', '是否保存修改？', True, True)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
            return
        for i, result in self.currentInquiryResult.items():
            if result[-1] == True:
                checkbox = self.tw_result.cellWidget(i + 2, 5)
                num = checkbox.itemText(0)
                apply = self.tw_result.item(i + 2, 7).text()
                other = self.tw_result.item(i + 2, 8).text()
                updateOrderApply(num, apply, other, result)
        getMessageBox('修改', '修改成功', True, False)
        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                   self.currentYear)
        return

    def soltCheckData(self,item):
        if item != None and type(item) != int:
            column = item.column()
            row = item.row()
            if  column == 7:
                self.pb_save.setDisabled(False)
                input = item.text()
                if input.isdigit() == True:
                    return
                else:
                    getMessageBox('警告', '请输入正确的数字！', True, False)
                    self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList,
                                                                self.currentCheckedEquipList,
                                                                self.currentYear)
        elif item != None and type(item) == int:
            column = self.tw_result.currentColumn()
            row = self.tw_result.currentRow()
            if column == 5:
                comboxCheck = self.tw_result.cellWidget(row,column)
                checkItems = comboxCheck.checkedItems()
                planToRetire = 0
                if len(checkItems) > 0:
                    for i,item in enumerate(checkItems):
                        data = comboxCheck.itemData(i + 1,Qt.UserRole)
                        planToRetire= int(data) + planToRetire
                    comboxCheck.setItemText(0,str(planToRetire))
                    comboxCheck.setCurrentIndex(0)
                else:
                    comboxCheck.setItemText(0, str(comboxCheck.itemData(0,Qt.UserRole)))
                    comboxCheck.setCurrentIndex(0)
                    return
        self.pb_save.setDisabled(False)

    def get_checked(self, node: QTreeWidgetItem) -> list:
        """ 得到当前节点选中的所有分支， 返回一个 list """
        temp_list = []
        # 此处看下方注释 1
        for item in node.takeChildren():
            # 判断是否选中
            if item.checkState(0) == Qt.Checked or item.checkState(0) == Qt.PartiallyChecked:
                temp_list.append(str(item.data(0,Qt.UserRole)))
                # 判断是否还有子分支
                if item.childCount():
                    temp_list.extend(self.get_checked(item))
            node.addChild(item)
        return temp_list

    #导出到Excel表格
    def slotOutputToExcel(self):
        if len(self.resultList) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('修改导出Excel', '是否保存修改并导出Excel？', True, True)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
            return
        for i, result in self.currentInquiryResult.items():
            if result[-1] == True:
                checkbox = self.tw_result.cellWidget(i + 2, 5)
                num = checkbox.itemText(0)
                apply = self.tw_result.item(i + 2, 7).text()
                other = self.tw_result.item(i + 2, 8).text()
                updateOrderApply(num, apply, other, result)
        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                    self.currentYear)
        currentClass = 0
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            import xlwt
            workBook = xlwt.Workbook(encoding='utf-8')
            workSheet = workBook.add_sheet('Sheet1')
            titileStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 2  # 设置为细实线
            borders.right = 2
            borders.top = 2
            borders.bottom = 2
            titileStyle.font = font  # 设定样式
            titileStyle.alignment = alignment
            titileStyle.borders = borders
            workSheet.col(0).width = 4000
            workSheet.col(1).width = 4000
            workSheet.col(2).width = 4000
            workSheet.col(3).width = 4000
            workSheet.col(4).width = 4000
            workSheet.col(5).width = 4000
            workSheet.col(6).width = 4000
            workSheet.col(7).width = 4000
            workSheet.col(8).width = 4000
            workSheet.col(9).width = 4000
            contentStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            contentStyle.font = font  # 设定样式
            contentStyle.alignment = alignment
            contentStyle.borders = borders


            workSheet.write_merge(0, 0, 0, 8, "%s年%s装备补充及退役需求表" % (self.year, selectUnitNameByUnitID(self.currentCheckedUnitList[0])), titileStyle)
            workSheet.write(1,0,"序号",titileStyle)
            workSheet.write(1, 1, "装备名称",titileStyle)
            workSheet.write(1, 2, "单位",titileStyle)
            workSheet.write(1, 3, "编制数",titileStyle)
            workSheet.write(1, 4, "实力数",titileStyle)
            workSheet.write(1, 5, "拟退役数",titileStyle)
            workSheet.write(1, 6, "现有数",titileStyle)
            workSheet.write(1, 7, "申请需求", titileStyle)
            workSheet.write(1, 8, "备注", titileStyle)

            for i, LineInfo in enumerate(self.resultList):
                m_isSecond = isSecondDict(LineInfo[2])
                if m_isSecond:
                    currentClass = currentClass + 1
                    ID = chinese[currentClass]
                    classID = 1
                    LineInfo.append(False)
                else:
                    if selectEquipIsHaveChild(LineInfo[2]):
                        ID = ""
                        LineInfo.append(False)
                    else:
                        ID = str(classID)
                        classID = classID + 1
                        LineInfo.append(True)

                workSheet.write(i + 2, 0,ID, contentStyle)
                # 名称
                workSheet.write(i + 2, 1, LineInfo[3], contentStyle)
                # 单位
                workSheet.write(i + 2, 2, LineInfo[4],contentStyle)
                # 编制数
                workSheet.write(i + 2, 3,str(LineInfo[5]), contentStyle)
                # 实力数
                workSheet.write(i + 2, 4, LineInfo[6], contentStyle)
                if len(str(LineInfo[7])) < 1:
                    LineInfo[7] = '0'
                # 拟退役数
                workSheet.write(i + 2, 5, LineInfo[7], contentStyle)
                #现有数
                workSheet.write(i + 2, 6, LineInfo[8], contentStyle)
                # 申请需求
                workSheet.write(i + 2, 7, LineInfo[9], contentStyle)
                # 备注
                workSheet.write(i + 2, 8, LineInfo[10], contentStyle)

            try:
                pathName = "%s/%s年%s专用装备订购申请表.xls" % (directoryPath,self.year, selectUnitNameByUnitID(self.currentCheckedUnitList[0]))
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                getMessageBox("导出成功", "导出成功！", True, False)
                return
            except Exception as e:
                getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                return
        else:
            getMessageBox("选取文件夹失败！", "请选择正确的文件夹！", True, False)



chinese = ['', '(一)', '(二)', '(三)', '(四)', '(五)','(六)','(七)', '']