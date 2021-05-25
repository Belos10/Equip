from widgets.alocatMange.ditalModel import Widget_Dital_Model
from sysManage.alocatMange.rocketTransfer import rocketTransfer
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QWidget, QTableWidgetItem, QDateEdit
from sysManage.alocatMange.armyTransfer import armyTransfer
from PyQt5.Qt import Qt
from database.alocatMangeSql import *

'''
   调拨单管理界面
'''
class totalModel(QDialog, Widget_Dital_Model):
    def __init__(self, parent=None):
        super(totalModel, self).__init__(parent)
        self.setupUi(self)

        self.unitNum = 0
        self.title = "装备调拨分配计划"
        self.minSize = 13
        self.isMin = False
        self.tw_ditalModel.horizontalHeader().hide()
        self.tw_ditalModel.verticalHeader().hide()
        self.equipInfo = None
        self.year = ""
        self.requireInfo = None

    def saveTotalModel(self):

        half = int((self.crtColumnCount - 2) / 2)
        #调拨单号
        if self.tw_ditalModel.item(3, 1):
            Trans_ID = self.tw_ditalModel.item(3, 1).text()
            print("Trans_ID, ", Trans_ID)
        else:
            Trans_ID = ""

        #调拨日期
        if self.tw_ditalModel.cellWidget(3, half + 2):
            Trans_Date = self.tw_ditalModel.cellWidget(3, half + 2).text()
            print("Trans_Date================================, ", Trans_Date)
        else:
            Trans_Date = ""
            print("transdataelse====================================")

        #调拨依据
        if self.tw_ditalModel.item(4, 1):
            Trans_Reason = self.tw_ditalModel.item(4, 1).text()
            print("Trans_Reason, ", Trans_Reason)
        else:
            Trans_Reason = ""

        # 调拨性质
        if self.tw_ditalModel.item(4, half + 2):
            Trans = self.tw_ditalModel.item(4, half + 2).text()
            print("Trans, ", Trans)
        else:
            Trans = ""
            print("Trans===============")

        # 调拨方式
        if self.tw_ditalModel.item(11, 1):
            Trans_Way = self.tw_ditalModel.item(11, 1).text()
            print("Trans_Way, ", Trans_Way)
        else:
            Trans_Way = ""

        # 运输方式
        if self.tw_ditalModel.item(11, half + 2):
            Port_Way = self.tw_ditalModel.item(11, half + 2).text()
            print("Port_Way, ", Port_Way)
        else:
            Port_Way = ""

        # 有效日期
        if self.tw_ditalModel.cellWidget(13, 1):
            Effic_Date = self.tw_ditalModel.cellWidget(13, 1).text()
            print("Effic_Date, ", Effic_Date)
        else:
            Effic_Date = ""

        # 交装联系人
        if self.tw_ditalModel.item(6, 1):
            Send_Connect = self.tw_ditalModel.item(6, 1).text()
            print("Send_Connect, ", Send_Connect)
        else:
            Send_Connect = ""

        Send_UnitID = ""
        # 交装单位
        if self.tw_ditalModel.item(5, 1):
            Send_UnitName = self.tw_ditalModel.item(5, 1).text()
            print("Send_UnitName, ", Send_UnitName)
        else:
            Send_UnitName = ""

        #交装联系人联系方式
        if self.tw_ditalModel.item(6, half + 2):
            Send_Tel = self.tw_ditalModel.item(6, half + 2).text()
            print("Send_Tel, ", Send_Tel)
        else:
            Send_Tel = ""

        # 接装单位
        if self.tw_ditalModel.item(8, 1):
            Recive_Name = self.tw_ditalModel.item(8, 1).text()
            print("Recive_Name, ", Recive_Name)
        else:
            Recive_Name = ""

        # 接装联系人
        if self.tw_ditalModel.item(10, 1):
            Recive_Connect = self.tw_ditalModel.item(10, 1).text()
            print("Recive_Connect, ", Recive_Connect)
        else:
            Recive_Connect = ""

        # 接装联系人联系方式
        if self.tw_ditalModel.item(10, half + 2):
            Recive_Tel = self.tw_ditalModel.item(10, half + 2).text()
            print("Recive_Tel, ", Recive_Tel)
        else:
            Recive_Tel = ""
        Equip_ID = self.equipInfo[0]
        Equip_Name = self.equipInfo[1]
        Equip_Unit = self.equipInfo[5]
        # 装备质量
        if self.tw_ditalModel.item(15, 3):
            Equip_Quity = self.tw_ditalModel.item(15, 3).text()
            print("Equip_Quity, ", Equip_Quity)
        else:
            Equip_Quity = ""

        # 装备总数
        if self.tw_ditalModel.item(15, 4):
            Equip_Num = self.tw_ditalModel.item(15, 4).text()
            print("Equip_Num, ", Equip_Num)
        else:
            Equip_Num = ""

        # 装备备注
        if self.tw_ditalModel.item(15, self.crtColumnCount - 1):
            Equip_Other = self.tw_ditalModel.item(15, self.crtColumnCount - 1).text()
            print("Equip_Other, ", Equip_Other)
        else:
            Equip_Other = ""

        year = self.year
        ID = Trans_ID + Send_UnitID + Equip_Name

        # print(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
        #                          Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
        #                          Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
        #                          Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year)
        print("transdata=",Trans_Date)
        insertIntoRocketTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                                 Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                                 Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                                 Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year)

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

        for i in range(5, self.crtColumnCount - 1):
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_ditalModel.setItem(14, i, item)

        item = QTableWidgetItem()
        item.setText("备注")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, self.crtColumnCount - 1, item)

        for i, num in enumerate(requireInfo[2:-2]):
            item = QTableWidgetItem()
            item.setText(num)
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
        print(self.crtColumnCount, half)
        self.tw_ditalModel.setItem(row, 1, item)
        self.tw_ditalModel.setSpan(row, 1, 1, half)

        item = QTableWidgetItem()
        item.setText(second)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, half + 1, item)

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
            print(self.crtColumnCount, half)
            self.tw_ditalModel.setCellWidget(row, 2, item)
            #self.tw_ditalModel.setSpan(row, 2, 1, half)
        else:
            item = QTableWidgetItem()
            item.setText("")
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            half = int((self.crtColumnCount - 4) / 2)
            print(self.crtColumnCount, half)
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