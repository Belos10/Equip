from widgets.alocatMange.ditalModel import Widget_Dital_Model
from sysManage.alocatMange.rocketTransfer import rocketTransfer
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QTableWidgetItem
from sysManage.alocatMange.armyTransfer import armyTransfer
from database.alocatMangeSql import insertIntoRocketTransfer
from PyQt5.Qt import Qt

'''
   调拨单管理界面
'''
class singleModel(QDialog, Widget_Dital_Model):
    def __init__(self, parent=None):
        super(singleModel, self).__init__(parent)
        self.setupUi(self)
        self.unitNum = 0
        self.title = "火箭军装备调拨通知单"
        self.minSize = 13
        self.isMin = False
        self.tw_ditalModel.horizontalHeader().hide()
        self.tw_ditalModel.verticalHeader().hide()
        self.unitInfo = None
        self.equipInfo = None
        self.year = None

    def initTableWidget(self, unitInfo, equipInfo, year):
        self.year = year
        self.unitInfo = unitInfo
        self.equipInfo = equipInfo
        self.crtColumnCount = 10
        self.tw_ditalModel.setColumnCount((self.crtColumnCount + 1) * 3 - 1)
        self.crtRowCount = 27
        self.tw_ditalModel.setRowCount(self.crtRowCount)

        self.initSingleTable(unitInfo, equipInfo, 0)
        item = QTableWidgetItem()
        item.setText("第一联：存根")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, self.crtColumnCount, item)
        self.tw_ditalModel.setSpan(14, self.crtColumnCount, self.crtRowCount - 23, 1)

        self.initSingleTable(unitInfo, equipInfo, self.crtColumnCount + 1)
        item = QTableWidgetItem()
        item.setText("第二联：发物单位留存")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, self.crtColumnCount * 2 + 1, item)
        self.tw_ditalModel.setSpan(14, self.crtColumnCount * 2 + 1, self.crtRowCount - 23, 1)


        self.initSingleTable(unitInfo, equipInfo, self.crtColumnCount * 2 + 2)
        self.initSingleTable(unitInfo, equipInfo, self.crtColumnCount + 1)
        item = QTableWidgetItem()
        item.setText("第三联：收物单位留存")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, self.crtColumnCount * 3 + 1, item)
        self.tw_ditalModel.setSpan(14, self.crtColumnCount * 3 + 1, self.crtRowCount - 23, 1)

    def initSingleTable(self, unitInfo, equipInfo, startColumn):
        self.unitInfo = unitInfo
        self.equipInfo = equipInfo
        title = QTableWidgetItem()
        title.setText(self.title)
        title.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(0, startColumn, title)
        self.tw_ditalModel.setSpan(0, startColumn, 3, self.crtColumnCount)


        self.initNinethRow('调拨单号:', '调拨日期:', 3, startColumn)
        self.initNinethRow('调拨依据:', '调拨性质:', 4, startColumn)
        self.initNinethRow('交装单位:', '单位地址:', 5, startColumn)
        self.initNinethRow('联系人:', '联系方式:', 6, startColumn)
        self.initNinethRow('军代表:', '联系方式:', 7, startColumn)
        self.initNinethRow('接装单位:', '', 8, startColumn)
        self.initNinethRow('单位地址:', '', 9, startColumn)
        self.initNinethRow('联系人:', '联系方式:', 10, startColumn)
        self.initNinethRow('调拨方式:', '运输方式:', 11, startColumn)

        item = QTableWidgetItem()
        item.setText("编号")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn, item)
        self.tw_ditalModel.setSpan(14, startColumn, 2, 1)

        item = QTableWidgetItem()
        item.setText("装备名称")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn + 1, item)
        self.tw_ditalModel.setSpan(14, startColumn + 1, 2, 1)

        item = QTableWidgetItem()
        item.setText("计量单位")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn + 2, item)
        self.tw_ditalModel.setSpan(14, startColumn + 2, 2, 1)

        item = QTableWidgetItem()
        item.setText("应发数")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn + 3, item)
        self.tw_ditalModel.setSpan(14, startColumn, 1, 2)

        item = QTableWidgetItem()
        item.setText("质量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 3, item)

        item = QTableWidgetItem()
        item.setText("数量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 4, item)

        item = QTableWidgetItem()
        item.setText("实发数")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn + 5, item)
        self.tw_ditalModel.setSpan(14, startColumn + 5, 1, 2)

        item = QTableWidgetItem()
        item.setText("质量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 5, item)

        item = QTableWidgetItem()
        item.setText("数量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 6, item)

        item = QTableWidgetItem()
        item.setText("接收数")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(14, startColumn + 7, item)
        self.tw_ditalModel.setSpan(14, startColumn + 7, 1, 2)

        item = QTableWidgetItem()
        item.setText("质量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 7, item)

        item = QTableWidgetItem()
        item.setText("数量")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 8, item)

        item = QTableWidgetItem()
        item.setText("备注")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(15, startColumn + 8, item)

        item = QTableWidgetItem()
        item.setText("备注")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(self.crtRowCount - 9, startColumn, item)
        self.tw_ditalModel.setSpan(self.crtRowCount - 9, startColumn, 4, 1)

        item = QTableWidgetItem()
        item.setText("1.凭《火箭军装备调拨通知单》接装；\n"
                     "2.完成接装后，将《火箭军装备调拨通知单》三联单，按要求分别盖章签字，并归档。")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(self.crtRowCount - 9, startColumn + 1, item)
        self.tw_ditalModel.setSpan(self.crtRowCount - 9, startColumn + 1, 4, self.crtColumnCount - 1)

        self.initLastFourRow("承办单位:", "(盖章)", "交装单位:", "(盖章)", self.crtRowCount - 4, startColumn)
        self.initLastFourRow("局    长:", "杨刚", "主管领导:", "", self.crtRowCount - 3, startColumn)
        self.initLastFourRow("经 办 人:", "", "经 办 人:", "", self.crtRowCount - 2, startColumn)
        self.initLastFourRow("日    期:", "", "日    期:", "", self.crtRowCount - 1, startColumn)

    def initNinethRow(self, first, second, row, startColumn):
        item = QTableWidgetItem()
        item.setText(first)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, startColumn + 0, item)

        item = QTableWidgetItem()
        item.setText("")
        half = int((self.crtColumnCount - 2) / 2)
        print(self.crtColumnCount, half)
        self.tw_ditalModel.setItem(row, startColumn + 1, item)
        self.tw_ditalModel.setSpan(row, startColumn + 1, 1, half)

        item = QTableWidgetItem()
        item.setText(second)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, startColumn + half + 1, item)

        item = QTableWidgetItem()
        item.setText("")
        self.tw_ditalModel.setItem(row, startColumn + half + 2, item)
        self.tw_ditalModel.setSpan(row, startColumn + half + 2, 1, self.crtColumnCount - half - 2)

    def initLastFourRow(self, first, second, third, fourth, row, startColumn):
        item = QTableWidgetItem()
        item.setText(first)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, startColumn, item)

        item = QTableWidgetItem()
        item.setText(second)
        self.tw_ditalModel.setItem(row, startColumn + 1, item)

        item = QTableWidgetItem()
        item.setText("")
        half = int((self.crtColumnCount - 4) / 2)
        print(self.crtColumnCount, half)
        self.tw_ditalModel.setItem(row, startColumn + 2, item)
        self.tw_ditalModel.setSpan(row, startColumn + 2, 1, half)

        item = QTableWidgetItem()
        item.setText(third)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_ditalModel.setItem(row, startColumn + half + 2, item)

        item = QTableWidgetItem()
        item.setText(fourth)
        self.tw_ditalModel.setItem(row, startColumn + half + 3, item)
        self.tw_ditalModel.setSpan(row, startColumn + half + 3, 1, self.crtColumnCount - half - 2)

    def updateTableWidget(self, requireInfo):
        self.updateSigleTable(requireInfo, 0)
        self.updateSigleTable(requireInfo, self.crtColumnCount + 1)
        self.updateSigleTable(requireInfo, 2 * self.crtColumnCount + 2)

    def updateSigleTable(self, requireInfo, startColumn):
        print(requireInfo)
        half = int((self.crtColumnCount - 4) / 2)
        self.tw_ditalModel.item(3, startColumn+half + 3).setText(requireInfo[0])
        self.tw_ditalModel.item(4, startColumn+1).setText(requireInfo[1])
        self.tw_ditalModel.item(4, startColumn+half + 3).setText(requireInfo[2])
        self.tw_ditalModel.item(5, startColumn+1).setText(requireInfo[3])
        self.tw_ditalModel.item(5, startColumn+half + 3).setText(requireInfo[4])

        self.tw_ditalModel.item(6, startColumn+1).setText(requireInfo[5])
        self.tw_ditalModel.item(6, startColumn+half + 3).setText(requireInfo[6])

        self.tw_ditalModel.item(7, startColumn+1).setText(requireInfo[7])
        self.tw_ditalModel.item(7, startColumn+half + 3).setText(requireInfo[8])
        self.tw_ditalModel.item(8, startColumn+1).setText(requireInfo[-2])
        self.tw_ditalModel.item(11, startColumn+1).setText(requireInfo[-7])
        self.tw_ditalModel.item(11, startColumn+half + 3).setText(requireInfo[-6])

        item = QTableWidgetItem()
        item.setText("有效期至：")
        self.tw_ditalModel.setItem(13, startColumn+0, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[9])
        self.tw_ditalModel.setItem(13, startColumn+1, item)

        item = QTableWidgetItem()
        item.setText("1")
        self.tw_ditalModel.setItem(16, startColumn+0, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[-5])
        self.tw_ditalModel.setItem(16, startColumn+1, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[-4])
        self.tw_ditalModel.setItem(16, startColumn+2, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[-3])
        self.tw_ditalModel.setItem(16, startColumn+3, item)

        item = QTableWidgetItem()
        item.setText(requireInfo[-1])
        self.tw_ditalModel.setItem(16, startColumn+4, item)

    def saveSingleModel(self):
        half = int((self.crtColumnCount - 2) / 2)
        # 调拨单号
        if self.tw_ditalModel.item(3, 1):
            Trans_ID = self.tw_ditalModel.item(3, 1).text()
            print("Trans_ID, ", Trans_ID)
        else:
            Trans_ID = ""

        # 调拨日期
        if self.tw_ditalModel.item(3, half + 2):
            Trans_Date = self.tw_ditalModel.item(3, half + 2).text()
            print("Trans_Date, ", Trans_Date)
        else:
            Trans_Date = ""

        # 调拨依据
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
        if self.tw_ditalModel.item(13, 1):
            Effic_Date = self.tw_ditalModel.item(13, 1).text()
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

        # 交装联系人联系方式
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
        if self.tw_ditalModel.item(16, 3):
            Equip_Quity = self.tw_ditalModel.item(16, 3).text()
            print("Equip_Quity, ", Equip_Quity)
        else:
            Equip_Quity = ""

        # 装备总数
        if self.tw_ditalModel.item(16, 4):
            Equip_Num = self.tw_ditalModel.item(16, 4).text()
            print("Equip_Num, ", Equip_Num)
        else:
            Equip_Num = ""

        # 装备备注
        if self.tw_ditalModel.item(16, self.crtColumnCount - 1):
            Equip_Other = self.tw_ditalModel.item(16, self.crtColumnCount - 1).text()
            print("Equip_Other, ", Equip_Other)
        else:
            Equip_Other = ""

        year = self.year
        ID = Trans_ID + Send_UnitID + Equip_Name

        print(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
              Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
              Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
              Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year)
        insertIntoRocketTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                                 Port_Way, Effic_Date, Send_UnitID, Send_UnitName, Send_Connect,
                                 Send_Tel, Recive_Name, Recive_Connect, Recive_Tel, Equip_ID,
                                 Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, year)