from PyQt5.QAxContainer import QAxObject

from widgets.alocatMange.transferModel import Widget_Transfer_Model
from sysManage.alocatMange.rocketTransfer import rocketTransfer
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QWidget, QMessageBox,QFileDialog, QTableWidgetItem
from sysManage.alocatMange.armyTransfer import armyTransfer
from sysManage.alocatMange.totalModel import totalModel
from sysManage.alocatMange.singleModel import singleModel
from database.alocatMangeSql import *
from PyQt5 import QtCore
'''
   调拨单管理界面
'''

class transferModel(QDialog, Widget_Transfer_Model):
    signal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(transferModel, self).__init__(parent)
        self.setupUi(self)

        self.unitNum = 0
        self.currentSingelUnitPage = {}
        self.currentUnitInfoList = []
        self.currentYear = ""
        self.signalConnect()
        self.setWindowTitle("火箭军调拨单")

    def signalConnect(self):
        self.pb_confirm.clicked.connect(self.slotClickedConfim)

        self.pb_saveTotal.clicked.connect(self.slotClickedSaveTotal)

        self.pb_output.clicked.connect(self.slotClickedOutput)

        self.pb_saveSingle.clicked.connect(self.slotSaveSingle)

    def slotClickedOutput(self):
        pass

    # 保存分单
    def slotSaveSingle(self):
        print("保存分单")
        for key, page in self.currentSingelUnitPage.items():
            half = int((page.crtColumnCount - 2) / 2)
            # 调拨单号
            if page.tw_ditalModel.item(3, 1):
                Trans_ID = page.tw_ditalModel.item(3, 1).text()
                print("Trans_ID, ", Trans_ID)
            else:
                Trans_ID = ""
            item1 = QTableWidgetItem()
            item1.setText(Trans_ID)
            item2 = QTableWidgetItem()
            item2.setText(Trans_ID)
            page.tw_ditalModel.setItem(3, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(3, 2*page.crtColumnCount + 2 + 1, item2)

            # 调拨日期
            if page.tw_ditalModel.item(3, half + 2):
                Trans_Date = page.tw_ditalModel.item(3, half + 2).text()
                print("Trans_Date, ", Trans_Date)
            else:
                Trans_Date = ""
            item1 = QTableWidgetItem()
            item1.setText(Trans_Date)
            item2 = QTableWidgetItem()
            item2.setText(Trans_Date)
            page.tw_ditalModel.setItem(3, page.crtColumnCount + 1 + half + 2, item1)
            page.tw_ditalModel.setItem(3, 2*page.crtColumnCount + 2 + half + 2,item2)

            # 调拨依据
            if page.tw_ditalModel.item(4, 1):
                Trans_Reason = page.tw_ditalModel.item(4, 1).text()
                print("Trans_Reason, ", Trans_Reason)
            else:
                Trans_Reason = ""
            item1 = QTableWidgetItem()
            item1.setText(Trans_Reason)
            item2 = QTableWidgetItem()
            item2.setText(Trans_Reason)
            page.tw_ditalModel.setItem(4, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(4, 2*page.crtColumnCount + 2 + 1, item2)

            # 调拨性质
            if page.tw_ditalModel.item(4, half + 2):
                Trans = page.tw_ditalModel.item(4, half + 2).text()
                print("Trans, ", Trans)
            else:
                Trans = ""
            item1 = QTableWidgetItem()
            item1.setText(Trans)
            item2 = QTableWidgetItem()
            item2.setText(Trans)
            page.tw_ditalModel.setItem(4, page.crtColumnCount + 1 + half + 2, item1)
            page.tw_ditalModel.setItem(4, 2*page.crtColumnCount + 2 + half + 2, item2)


            # 交装联系人
            if page.tw_ditalModel.item(6, 1):
                Send_Connect = page.tw_ditalModel.item(6, 1).text()
                print("Send_Connect, ", Send_Connect)
            else:
                Send_Connect = ""
            item1 = QTableWidgetItem()
            item1.setText(Send_Connect)
            item2 = QTableWidgetItem()
            item2.setText(Send_Connect)
            page.tw_ditalModel.setItem(6, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(6, 2*page.crtColumnCount + 2 + 1, item2)

            Send_UnitID = ""
            # 交装单位
            if page.tw_ditalModel.item(5, 1):
                Send_UnitName = page.tw_ditalModel.item(5, 1).text()
                print("Send_UnitName, ", Send_UnitName)
            else:
                Send_UnitName = ""
            item1 = QTableWidgetItem()
            item1.setText(Send_UnitName)
            item2 = QTableWidgetItem()
            item2.setText(Send_UnitName)
            page.tw_ditalModel.setItem(5, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(5, 2*page.crtColumnCount + 2 + 1, item2)

            # 交装联系人电话
            if page.tw_ditalModel.item(6, half + 2):
                Send_Tel = page.tw_ditalModel.item(6, half + 2).text()
                print("Send_Tel, ", Send_Tel)
            else:
                Send_Tel = ""
            item1 = QTableWidgetItem()
            item1.setText(Send_Tel)
            item2 = QTableWidgetItem()
            item2.setText(Send_Tel)
            page.tw_ditalModel.setItem(6, page.crtColumnCount + 1 + half + 2, item1)
            page.tw_ditalModel.setItem(6, 2*page.crtColumnCount + 2 + half + 2, item2)

            # 接装单位地址
            if page.tw_ditalModel.item(9, 1):
                Recive_Add = page.tw_ditalModel.item(9, 1).text()
                print("Recive_Add, ", Recive_Add)
            else:
                Recive_Add = ""
            item1 = QTableWidgetItem()
            item1.setText(Recive_Add)
            item2 = QTableWidgetItem()
            item2.setText(Recive_Add)
            page.tw_ditalModel.setItem(9, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(9, 2 * page.crtColumnCount + 2 + 1, item2)

            # 接装单位
            if page.tw_ditalModel.item(8, 1):
                Recive_Name = page.tw_ditalModel.item(8, 1).text()
                print("Recive_Name, ", Recive_Name)
            else:
                Recive_Name = ""
            item1 = QTableWidgetItem()
            item1.setText(Recive_Name)
            item2 = QTableWidgetItem()
            item2.setText(Recive_Name)
            page.tw_ditalModel.setItem(8, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(8, 2*page.crtColumnCount + 2 + 1, item2)

            # 接装联系人
            if page.tw_ditalModel.item(10, 1):
                Recive_Connect = page.tw_ditalModel.item(10, 1).text()
                print("Recive_Connect, ", Recive_Connect)
            else:
                Recive_Connect = ""
            item1 = QTableWidgetItem()
            item1.setText(Recive_Connect)
            item2 = QTableWidgetItem()
            item2.setText(Recive_Connect)
            page.tw_ditalModel.setItem(10, page.crtColumnCount + 1 + 1, item1)
            page.tw_ditalModel.setItem(10, 2*page.crtColumnCount + 2 + 1, item2)
            # 接装联系人联系方式
            if page.tw_ditalModel.item(10, half + 2):
                Recive_Tel = page.tw_ditalModel.item(10, half + 2).text()
                print("Recive_Tel, ", Recive_Tel)
            else:
                Recive_Tel = ""
            item1 = QTableWidgetItem()
            item1.setText(Recive_Tel)
            item2 = QTableWidgetItem()
            item2.setText(Recive_Tel)
            page.tw_ditalModel.setItem(10, page.crtColumnCount + 1 + half + 2, item1)
            page.tw_ditalModel.setItem(10, 2*page.crtColumnCount + 2 + half+2, item2)

    # 保存总单
    def slotClickedSaveTotal(self):
        print("保存总单, ", self.currentSingelUnitPage)
        half = int((self.totalModel.crtColumnCount - 4) / 2)
        if self.totalModel.tw_ditalModel.cellWidget(3,  half + 3):
            Trans_Date = self.totalModel.tw_ditalModel.cellWidget(3, half + 3).text()
            print("Trans_Date, ", Trans_Date)
        else:
            Trans_Date = ""

        if self.totalModel.tw_ditalModel.item(4, 1):
            Trans_Reason = self.totalModel.tw_ditalModel.item(4, 1).text()
            print("Trans_Reason, ", Trans_Reason)
        else:
            Trans_Reason = ""

        if self.totalModel.tw_ditalModel.item(4, half + 3):
            Trans = self.totalModel.tw_ditalModel.item(4, half + 3).text()
            print("Trans, ", Trans)
        else:
            Trans = ""

        if self.totalModel.tw_ditalModel.cellWidget(5, 1):
            Send_Unit = self.totalModel.tw_ditalModel.cellWidget(5, 1).currentText()
            print("Send_Unit, ", Send_Unit)
        else:
            Send_Unit = ""

        if self.totalModel.tw_ditalModel.item(5, half + 3):
            Send_Address = self.totalModel.tw_ditalModel.item(5, half + 3).text()
            print("Send_Address, ", Send_Address)
        else:
            Send_Address = ""

        if self.totalModel.tw_ditalModel.item(6, 1):
            Send_People = self.totalModel.tw_ditalModel.item(6, 1).text()
            print("Send_People, ", Send_People)
        else:
            Send_People = ""

        if self.totalModel.tw_ditalModel.item(6, half + 3):
            Send_Tel1 = self.totalModel.tw_ditalModel.item(6, half + 3).text()
            print("Send_Tel1, ", Send_Tel1)
        else:
            Send_Tel1 = ""

        if self.totalModel.tw_ditalModel.item(7, 1):
            Send_Represent = self.totalModel.tw_ditalModel.item(7, 1).text()
            print("Send_Represent, ", Send_Represent)
        else:
            Send_Represent = ""

        if self.totalModel.tw_ditalModel.item(7, half + 3):
            Send_Tel2 = self.totalModel.tw_ditalModel.item(7, half + 3).text()
            print("Send_Tel2, ", Send_Tel2)
        else:
            Send_Tel2 = ""

        if self.totalModel.tw_ditalModel.cellWidget(13, 1):
            Effice_Date = self.totalModel.tw_ditalModel.cellWidget(13, 1).text()
            print("Effice_Date, ", Effice_Date)
        else:
            Effice_Date = ""

        if self.totalModel.tw_ditalModel.item(11, 1):
            Trans_Way = self.totalModel.tw_ditalModel.item(11, 1).text()
            print("Trans_Way, ", Trans_Way)
        else:
            Trans_Way = ""

        if self.totalModel.tw_ditalModel.item(11, half + 3):
            Port_Way = self.totalModel.tw_ditalModel.item(11, half + 3).text()
            print("Port_Way, ", Port_Way)
        else:
            Port_Way = ""

        if self.totalModel.tw_ditalModel.item(15, 3):
            Equip_Quity = self.totalModel.tw_ditalModel.item(15, 3).text()
            print("Equip_Quity, ", Equip_Quity)
        else:
            Equip_Quity = ""

        unitOtherName = []
        for unitInfo in self.totalModel.unitInfoList:
            unitOtherName.append(unitInfo[3])

        numList = []
        for num in self.totalModel.requireInfo[2: -2]:
            numList.append(num)

        for key, page in self.currentSingelUnitPage.items():
            for i, unitInfo in enumerate(self.totalModel.unitInfoList):
                print("key", key, "unitInfo", unitInfo)
                requireInfo = []
                requireInfo.append(Trans_Date)
                requireInfo.append(Trans_Reason)
                requireInfo.append(Trans)
                requireInfo.append(Send_Unit)
                requireInfo.append(Send_Address)
                requireInfo.append(Send_People)
                requireInfo.append(Send_Tel1)
                requireInfo.append(Send_Represent)
                requireInfo.append(Send_Tel2)
                requireInfo.append(Effice_Date)
                requireInfo.append(Trans_Way)
                requireInfo.append(Port_Way)
                requireInfo.append(Send_Unit)
                requireInfo.append(Send_Address)
                requireInfo.append(Send_People)
                requireInfo.append(Send_Tel1)
                requireInfo.append(Send_Represent)
                requireInfo.append(Send_Tel2)
                requireInfo.append(Effice_Date)
                requireInfo.append(Trans_Way)
                requireInfo.append(Port_Way)
                requireInfo.append(self.totalModel.equipInfo[1])
                requireInfo.append(self.totalModel.equipInfo[5])
                requireInfo.append(Equip_Quity)
                if key == unitInfo[0]:
                    print("hao")
                    requireInfo.append(unitInfo[3])
                    requireInfo.append(self.totalModel.requireInfo[2 + i])
                    page.updateTableWidget(requireInfo)

    def slotClickedConfim(self):
        reply = QMessageBox.question(self, '保存', '是否将调拨信息存入火箭军调拨单并已经导出调拨单？', QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        else:
            self.pb_confirm.setDisabled(True)
            self.pb_saveSingle.setDisabled(True)
            self.pb_saveTotal.setDisabled(True)
            self.pb_input.setDisabled(True)
            self.totalModel.setDisabled(True)
            self.totalModel.saveTotalModel()
            for key, page in self.currentSingelUnitPage.items():
                page.saveSingleModel()
                page.setDisabled(True)
            self.signal.emit('1')

    def setCurrentYear(self, year):
        self.currentYear = year

    def getUnitIDList(self, unitInfoList, equipInfo, year, requireInfo):
        #print("===========", requireInfo)
        if unitInfoList == "" and equipInfo =="" and  year =="" and  requireInfo == "":
            self.pb_input.setDisabled(True)
            self.pb_output.setDisabled(True)
            self.pb_saveTotal.setDisabled(True)
            self.pb_saveSingle.setDisabled(True)
            self.pb_confirm.setDisabled(True)
            return
        #print("==============================")
        self.pb_input.setDisabled(False)
        self.pb_output.setDisabled(False)
        self.pb_saveTotal.setDisabled(False)
        self.pb_saveSingle.setDisabled(False)
        self.pb_confirm.setDisabled(False)
        self.unitInfoList = unitInfoList
        self.equipInfo = equipInfo
        self.year = year
        self.requireInfo = requireInfo
        self.unitNum = len(unitInfoList)
        self.currentUnitInfoList = unitInfoList
        self.tw_transferModel.clear()
        #print("requireInfo :==============", requireInfo)
        #####
        self.totalModel = totalModel()
        self.totalModel.initTableWidget(self.unitInfoList, self.equipInfo, self.year, self.requireInfo)
        self.tw_transferModel.addTab(self.totalModel, "总单")
        print("require", self.requireInfo)
        for unitInfo, num in zip(unitInfoList, requireInfo[2: -2]):
            if num == "" or num == "0":
                continue
            page = singleModel()
            self.tw_transferModel.addTab(page, unitInfo[0])
            self.currentSingelUnitPage[unitInfo[0]] = page
            page.initTableWidget(unitInfo, self.equipInfo,self.year)
        #######
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = transferModel()
    widget.getUnitIDList([["1", "", '', '96602' ], ["2","", '', '96603'],
                                         ['3', "", '', '96604' ]], ['3', '装备', '1', '', '', '车'],"2001",
                                        ("良好", "3", '1', '1', '1', '分配依据', '陆军调拨单单号'))
    widget.show()
    sys.exit(app.exec_())

