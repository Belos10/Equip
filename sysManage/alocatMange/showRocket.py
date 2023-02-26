from widgets.alocatMange.showRocketTransfer import widget_showRocket
from PyQt5.QtWidgets import QDialog, QTableWidgetItem



class showRocket(QDialog, widget_showRocket):
    def __init__(self, parent=None):
        super(showRocket, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("火箭军调拨单")



    def initTableWidget(self, unitInfoList, equipInfo, year, requireInfo):
        self.requireInfo = requireInfo
        self.year = year
        self.unitNum = len(unitInfoList)
        self.unitInfoList = unitInfoList
        self.equipInfo = equipInfo
        self.crtColumnCount = len(unitInfoList) + 6
        if self.crtColumnCount < self.minSize:
            self.crtColumnCount = self.minSize
            self.isMin = True
        else:
            self.isMin = False
        self.tw_ditalModel.setColumnCount(self.crtColumnCount)
        self.crtRowCount = 26
        self.tw_ditalModel.setRowCount(self.crtRowCount)
        title = QTableWidgetItem()
        title.setText(self.title)
        title.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(0, 0, title)
        self.tw_ditalModel.setSpan(0, 0, 3, self.crtColumnCount)

        self.initNinethRow('调拨单号:', '调拨日期:', 3)
        self.initNinethRow('调拨依据:', '调拨性质:', 4)
        self.tw_ditalModel.item(4, 1).setText(requireInfo[-2] + " " + requireInfo[-1] + "; 火装计+军装计+陆装拨")
        self.initNinethRow('交装单位:', '单位地址:', 5)
        self.initNinethRow('联系人:', '联系方式:', 6)
        self.initNinethRow('军代表:', '联系方式:', 7)
        self.initNinethRow('接装单位:', '', 8)
        self.tw_ditalModel.item(8, 1).setText("火箭军参谋部核安全局")
        self.initNinethRow('单位地址:', '', 9)
        self.tw_ditalModel.item(9, 1).setText("北京市海淀区小营西路31号院")
        self.initNinethRow('联系人:', '联系方式:', 10)
        self.tw_ditalModel.item(10, 1).setText("陈燕栋")
        half = int((self.crtColumnCount - 2) / 2)
        self.initNinethRow('调拨方式:', '运输方式:', 11)
        self.tw_ditalModel.item(6, 1).setText(str(self.factoryInfoList[0][3]))
        self.tw_ditalModel.item(6, half+2).setText(str(self.factoryInfoList[0][4]))
        self.tw_ditalModel.item(7, 1).setText(str(self.factoryInfoList[0][5]))
        self.tw_ditalModel.item(7, half+2).setText(str(self.factoryInfoList[0][6]))
        self.tw_ditalModel.item(10, half + 2).setText("15311997201")

        item = QTableWidgetItem()
        item.setText("1")
        self.tw_ditalModel.setItem(15, 0, item)

        item = QTableWidgetItem()
        item.setText(equipInfo[1])
        self.tw_ditalModel.setItem(15, 1, item)

        item = QTableWidgetItem()
        item.setText(equipInfo[5])
        self.tw_ditalModel.setItem(15, 2, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[0])
        self.tw_ditalModel.setItem(15, 3, item)

        item = QTableWidgetItem()

        item.setText(requireInfo[1])
        self.tw_ditalModel.setItem(15, 4, item)

        for i, unitInfo in enumerate(unitInfoList):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setText(unitInfo[3])
            self.tw_ditalModel.setItem(14, 5 + i, item)

        item = QTableWidgetItem()
        item.setText("编号")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, 0, item)

        item = QTableWidgetItem()
        item.setText("装备名称")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, 1, item)

        item = QTableWidgetItem()
        item.setText("计量单位")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, 2, item)

        item = QTableWidgetItem()
        item.setText("质量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, 3, item)

        item = QTableWidgetItem()
        item.setText("总数")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, 4, item)

        # for i in range(5, self.crtColumnCount - 1):
        #     item = QTableWidgetItem()
        #     item.setText("")
        #     item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        #     self.tw_ditalModel.setItem(14, i, item)

        item = QTableWidgetItem()
        item.setText("备注")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, self.crtColumnCount - 1, item)

        for i, num in enumerate(requireInfo[2:-2]):
            item = QTableWidgetItem()
            item.setText(num)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(15, i + 5, item)

        item = QTableWidgetItem()
        item.setText("备注")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(self.crtRowCount - 9, 0, item)
        self.tw_ditalModel.setSpan(self.crtRowCount - 9, 0, 4, 1)

        item = QTableWidgetItem()
        item.setText("1.火箭军装备分配，按照《装备调拨分配计划》执行；\n"
                     "2.火箭军部队接装，需凭《火箭军装备调拨通知单》；\n"
                     "3.完成装备调拨后，将《装备调拨分配计划》《火箭军装备调拨通知单》第一联，盖章签字后交我局；《火箭军装备调拨通知单》第三联，盖章签字后交接装单位。")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(self.crtRowCount - 9, 1, item)
        self.tw_ditalModel.setSpan(self.crtRowCount - 9, 1, 4, self.crtColumnCount - 1)

        self.initLastFourRow("承办单位:", "(盖章)", "交装单位:", "(盖章)", self.crtRowCount-4)
        self.initLastFourRow("局    长:", "杨刚", "主管领导:", "",self.crtRowCount-3)
        self.initLastFourRow("经 办 人:", "陈燕栋", "经 办 人:", "",self.crtRowCount-2)
        self.initLastFourRow("日    期:", "", "日    期:", "", self.crtRowCount - 1)

        item = QTableWidgetItem()
        item.setText("有效期至: ")
        self.tw_ditalModel.setItem(13, 0, item)

        item = QDateEdit()
        self.tw_ditalModel.setCellWidget(13, 1, item)
        for i in range(self.crtColumnCount):
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(12, i, item)
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(16, i, item)
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(self.crtRowCount - 5, i, item)

        for i in range(2, self.crtColumnCount):
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(13, i, item)


    def initNinethRow(self, first, second, row):
        item = QTableWidgetItem()
        item.setText(first)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, 0, item)


        item = QTableWidgetItem()
        item.setText("")
        half = int((self.crtColumnCount - 2) / 2)
        # print(self.crtColumnCount, half)
        self.tw_ditalModel.setItem(row, 1, item)
        self.tw_ditalModel.setSpan(row, 1, 1, half)

        item = QTableWidgetItem()
        item.setText(second)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, half + 1, item)
        self.factoryInfoList = selectAllDataAboutFactory()
        if row == 3:
            item = QDateEdit()
            half = int((self.crtColumnCount - 4) / 2)
            self.tw_ditalModel.setCellWidget(row, half + 3, item)

            self.tw_ditalModel.setSpan(row, half + 3, 1, self.crtColumnCount - half - 2)
        elif row == 8 or row == 9:
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(row, half + 2, item)
            self.tw_ditalModel.setSpan(row, half + 2, 1, self.crtColumnCount - half - 2)
        elif row == 5:
            item = QComboBox()
            for factoryInfo in self.factoryInfoList:
                item.addItem(factoryInfo[1])
            item.currentIndexChanged.connect(self.slotChangeFactory)
            self.tw_ditalModel.setCellWidget(row, 1, item)
            item = QTableWidgetItem()
            item.setText(self.factoryInfoList[0][2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(row, half + 2, item)
            self.tw_ditalModel.setSpan(row, half + 2, 1, self.crtColumnCount - half - 2)
        else:
            item = QTableWidgetItem()
            item.setText("")
            self.tw_ditalModel.setItem(row, half + 2, item)
            self.tw_ditalModel.setSpan(row, half + 2, 1, self.crtColumnCount - half - 2)

    def initLastFourRow(self, first, second, third, fourth, row):
        item = QTableWidgetItem()
        item.setText(first)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, 0, item)
        half = int((self.crtColumnCount - 4) / 2)
        item = QTableWidgetItem()
        item.setText("")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, 2, item)

        item = QTableWidgetItem()
        item.setText(second)
        self.tw_ditalModel.setItem(row, 1, item)

        if row == 3:
            item = QDateEdit()
            half = int((self.crtColumnCount - 4) / 2)
            # print(self.crtColumnCount, half)
            self.tw_ditalModel.setCellWidget(row, 2, item)
            #self.tw_ditalModel.setSpan(row, 2, 1, half)
        else:
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            half = int((self.crtColumnCount - 4) / 2)
            # print(self.crtColumnCount, half)
            self.tw_ditalModel.setItem(row, 2, item)
            self.tw_ditalModel.setSpan(row, 2, 1, half)

        item = QTableWidgetItem()
        item.setText(third)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, half + 2, item)

        item = QTableWidgetItem()
        item.setText(fourth)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, half + 3, item)

        item = QTableWidgetItem()
        item.setText("")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, half + 4, item)
        self.tw_ditalModel.setSpan(row, half + 4, 1, self.crtColumnCount - half - 3)