from widgets.alocatMange.transferModel import Widget_Transfer_Model
from sysManage.alocatMange.rocketTransfer import rocketTransfer
import sys
from PyQt5.QtWidgets import QDialog,QApplication,QWidget, QMessageBox
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

    def slotClickedSaveTotal(self):
        print("curent, ", self.currentSingelUnitPage)
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

        if self.totalModel.tw_ditalModel.item(5, 1):
            Send_Unit = self.totalModel.tw_ditalModel.item(5, 1).text()
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
            self.totalModel.saveTotalModel()
            for key, page in self.currentSingelUnitPage.items():
                page.saveSingleModel()
            self.signal.emit('1')

    def setCurrentYear(self, year):
        self.currentYear = year

    def getUnitIDList(self, unitInfoList, equipInfo, year, requireInfo):
        self.unitInfoList = unitInfoList
        self.equipInfo = equipInfo
        self.year = year
        self.requireInfo = requireInfo
        self.unitNum = len(unitInfoList)
        self.currentUnitInfoList = unitInfoList
        self.tw_transferModel.clear()

        self.totalModel = totalModel()
        self.totalModel.initTableWidget(self.unitInfoList, self.equipInfo, self.year, self.requireInfo)
        self.tw_transferModel.addTab(self.totalModel, "总单")
        for unitInfo in unitInfoList:
            page = singleModel()
            self.tw_transferModel.addTab(page, unitInfo[0])
            self.currentSingelUnitPage[unitInfo[0]] = page

            page.initTableWidget(unitInfo, self.equipInfo,self.year)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = transferModel()
    widget.getUnitIDList([["1", "", '', '96602' ], ["2","", '', '96603'],
                                         ['3', "", '', '96604' ]], ['3', '装备', '1', '', '', '车'],"2001",
                                        ("良好", "3", '1', '1', '1', '分配依据', '陆军调拨单单号'))
    widget.show()
    sys.exit(app.exec_())

