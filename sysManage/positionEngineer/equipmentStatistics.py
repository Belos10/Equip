from PyQt5.QtCore import Qt, QVariant

from database.SD_EquipmentBanlanceSql import getFomatEquipmentName
from database.danderGoodsSql import getBrigadesByBaseId, getpositionsByPositionId, getUnit
from database.positionEngneerSql import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog
from widgets.positionEngineer.posEngneerStatisticsUI import PosEngneerStatisticsUI
from sysManage.userInfo import get_value


class EquipmentStatistics(QWidget, PosEngneerStatisticsUI):
    def __init__(self, parent=None):
        super(EquipmentStatistics, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self.countOfPosition = 0
        self.rowAndCountIndex = {}
        self.startInfo = None
        self.userInfo = None
        self.info = {}
        self.initEquipmentStatistics()
        self.signalConnectSlot()


    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        self.tw_first.clicked.connect(self.slotEquipmentStatisticsResult)
        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotEquipmentStatisticsResult)
        # #新增某个年份
        # self.tb_delete.clicked.connect(self.slotDelete)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        # self.tb_output.clicked.connect(self.slotInput)
        self.tb_input.setDisabled(True)
        self.tb_input.setVisible(False)
        self.tb_output.setDisabled(True)
        self.tb_output.setVisible(False)
        # self.tb_output.clicked.connect(self.slotOutput)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)

    # 信号和槽断开
    def slotDisconnect(self):
        pass

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
    # 定义初始化函数
    def initEquipmentStatistics(self):
        self.initUserInfo()
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_first.setVisible(True)
        self.pb_firstSelect.setVisible(False)
        self.pb_firstSelect.setDisabled(False)
        self.le_first.setVisible(False)
        self.le_second.setVisible(False)
        self.pb_outputToExcel.setDisabled(True)
    



        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        if self.userInfo:
            from database.strengthDisturbSql import selectUnitInfoByUnitID
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])

        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        equipInfo = None
        equipInfo = selectEquipInfoByEquipUper("")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root)

        pass

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

    '''
        功能：
            点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''

    def slotClickedInqury(self):
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


        self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        item = QTreeWidgetItem(self.tw_first)
        item.setText(0, self.startName)
        item.setCheckState(0, Qt.Unchecked)
        self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget(self.userInfo[0][4], item)
        self._initEquipTreeWidget("", self.tw_second)

    # def slotSelectUnit(self):
    #     findText = self.le_first.text()
    #     for i, item in self.first_treeWidget_dict.items():
    #         if item.text(0) == findText:
    #             self.tw_first.setCurrentItem(item)
    #             break
    #
    # def slotSelectEquip(self):
    #     findText = self.le_second.text()
    #     for i, item in self.second_treeWidget_dict.items():
    #         if item.text(0) == findText:
    #             self.tw_second.setCurrentItem(item)
    #             break

    '''
        功能：
            查询实力结果
    '''

    def slotEquipmentStatisticsResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        # for equipID, equipItem in self.second_treeWidget_dict.items():
        #     if equipItem.checkState(0) == Qt.Checked:
        #         self.currentCheckedEquipList.append(equipID)
        iterator = QTreeWidgetItemIterator(self.tw_second)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked or item.checkState(0) == Qt.PartiallyChecked:
                self.currentCheckedEquipList.append(str(item.data(0, Qt.UserRole)))
            # columnCount = item.columnCount()
            # for i in range(columnCount):
            #     text = item.text(i)
            #     if i == columnCount - 1:
            #         print(text)
            #         # self.currentCheckedUnitList.append(text)
            #     else:
            #         print(text, end=' ')
            iterator.__iadd__(1)
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
        print("self.currentCheckedUnitList ", self.currentCheckedUnitList)
        if len(self.currentCheckedUnitList) == 1 and len(self.currentCheckedEquipList) > 0:
            if gradeInUnit(self.currentCheckedUnitList[0]) == 3:
                self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList)
            else:
                self.tw_result.setRowCount(0)
                self.tw_result.setColumnCount(0)



    '''
        功能：
            根据单位目录和装备目录初始化结果表格
    '''

    def _initTableWidgetByUnitListAndEquipList(self, unitList, equipList):
        self.pb_outputToExcel.setDisabled(False)
        try:
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        except:
            pass
        self.info = {}
        self.brigades = []
        self.brigade = {}
        self.positions = []
        self.position = {}
        self.positionCount = 0
        self.base = {}
        self.tw_result.clear()
        self.base['Unit_ID'] =  unitList[0]
        self.base['Unit_Name'] = getUnit(self.base['Unit_ID'])['Unit_Name']
        self.brigadeIds = getBrigadesByBaseId(self.base['Unit_ID'])
        # if len(self.brigadeIds) < 1:
        #     return
        for item in self.brigadeIds:
            self.brigade['Unit_ID'] = item['Unit_ID']
            self.brigade['Unit_Name'] = item['Unit_Name']
            positionIds = getpositionsByPositionId(self.brigade['Unit_ID'])
            self.positions = []
            for element in positionIds:
                self.position['Unit_ID'] = element['Unit_ID']
                self.position['Unit_Name'] = element['Unit_Name']
                self.positionCount = self.positionCount + 1
                self.positions.append(self.position.copy())
            self.brigade['Positions'] = self.positions.copy()
            self.brigades.append(self.brigade.copy())
        self.base['brigades'] = self.brigades

        # 画表头
        self.rowCount = len(equipList) + 4
        self.columnCount = 4 + 2 * self.positionCount
        self.tw_result.setRowCount(self.rowCount)
        self.tw_result.setColumnCount(self.columnCount)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()
        item = QTableWidgetItem("%s阵地工程X生化防护装备统计表" % self.base['Unit_Name'])
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, self.columnCount)
        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        self.tw_result.setSpan(1, 0, 3, 1)
        item = QTableWidgetItem("名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        self.tw_result.setSpan(1, 1, 3, 1)
        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 2, item)
        self.tw_result.setSpan(1, 2, 3, 1)
        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 3, 1)

        for i in range(len(equipList)):
            item = QTableWidgetItem(str(i + 1))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 0, item)

            item = QTableWidgetItem("%s"%getFomatEquipmentName(equipList[i]))
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 1, item)

            item = QTableWidgetItem("%s" % getEquipmentTypeById(equipList[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 2, item)

            if self.columnCount > 4:
                brigadeStartColumn = 4
                positionStartColum = 4
                currentRow = 4 + i
                currentColumn = 4
                for aBrigade in self.base['brigades']:
                    item = QTableWidgetItem("%s"%aBrigade['Unit_Name'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, brigadeStartColumn, item)
                    self.tw_result.setSpan(1, brigadeStartColumn, 1, 2 * len(aBrigade['Positions']))
                    for aPosition in aBrigade['Positions']:
                        item = QTableWidgetItem("%s" % aPosition['Unit_Name'])
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tw_result.setItem(2, positionStartColum, item)
                        self.tw_result.setSpan(2, positionStartColum, 1, 2 )

                        item = QTableWidgetItem("数量")
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        item.setFlags(Qt.ItemIsEnabled)
                        self.tw_result.setItem(3, positionStartColum, item)

                        item = QTableWidgetItem("运行状态")
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        item.setFlags(Qt.ItemIsEnabled)
                        self.tw_result.setItem(3, positionStartColum + 1, item)
                       # info['%d,%d'%(currentRow,currentColumn)] = aPosition['Unit_ID']
                        data = getStatictsResult(aPosition['Unit_ID'],equipList[i])
                        if len(data) > 0:
                            item = QTableWidgetItem("%d"%data[3])
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            self.tw_result.setItem(currentRow, positionStartColum, item)

                            item = QTableWidgetItem("%s" % data[4])
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            self.tw_result.setItem(currentRow, positionStartColum + 1, item)
                            self.info['%d,%d' % (currentRow, currentColumn)] = data[0]
                            self.info['%d,%d' % (currentRow, currentColumn + 1)] = data[0]
                        else:
                            self.info['%d,%d' % (currentRow, currentColumn)] = [equipList[i],aPosition['Unit_ID']]
                            self.info['%d,%d' % (currentRow, currentColumn + 1)] = [equipList[i],aPosition['Unit_ID']]
                        positionStartColum = positionStartColum + 2
                        currentColumn = positionStartColum
                    brigadeStartColumn = positionStartColum



        #设置前三行为不可编辑
        for i in range(3):
            for j in range(self.columnCount):
                item = self.tw_result.item(i,j)
                if item != None:
                    item.setFlags(Qt.ItemIsEnabled)
        rowCount = 0
        for i in range(len(equipList) - 1, -1, -1):
            columnCount = 0
            if isLastLevelEquipment(equipList[i]) == True:
                for j in range(4,self.tw_result.columnCount()):
                    if j % 2 == 0:
                        itemData = self.tw_result.item(4 + i, j)
                        if itemData != None:
                            text1 = itemData.text()
                        else:
                            text1 = ''
                        if len(text1) > 0:
                            columnCount = columnCount + int(text1)
                item = QTableWidgetItem(str(columnCount))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(4 + i, 3,item)
                rowCount = rowCount + columnCount
            else:
                item = QTableWidgetItem(str(rowCount))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(4 + i, 3, item)
                for j in range(4, self.tw_result.columnCount()):
                    item = QTableWidgetItem('')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.tw_result.setItem(4 + i, j, item)

        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

    '''
                功能：
                    单位目录的初始化，显示整个单位表
                    参数表：root为上级单位名字，mother为上级节点对象
    '''

    def _initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
            # item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
        self.tw_first.expandAll()
    '''
        功能：
            初始化装备目录
    '''

    def _initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            item.setData(0,Qt.UserRole,QVariant(EquipInfo[0]))
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
        self.tw_second.expandAll()


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
        self.tw_second.expandAll()

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()
        if currentRow > 3 and currentColumn > 3:
            index = self.info.get('%s,%s'%(currentRow,currentColumn))
            print(index)
            if type(index) == int:
                if currentColumn % 2 == 0:
                    itemData = self.tw_result.item(currentRow,currentColumn)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn + 1)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0:
                        try:
                            count = int(text1)
                        except:
                            QMessageBox.warning(self, "注意", "请输入正确的数字！", QMessageBox.Yes)
                            return
                        status = text2
                        if alterData(index,count,status) == True:
                            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
                            self.slotEquipmentStatisticsResult()
                    elif len(text1) == 0 and len(text2) == 0:
                       if deleteData(index) == True:
                           QMessageBox.warning(self, "注意", "清除成功！", QMessageBox.Yes, QMessageBox.Yes)
                           self.slotEquipmentStatisticsResult()
                else:
                    itemData = self.tw_result.item(currentRow, currentColumn - 1)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 :

                        try:
                            count = int(text1)
                        except:
                            QMessageBox.warning(self, "注意", "请输入正确的数字！", QMessageBox.Yes)
                            return
                        status = text2
                        if alterData(index,count,status) == True:
                            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
                            self.slotEquipmentStatisticsResult()
                    elif len(text1) == 0 and len(text2) == 0:
                       if deleteData(index) == True:
                           QMessageBox.warning(self, "注意", "清除成功！", QMessageBox.Yes, QMessageBox.Yes)
                           self.slotEquipmentStatisticsResult()
            elif type(index) == list:
                if currentColumn % 2 == 0:
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn + 1)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 :
                        try:
                            count = int(text1)
                        except:
                            QMessageBox.warning(self, "注意", "请输入正确的数字！", QMessageBox.Yes)
                            return
                        status = text2
                        if insertData(index[0],index[1],count,status) == True:
                            QMessageBox.warning(self, "注意", "增加成功！", QMessageBox.Yes, QMessageBox.Yes)
                            self.slotEquipmentStatisticsResult()
                else:
                    itemData = self.tw_result.item(currentRow, currentColumn - 1)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 :
                        try:
                            count = int(text1)
                        except:
                            QMessageBox.warning(self, "注意", "请输入正确的数字！", QMessageBox.Yes)
                            return
                        status = text2
                        if insertData(index[0], index[1], count, status) == True:
                            QMessageBox.warning(self, "注意", "增加成功！", QMessageBox.Yes, QMessageBox.Yes)
                            self.slotEquipmentStatisticsResult()




    def slotInput(self):
        pass

    def slotOutput(self):
        pass

    def slotOutputToExcel(self):
        if len(self.currentCheckedUnitList) == 1 and len(self.currentCheckedEquipList) > 0:
            if gradeInUnit(self.currentCheckedUnitList[0]) != 3:
                reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
                return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            return

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


            # 画表头
            self.rowCount = len(self.currentCheckedEquipList) + 4
            self.columnCount = 4 + 2 * self.positionCount
            for i in range(self.columnCount):
                workSheet.col(i).width = 4000

            # self.tw_result.setSpan(0, 0, 1, self.columnCount)
            workSheet.write_merge(0, 0, 0, self.columnCount -1, "%s阵地工程X生化防护装备统计表" % self.base['Unit_Name'], titileStyle)


            # self.tw_result.setSpan(1, 0, 3, 1)
            workSheet.write_merge(1, 3, 0, 0, '序号',titileStyle)
            # self.tw_result.setSpan(1, 1, 3, 1)
            workSheet.write_merge(1, 3, 1, 1, '名称', titileStyle)
            # self.tw_result.setSpan(1, 2, 3, 1)
            workSheet.write_merge(1, 3, 2, 2, '单位', titileStyle)

            workSheet.write_merge(1, 3, 3, 3, '合计', titileStyle)

            for i in range(len(self.currentCheckedEquipList)):
                # self.tw_result.setItem(4 + i, 0, item)
                workSheet.write(4 + i, 0, str(i + 1),contentStyle)

                # self.tw_result.setItem(4 + i, 1, item)
                workSheet.write(4 + i, 1, "%s" % getFomatEquipmentName(self.currentCheckedEquipList[i]), contentStyle)
                # self.tw_result.setItem(4 + i, 2, item)
                workSheet.write(4 + i, 2, "%s" % getEquipmentTypeById(self.currentCheckedEquipList[i]), contentStyle)

                if self.columnCount > 4:
                    brigadeStartColumn = 4
                    positionStartColum = 4
                    currentRow = 4 + i
                    currentColumn = 4
                    for aBrigade in self.base['brigades']:
                        # self.tw_result.setSpan(1, brigadeStartColumn, 1, 2 * len(aBrigade['Positions']))
                        try:
                            workSheet.write_merge(1, 1, brigadeStartColumn, brigadeStartColumn + 2 * len(aBrigade['Positions']) -1, '单位', titileStyle)
                        except:
                            pass
                        for aPosition in aBrigade['Positions']:
                            # self.tw_result.setSpan(2, positionStartColum, 1, 2)
                            try:
                                workSheet.write_merge(2, 2, positionStartColum,positionStartColum + 1, "%s" % aPosition['Unit_Name'],titileStyle)
                            except:
                                pass
                            # self.tw_result.setItem(3, positionStartColum, item)
                            try:
                                workSheet.write(3, positionStartColum, '数量',titileStyle)
                            except:
                                pass
                            # self.tw_result.setItem(3, positionStartColum + 1, item)
                            try:
                                workSheet.write(3, positionStartColum + 1, '运行状态', titileStyle)
                            except:
                                pass


                            data = getStatictsResult(aPosition['Unit_ID'], self.currentCheckedEquipList[i])
                            if len(data) > 0:
                                # self.tw_result.setItem(currentRow, positionStartColum, item)
                                workSheet.write(currentRow, positionStartColum, "%d" % data[3], contentStyle)
                                workSheet.write(currentRow, positionStartColum + 1, "%s" % data[4], contentStyle)
                            else:
                                pass

                            positionStartColum = positionStartColum + 2
                            currentColumn = positionStartColum
                        brigadeStartColumn = positionStartColum


            rowCount = 0
            for i in range(len(self.currentCheckedEquipList) - 1, -1, -1):
                columnCount = 0
                if isLastLevelEquipment(self.currentCheckedEquipList[i]) == True:
                    for j in range(4, self.tw_result.columnCount()):
                        if j % 2 == 0:
                            itemData = self.tw_result.item(4 + i, j)
                            if itemData != None:
                                text1 = itemData.text()
                            else:
                                text1 = ''
                            if len(text1) > 0:
                                columnCount = columnCount + int(text1)
                    # self.tw_result.setItem(4 + i, 3, item)
                    workSheet.write(4 + i, 3, str(columnCount), contentStyle)
                    rowCount = rowCount + columnCount
                else:
                    # self.tw_result.setItem(4 + i, 3, item)
                    workSheet.write(4 + i, 3, str(rowCount), contentStyle)
                    for j in range(4, self.tw_result.columnCount()):
                        workSheet.write(4 + i, j, '', contentStyle)

            try:
                pathName = "%s/%s阵地工程X生化防护装备统计表.xls" % (directoryPath, self.base['Unit_Name'])
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return
        else:
            QMessageBox.about(self, "选取文件夹失败！", "请选择正确的文件夹！")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EquipmentStatistics()
    widget.show()
    sys.exit(app.exec_())
