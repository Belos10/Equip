from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from database.OrderManageSql import *
from sysManage.orderManage.OrderAdjustCont import OrderAdjustCont
from sysManage.userInfo import get_value
from widgets.orderManage.Widget_AdjustOrder import widget_adjustOrder
from sysManage.component import getMessageBox, getIntInputDialog


class AdjustOrder(QWidget, widget_adjustOrder):
    def __init__(self,parent=None):
        super(AdjustOrder, self).__init__(parent)
        self.setupUi(self)
        self.initAll()
        self.contEdit = OrderAdjustCont()
        self.fileName = ""
        self.signalConnect()



    def initAll(self):
        self.tw_equip.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.tw_equip.setDisabled(1)
        self.tw_equip.clear()
        self.txt_adjustOrderYear.clear()
        self.adjustForm.clear()
        self.adjustForm.setRowCount(0)
        self.adjustForm.setColumnCount(0)
        self._initYearWidget_()



    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.connect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.connect(self.setAdjustOrderTitle)
        # 点击第一目录结果
        self.tw_equip.itemClicked.connect(self.slotAdjustStrengthResult)
        self.tw_equip.itemChanged.connect(self.slotCheckedChange)
        # 修改数据
        self.pb_Save.clicked.connect(self.saveData)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)
        self.tb_add.clicked.connect(self.slotAddNewYear)
        self.tb_del.clicked.connect(self.slotDelYear)
        self.pb_firstSelect.clicked.connect(self.slotSelectEquip)




    def slotSelectEquip(self):
        findText = self.le_first.text()
        for i, item in self.equip_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_equip.setCurrentItem(item)
                break
    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass


    # 新增年份
    def slotAddNewYear(self):
        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)
        if ok:
            haveYear = False
            allyear = selectYearListAboutOrderAdjust()
            for yearInfo in allyear:
                if str(year) == yearInfo:
                    haveYear = True
            if haveYear == True:
                getMessageBox('添加', '添加失败，该年份已存在', True, False)
                return
            insertIntoOrderAdjustYear(year)
            self._initYearWidget_()
            return


    # 删除年份
    def slotDelYear(self):
        reply = getMessageBox("删除", "是否删除所有？", True, True)
        if reply == QMessageBox.Ok:
            currentYear = self.lw_yearChoose.currentItem()
            deleteOrderAdjustYear(currentYear.text())
            deleteByYear(currentYear.text())
            self._initYearWidget_()


    # 初始化年份
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutOrderAdjust()
        for year in allYear:
            self.yearList.append(year)
        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)


    def slotClickedInqury(self):
        self.tw_equip.clear()
        self.tw_equip.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.tw_equip.setDisabled(False)
        # self.first_treeWile_firstdget_dict = {}
        self.equip_treeWidget_dict = {}
        self.initUserInfo()
        self.currentYear = self.lw_yearChoose.currentItem().text()
        self.oneYear = int(self.currentYear) + 1
        self.twoYear = int(self.currentYear) + 2
        # self._initUnitTreeWidget("", self.tw_equip)
        # startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        # stack = []
        # root = []
        # if startInfo:
        #     stack.append(startInfo)
        #     root.append(self.tw_equip)
        #     self._initUnitTreeWidget(stack, root)

        equipInfo = findUperEquipIDByName("专用装备")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_equip)
            self._initEquipTreeWidget(stack, root, 0)


    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    # def _initUnitTreeWidget(self, stack,root):
    #     while stack:
    #         UnitInfo = stack.pop(0)
    #         item = QTreeWidgetItem(root.pop(0))
    #         item.setText(0, UnitInfo[1])
    #         # item.setCheckState(0, Qt.Unchecked)
    #         self.first_treeWidget_dict[UnitInfo[0]] = item
    #         result = selectDisturbPlanUnitInfoByDeptUper(UnitInfo[0])
    #         for resultInfo in result:
    #             stack.append(resultInfo)
    #             root.append(item)

    def _initEquipTreeWidget(self, stack, root, count):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            item.setCheckState(0, Qt.Unchecked)
            self.equip_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
                self._initEquipTreeWidget(stack, root, count + 1)

    def addTab(self, result):
        count = selectLevelForEquip(result[0][0])
        Name = count * '    ' + result[0][1]
        result1 = []
        for i,value in enumerate(result[0]):
            if i != 1:
                result1.append(result[0][i])
            else:
                result1.append(Name)
        result[0] = tuple(result1)
        return result



    '''
        查询结果
    '''
    def slotAdjustStrengthResult(self):
        self.yearList = []
        self.originalEquipDict = {}
        self.originalEquipDictTab = {}
        self.currentUnitChilddict = {}
        self.unitFlag = 0
        self.adjustForm.clear()
        # 获取当前装备名
        j = 0
        for equipID, equipItem in self.equip_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.originalEquipDictTab[j] = equipInfo[0]
                j = j + 1
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.originalEquipDictTab[j] = equipInfo[0]
                j = j + 1
        print("self.originalEquipDict",self.originalEquipDict)
        self._initOrderAdjustByUnitListAndEquipList(self.originalEquipDict, self.originalEquipDictTab)


    '''
        初始化分配计划结果
    '''
    def _initOrderAdjustByUnitListAndEquipList(self, equipDict, equipDictTab={}):
        self.adjustForm.clear()
        self.adjustForm.setRowCount(0)
        self.currentEquipdict = equipDict
        self.lenCurrentEquipdict = len(self.currentEquipdict)
        self.adjustForm.setColumnCount(19)
        self.adjustForm.setRowCount(self.lenCurrentEquipdict+2)

        item = QTableWidgetItem()
        item.setText('名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setText('单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setText('单价(万元)')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 2, item)
        item = QTableWidgetItem()
        item.setText(str(self.oneYear)+'年调整计划')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 3, item)
        item = QTableWidgetItem()
        item.setText(str(self.twoYear) + '年计划')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 7, item)
        item = QTableWidgetItem()
        item.setText('申报单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 11, item)
        item = QTableWidgetItem()
        item.setText('承制部门')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 12, item)
        item = QTableWidgetItem()
        item.setText('采购方式')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 13, item)
        item = QTableWidgetItem()
        item.setText('生产厂家')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 14, item)
        item = QTableWidgetItem()
        item.setText('调整要素')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 15, item)
        item = QTableWidgetItem()
        item.setText('拟分配单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 16, item)
        item = QTableWidgetItem()
        item.setText('备注')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 17, item)
        item = QTableWidgetItem()
        item.setText('合同来源')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(0, 18, item)

        item = QTableWidgetItem()
        item.setText('上一年结转数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 3, item)
        item = QTableWidgetItem()
        item.setText('今年应交数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 4, item)
        item = QTableWidgetItem()
        item.setText('今年实交付数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 5, item)
        item = QTableWidgetItem()
        item.setText('金额(万元)')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 6, item)
        item = QTableWidgetItem()
        item.setText('上一年结转数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 7, item)
        item = QTableWidgetItem()
        item.setText('今年应交数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 8, item)
        item = QTableWidgetItem()
        item.setText('今年实交付数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 9, item)
        item = QTableWidgetItem()
        item.setText('金额(万元)')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.adjustForm.setItem(1, 10, item)

        self.adjustForm.setSpan(0, 0, 2, 1)
        self.adjustForm.setSpan(0, 1, 2, 1)
        self.adjustForm.setSpan(0, 2, 2, 1)
        self.adjustForm.setSpan(0, 3, 1, 4)
        self.adjustForm.setSpan(0, 7, 1, 4)
        self.adjustForm.setSpan(0, 11, 2, 1)
        self.adjustForm.setSpan(0, 12, 2, 1)
        self.adjustForm.setSpan(0, 13, 2, 1)
        self.adjustForm.setSpan(0, 14, 2, 1)
        self.adjustForm.setSpan(0, 15, 2, 1)
        self.adjustForm.setSpan(0, 16, 2, 1)
        self.adjustForm.setSpan(0, 17, 2, 1)
        self.adjustForm.setSpan(0, 18, 2, 1)
        self.adjustForm.horizontalHeader().setHidden(1)
        self.adjustForm.verticalHeader().setHidden(1)
        i = 2
        for LineInfo in equipDictTab.values():
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.adjustForm.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[5])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.adjustForm.setItem(i, 1, item)
            # (i, 2-18)
            for j in range(2,18):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.adjustForm.setItem(i, j, item)
            i = i + 1
        if self.currentEquipdict:
            self.initAdjustOrderData()
            self.initcbschedule()
            self.ifEquipHaveChild()

    # 初始化表格
    def initAdjustOrderData(self):
        adjustOrderData = selectOrderAdjustDataByList(self.currentEquipdict,self.currentYear)
        for i,adjustOrderDataInfo in enumerate(adjustOrderData):
            for j in range(2,18):
                item = self.adjustForm.item(i + 2, j)
                item.setText(adjustOrderDataInfo[j + 2])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable|Qt.ItemIsEditable)

    # 初始化合同来源
    def initcbschedule(self):
        for i,equipInfo in self.currentEquipdict.items():
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                if ifHaveContSource(equipInfo[0],self.currentYear):
                    adjustContData = selectOneOrderAdjustContData(equipInfo[0],self.currentYear)
                    item = QPushButton(adjustContData[3])
                    self.adjustForm.setCellWidget(i + 2, 18, item)
                    item.clicked.connect(self.setAdjustCont)
                else:
                    item = QComboBox()
                    item.addItem("选择合同来源",0)
                    item.addItem("单一来源", 1)
                    item.addItem("招标", 2)
                    self.adjustForm.setCellWidget(i + 2, 18, item)
            else:
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.adjustForm.setItem(i + 2, 18, item)

    # 保存数据
    def saveData(self):
        if self.adjustForm.rowCount()<2:
            return
        flag =False
        for i,equipInfo in self.currentEquipdict.items():
            # 保存合同来源
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                if not ifHaveContSource(equipInfo[0], self.currentYear):
                    item = self.adjustForm.cellWidget(i + 2, 18)
                    if item.currentIndex() == 0:
                        flag =True
                    else:
                        txt = item.currentText()
                        updateContSource(txt,equipInfo[0],self.currentYear)
            # 保存调整计划表
            data=[]
            for j in range(2, 18):
                txt = self.adjustForm.item(i+2,j).text()
                data.append(txt)
            updateOrderAdjustData(equipInfo[0],data,self.currentYear)
        if flag:
            getMessageBox("提示","有装备未选择合同来源", True, False)
        if self.currentEquipdict:
            self.initAdjustOrderData()
            self.initcbschedule()
            self.ifEquipHaveChild()


    def setAdjustCont(self):
        row = self.adjustForm.currentRow()
        equip_ID = self.currentEquipdict[row-2][0]
        self.contEdit._initSelf_()
        self.contEdit.setYearandEquipID(self.currentYear,equip_ID)
        self.contEdit.setWindowTitle("装备订购")
        self.contEdit.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.contEdit.show()


    # 若装备含子装备，则该行不可选中
    def ifEquipHaveChild(self):
        for i in self.currentEquipdict:
            if selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(1, self.adjustForm.columnCount()-1):
                    item = self.adjustForm.item(i + 2, j)
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

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


    # 初始化分配计划年份
    def setAdjustOrderTitle(self):
        txt="火箭军正常装备订购" + str(self.currentYear) + "年调整和" + str(self.oneYear) + "年计划预算"
        self.txt_adjustOrderYear.setFont(QFont("Microsoft YaHei"))
        self.txt_adjustOrderYear.setAlignment(Qt.AlignCenter)
        self.txt_adjustOrderYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_adjustOrderYear.setFontPointSize(15)
        self.txt_adjustOrderYear.setText(txt)


    '''
        功能
            导出数据到Excel
    '''
    def slotOutputToExcel(self):
        self.adjustOrderList = {}
        if self.adjustForm.rowCount() <= 0:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('导出Excel', '是否保存修改并导出Excel？', True, True)
        if reply == QMessageBox.Cancel:
            self._initOrderAdjustByUnitListAndEquipList(self.originalEquipDict, self.originalEquipDictTab)
            return

        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0 and '.' not in directoryPath:
            import xlwt
            workBook = xlwt.Workbook(encoding='utf-8')
            workSheet = workBook.add_sheet('Sheet1')

            headTitleStyle2 = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            headTitleStyle2.font = font  # 设定样式
            headTitleStyle2.alignment = alignment
            headTitleStyle2.borders = borders

            headTitleStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 20  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 3  # 设置为细实线
            borders.right = 3
            borders.top = 3
            borders.bottom = 3
            headTitleStyle.font = font  # 设定样式
            headTitleStyle.alignment = alignment
            headTitleStyle.borders = borders

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

            #画表头
            for i in range(19):
                workSheet.col(i).width = 5500
            workSheet.write_merge(0, 1, 0, 0, "名称", titileStyle)
            workSheet.write_merge(0, 1, 1, 1, "单位", titileStyle)
            workSheet.write_merge(0, 0, 2, 2, "单价(万元)", titileStyle)
            workSheet.write_merge(0, 0, 3, 6, "%s年调整计划" % self.oneYear, titileStyle)
            workSheet.write_merge(0, 0, 7, 10, "%s年计划" % self.twoYear, titileStyle)
            workSheet.write_merge(0, 1, 11, 11, "申报单位", titileStyle)
            workSheet.write_merge(0, 1, 12, 12, "承制部门", titileStyle)
            workSheet.write_merge(0, 1, 13, 13, "采购方式", titileStyle)
            workSheet.write_merge(0, 1, 14, 14, "生产厂家", titileStyle)
            workSheet.write_merge(0, 1, 15, 15, "调整要素", titileStyle)
            workSheet.write_merge(0, 1, 16, 16, "拟分配单位", titileStyle)
            workSheet.write_merge(0, 1, 17, 17, "备注", titileStyle)
            workSheet.write_merge(0, 1, 18, 18, "合同来源", titileStyle)
            workSheet.write(1, 3, "上一年结转数量", titileStyle)
            workSheet.write(1, 4, "今年应交数量", titileStyle)
            workSheet.write(1, 5, "今年实交付数量", titileStyle)
            workSheet.write(1, 6, "金额(万元)", titileStyle)
            workSheet.write(1, 7, "上一年结转数量", titileStyle)
            workSheet.write(1, 8, "今年应交数量", titileStyle)
            workSheet.write(1, 9, "今年实交付数量", titileStyle)
            workSheet.write(1, 10, "金额(万元)", titileStyle)

            #填表数据
            for i,equipInfo in self.currentEquipdict.items():
                columnList = []
                for j in range(18):
                    columnList.append(self.adjustForm.item(i + 2, j).text())
                if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                    if not ifHaveContSource(equipInfo[0], self.currentYear):
                        columnList.append(self.adjustForm.cellWidget(i + 2, 18).currentText())
                    else:
                        columnList.append(self.adjustForm.cellWidget(i + 2, 18).text())
                else:
                    columnList.append(self.adjustForm.item(i + 2, 18).text())
                self.adjustOrderList[i] = columnList

            for key in self.adjustOrderList.keys():
                for index in range(19):
                    rowData = self.adjustOrderList.get(key)
                    workSheet.write(2 + key, index, rowData[index], contentStyle)

            try:
                pathName = "%s/火箭军正常装备订购%s年调整和%s年计划预算.xls" % (directoryPath, str(self.currentYear), str(self.oneYear))
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

