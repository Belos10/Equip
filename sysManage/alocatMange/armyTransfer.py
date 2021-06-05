from widgets.alocatMange.armyTransfer import Widget_Army_Transfer
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem, QComboBox, QTableWidgetItem, QDateEdit, \
    QInputDialog, QMessageBox, QPushButton, QFileDialog
from database.alocatMangeSql import *
from database.strengthDisturbSql import *
from sysManage.alocatMange.config import ArmyTransferReceiveUnit, ArmyTransferSendUnit
from PyQt5.Qt import Qt
from database.dictSelect.factorySetSql import *

#new
'''
    功能：
        陆军调拨单管理
'''
class armyTransfer(QWidget, Widget_Army_Transfer):
    def __init__(self, parent=None):
        super(armyTransfer, self).__init__(parent)
        self.setupUi(self)

        #设置tablewidget左侧栏以及头部不显示
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)

        #初始化当前界面
        self._initSelf_()

        #信号连接
        self.signalConnect()

        #存储当前结果，结构为：{i（行数）：一行数据}
        self.currentResult = {}
        startEquipIDInfo = findUperEquipIDByName("通用装备")
        self.equipInfoList = []
        for startEquipInfo in startEquipIDInfo:
            self.equipInfoList.append(startEquipInfo)
            self._initEquipInfoList_(startEquipInfo)
            break

    '''
        信号连接
    '''
    def signalConnect(self):
        #当前年份筛选列表被选中某行
        self.lw_yearChoose.itemPressed.connect(self.slotSelectResult)
        #新增一行空白行
        self.pb_add.clicked.connect(self.addNewRow)
        #新增一个年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        #保存新增的数据
        self.pb_save.clicked.connect(self.slotSaveNewAdd)
        #删除当前行
        self.pb_del.clicked.connect(self.slotDelCurrentRow)
        #删除某年
        self.tb_del.clicked.connect(self.slotDelCurrentYear)
        #导出至Excel
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)


    '''
        关闭信号
    '''
    def disconnectSlot(self):
        # 当前年份筛选列表被选中某行
        self.lw_yearChoose.itemPressed.disconnect(self.slotSelectResult)
        # 新增一行空白行
        self.pb_add.clicked.disconnect(self.addNewRow)
        # 新增一个年份
        self.tb_add.clicked.disconnect(self.slotAddNewYear)
        # 保存新增的数据
        self.pb_save.clicked.disconnect(self.slotSaveNewAdd)
        # 删除当前行
        self.pb_del.clicked.disconnect(self.slotDelCurrentRow)
        # 删除某年
        self.tb_del.clicked.disconnect(self.slotDelCurrentYear)

    '''
        初始化当前界面，设置当前查询结果界面为灰
    '''
    def _initSelf_(self):
        self.tw_result.clear()
        self.groupBox_2.setDisabled(True)
        #初始化年份listwidget
        self._initYearWidget_()

    '''
        删除当前行
        逻辑：
            查看当前行是否在范围内，是的话删除
    '''
    def slotDelCurrentRow(self):
        currentRow = self.tw_result.currentRow()
        if len(self.currentResult) + 2 < currentRow and currentRow != -1:
            self.tw_result.removeRow(currentRow)
            return
        #print(currentRow)
        if currentRow < 2:
            reply = QMessageBox.question(self, '删除', '当前未选中某行，请选中某行删除', QMessageBox.Yes)
            return
        else:
            reply = QMessageBox.question(self, '删除', '是否删除当前行？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                #根据陆军调拨单的序号以及年份删除当前行
                delArmyTransferByIDAndYear(self.tw_result.item(currentRow, 0).text(), self.currentYear)
                #删除后重新显示结果界面
                self.slotSelectResult()
            else:
                return

    '''
        保存新增结果
    '''
    def slotSaveNewAdd(self):
        currentRowNum = self.tw_result.rowCount() - 2
        addRow = 2 + self.orginRowCount
        IDList = selectIDFromArmyByYear(self.currentYear)
        equipIDList = selectEquipIDFromArmyByYear(self.currentYear)
        #print("IDList :", IDList)
        for i in range(currentRowNum - self.orginRowCount):
            haveID = False
            if self.tw_result.item(i + addRow, 0):
                pass
            else:
                ID = ""
            ID = self.tw_result.item(i + addRow, 0).text()
            if ID == "":
                reply = QMessageBox.question(self, '新增', '第' + str(i + addRow - 1) + '添加失败，序号不能为空', QMessageBox.Yes)
                continue
            for id in IDList:
                if ID == id:
                    haveID = True

            if haveID:
                reply = QMessageBox.question(self, '新增', '第' + str(i + addRow- 1) + '添加失败，当前年份当前序号已存在', QMessageBox.Yes)
                continue
            if self.tw_result.item(i + addRow, 17):
                pass
            else:
                Equip_Num = "-"
            Equip_Num = self.tw_result.item(i + addRow, 17).text()
            if Equip_Num.isdigit():
                pass
            else:
                reply = QMessageBox.question(self, '新增', '第' + str(i + addRow-1) + '添加失败，数量必须为整数', QMessageBox.Yes)
                continue
            index = self.tw_result.cellWidget(i + addRow, 14).currentIndex()
            Equip_ID = self.currentEquipInfo[index][0]
            haveEquip = False
            for equipID in equipIDList:
                if Equip_ID == equipID:
                    haveEquip = True
            if haveEquip:
                reply = QMessageBox.information(self, '新增', '第' + str(i + addRow - 1) + '添加失败，当前年份该装备已录入', QMessageBox.Yes)
                continue
            if self.tw_result.item(i + addRow, 1):
                Trans_ID = self.tw_result.item(i + addRow, 1).text()
            else:
                Trans_ID = ""
            if self.tw_result.cellWidget(i + addRow, 2):
                Trans_Date = self.tw_result.cellWidget(i + addRow, 2).text()
            else:
                Trans_Date = ""
            Trans_Date = self.currentYear + "/" + Trans_Date
            #print(Trans_Date)
            if self.tw_result.item(i + addRow, 3):
                Trans_Reason = self.tw_result.item(i + addRow, 3).text()
            else:
                Trans_Reason = ""
            if self.tw_result.item(i + addRow, 4):
                Trans = self.tw_result.item(i + addRow, 4).text()
            else:
                Trans = ""
            if self.tw_result.cellWidget(i + addRow, 5):
                Trans_Way = self.tw_result.cellWidget(i + addRow, 5).currentText()
            else:
                Trans_Way = ""

            if self.tw_result.item(i + addRow, 6):
                Port_Way = self.tw_result.item(i + addRow, 6).text()
            else:
                Port_Way = ""

            if self.tw_result.cellWidget(i + addRow, 7):
                Effic_Date = self.tw_result.cellWidget(i + addRow, 7).text()
            else:
                Effic_Date = ""

            if self.tw_result.cellWidget(i + addRow, 8):
                index = self.tw_result.cellWidget(i + addRow, 8).currentIndex()
                if self.factoryInfoList:
                    Send_UintID = self.factoryInfoList[index][0]
                    Send_UnitName = self.factoryInfoList[index][1]
                else:
                    Send_UintID = ""
                    Send_UnitName = ""
            else:
                Send_UintID = ""
                Send_UnitName = ""

            if self.tw_result.item(i + addRow, 9):
                Send_Connect = self.tw_result.item(i + addRow, 9).text()
            else:
                Send_Connect = ""
            if self.tw_result.item(i + addRow, 10):
                Send_Tel = self.tw_result.item(i + addRow, 10).text()
            else:
                Send_Tel = ""

            if self.tw_result.item(i + addRow, 11):
                Receive_Name = self.tw_result.item(i + addRow, 11).text()
            else:
                Receive_Name = ""

            if self.tw_result.item(i + addRow, 12):
                Receive_Connect = self.tw_result.item(i + addRow, 12).text()
            else:
                Receive_Connect = ""

            if self.tw_result.item(i + addRow, 13):
                Receive_Tel = self.tw_result.item(i + addRow, 13).text()
            else:
                Receive_Tel = ""

            if self.tw_result.cellWidget(i + addRow, 14):
                Equip_Name = self.tw_result.cellWidget(i + addRow, 14).currentText()
            else:
                Equip_Name = ""
            if self.tw_result.item(i + addRow, 15):
                Equip_Unit = self.tw_result.item(i + addRow, 15).text()
            else:
                Equip_Unit = ""

            if self.tw_result.cellWidget(i + addRow, 16):
                Equip_Quity = self.tw_result.cellWidget(i + addRow, 16).currentText()
            else:
                Equip_Quity = ""

            if self.tw_result.item(i + addRow, 18):
                Equip_Other = self.tw_result.item(i + addRow, 18).text()
            else:
                Equip_Other = ""
            insertIntoArmyTransfer(ID, Trans_ID, Trans_Date, Trans_Reason, Trans, Trans_Way,
                                   Port_Way, Effic_Date, Send_UintID, Send_UnitName, Send_Connect,
                                   Send_Tel, Receive_Name, Receive_Connect, Receive_Tel,
                                   Equip_ID, Equip_Name, Equip_Unit, Equip_Quity, Equip_Num, Equip_Other, self.currentYear)
            self.slotSelectResult()

    '''
       新增一个年份
    '''
    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if year:
            insertIntoArmyTransferYear(year)
            self._initYearWidget_()

    '''
       删除当前选中年份
    '''
    def slotDelCurrentYear(self):
        currentRow = self.lw_yearChoose.currentRow()
        if currentRow == 0:
            reply = QMessageBox.question(self, '删除', '是否删除所有年份以及年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if QMessageBox.Cancel:
                return
        if currentRow < 0:
            reply = QMessageBox.question(self, '删除', '请选中某年进行删除', QMessageBox.Yes)
        else:
            currentYear = self.lw_yearChoose.currentItem().text()
            reply = QMessageBox.question(self, '删除', '是否删除当前年份以及当前年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delArmyTransferYearByYear(currentYear)
                self._initSelf_()
            else:
                return

    '''
        初始化年份listwidget
    '''
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = ''
        self.lw_yearChoose.clear()
        self.yearList = []
        allYear = selectYearListAboutArmy()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)

    '''
        初始化结果tablewidget表头
    '''
    def _initResultHeader_(self):
        self.orginRowCount = 0
        self.tw_result.clear()
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText('序号')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setText('调拨单信息')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setText('交装单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 8, item)
        item = QTableWidgetItem()
        item.setText('接装单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 11, item)
        item = QTableWidgetItem()
        item.setText('装备名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 14, item)
        item = QTableWidgetItem()
        item.setText('计量单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 15, item)
        item = QTableWidgetItem()
        item.setText('应发数')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 16, item)
        item = QTableWidgetItem()
        item.setText('备注')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 18, item)
        item = QTableWidgetItem()

        item.setText('调拨单号')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 1, item)
        item = QTableWidgetItem()
        item.setText('调拨日期')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)
        item = QTableWidgetItem()
        item.setText('调拨依据')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        item = QTableWidgetItem()
        item.setText('调拨')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        item = QTableWidgetItem()
        item.setText('调拨方式')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)
        item = QTableWidgetItem()
        item.setText('运输方式')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)
        item = QTableWidgetItem()
        item.setText('有效日期')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 7, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 8, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 9, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 13, item)
        item = QTableWidgetItem()
        item.setText('质量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 16, item)
        item = QTableWidgetItem()
        item.setText('数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)   #设置当前item不能被修改
        self.tw_result.setItem(1, 17, item)

        self.tw_result.setSpan(0, 0, 2, 1)
        self.tw_result.setSpan(0, 1, 1, 7)
        self.tw_result.setSpan(0, 8, 1, 3)
        self.tw_result.setSpan(0, 11, 1, 3)
        self.tw_result.setSpan(0, 16, 1, 2)
        self.tw_result.setSpan(0, 14, 2, 1)
        self.tw_result.setSpan(0, 15, 2, 1)
        self.tw_result.setSpan(0, 18, 2, 1)

    '''
        查找当前要显示的数据并显示到tablewidget上
    '''
    def slotSelectResult(self):
        self.currentResult = {}
        self.groupBox_2.setDisabled(False)
        self._initResultHeader_()
        self.orginRowCount = 0      #当前结果界面的查询个数
        row = self.lw_yearChoose.currentRow()
        self.currentYear = self.lw_yearChoose.item(row).text()  #当前选中的年份
        resultList = selectArmyTransferByYear(self.currentYear)
        self.tw_result.setRowCount(len(resultList) + 2)
        self.orginRowCount = len(resultList)
        for i, armyTransferInfo in enumerate(resultList):
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 0, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 1, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 2, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 3, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 4, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[5])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 5, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[6])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 6, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[7])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 7, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[9])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 8, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 9, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[11])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 10, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[12])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 11, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[13])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 12, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[14])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 13, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[16])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 14, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[17])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 15, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[18])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 16, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[19])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 17, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[20])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 18, item)
            self.currentResult[i] = armyTransferInfo

    def _initEquipInfoList_(self, root):
        if root[0] == '':
            result = selectEquipInfoByEquipUper('')
        else:
            result = selectEquipInfoByEquipUper(root[0])
        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            self.equipInfoList.append(rowData)
            if rowData[0] != '':
                self._initEquipInfoList_(rowData)

    def slotCurrentIndexChanged(self):
        row = self.tw_result.currentRow()
        index = self.tw_result.cellWidget(row, 14).currentIndex()
        if index >= 0:
            unit = self.currentEquipInfo[index][5]
            self.tw_result.item(row, 15).setText(unit)
    '''
        增加新行等待用户输入
    '''
    def addNewRow(self):
        startEquipIDInfo = findUperEquipIDByName("通用装备")
        self.equipInfoList = []
        for startEquipInfo in startEquipIDInfo:
            self.equipInfoList.append(startEquipInfo)
            self._initEquipInfoList_(startEquipInfo)
            break
        print(self.equipInfoList)
        if self.currentYear == '全部' or self.currentYear == None:
            reply = QMessageBox.question(self, '新增', '只能对某年的数据进行新增，请重新选择', QMessageBox.Yes)
            return
        currentRow = self.tw_result.rowCount()
        self.tw_result.setRowCount(currentRow + 1)

        for i in range(19):
            self.factoryInfoList = selectAllDataAboutFactory()
            if i == 14:
                self.currentEquipInfo = []
                equipCombo = QComboBox()
                for equipInfo in self.equipInfoList:
                    if EquipNotHaveChild(equipInfo[0]):
                        equipCombo.addItem(equipInfo[1])
                        self.currentEquipInfo.append(equipInfo)
                self.tw_result.setCellWidget(currentRow, i, equipCombo)
                equipCombo.currentIndexChanged.connect(self.slotCurrentIndexChanged)
                if self.currentEquipInfo:
                    item = QTableWidgetItem()
                    item.setText(self.currentEquipInfo[0][5])
                    self.tw_result.setItem(currentRow, i+1, item)

            elif i == 15:
                pass
            elif i == 2:
                dateEdit = QDateEdit()
                dateEdit.setDisplayFormat("MM/dd")
                self.tw_result.setCellWidget(currentRow, i, dateEdit)
            elif i == 7:
                dateEdit = QDateEdit()
                dateEdit.setDisplayFormat("yyyy/MM/dd")
                self.tw_result.setCellWidget(currentRow, i, dateEdit)
            elif i == 11:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['单位名称'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 12:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['联系人'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 13:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['联系电话'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 8:

                item = QComboBox()
                for factoryInfo in self.factoryInfoList:
                    item.addItem(factoryInfo[1])
                item.currentIndexChanged.connect(self.slotChangeFactory)
                self.tw_result.setCellWidget(currentRow, i, item)
            elif i == 9:
                item = QTableWidgetItem()
                if self.factoryInfoList:
                    item.setText(self.factoryInfoList[0][3])
                else:
                    item.setText("")
                self.tw_result.setItem(currentRow, i, item)
            elif i == 10:
                item = QTableWidgetItem()
                if self.factoryInfoList:
                    item.setText(self.factoryInfoList[0][4])
                else:
                    item.setText("")
                self.tw_result.setItem(currentRow, i, item)
            elif i == 5:
                item = QComboBox()
                item.addItem("自提")
                item.addItem("厂家交付")
                self.tw_result.setCellWidget(currentRow,i,item)
            elif i == 16:
                item = QComboBox()
                item.addItem("新品")
                item.addItem("堪用品")
                item.addItem("待修品")
                item.addItem("废品")
                self.tw_result.setCellWidget(currentRow, i, item)
            else:
                item = QTableWidgetItem()
                item.setText("")
                self.tw_result.setItem(currentRow, i, item)

    def slotChangeFactory(self, index):
        row = self.tw_result.currentRow()
        column = self.tw_result.currentColumn()
        if row < 0 or column < 0:
            return
        if self.tw_result.item(row, 9):
            self.tw_result.item(row, 9).setText(self.factoryInfoList[index][3])
        if self.tw_result.item(row, 10):
            self.tw_result.item(row, 10).setText(self.factoryInfoList[index][4])
        return

    #导出至Excel
    def slotOutputToExcel(self):
        if len(self.currentResult) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
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
            alignment.horz = xlwt.Alignment.HORZ_RIGHT
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
            font.name = '黑体'
            font.bold = True
            font.height = 20 * 10  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 2  # 设置为3细实线
            borders.right = 2
            borders.top = 2
            borders.bottom = 2
            headTitleStyle.font = font  # 设定样式
            headTitleStyle.alignment = alignment
            headTitleStyle.borders = borders


            titileStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 10  # 字体大小，11为字号，20为衡量单位
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

            for i in range(19):
                workSheet.col(i).width = 5500
            workSheet.write_merge(0, 1, 0, 0,  '序号',headTitleStyle)
            workSheet.write_merge(0, 0, 1, 7, '调拨单信息', headTitleStyle)
            workSheet.write_merge(0, 0, 8, 10, '交装单位', headTitleStyle)
            workSheet.write_merge(0, 0, 11, 13, '接装单位', headTitleStyle)
            workSheet.write_merge(0, 1, 14, 14, '装备名称', headTitleStyle)
            workSheet.write_merge(0, 1, 15, 15, '计量单位', headTitleStyle)
            workSheet.write_merge(0, 0, 16, 17, '应发数', headTitleStyle)
            workSheet.write_merge(0, 1, 18, 18, '备注', headTitleStyle)
            workSheet.write(1, 1, '调拨单号', headTitleStyle)
            workSheet.write(1, 2, '调拨日期', headTitleStyle)
            workSheet.write(1, 3, '调拨依据', headTitleStyle)
            workSheet.write(1, 4, '调拨性质', headTitleStyle)
            workSheet.write(1, 5, '调拨方式', headTitleStyle)
            workSheet.write(1, 6, '运输方式', headTitleStyle)
            workSheet.write(1, 7, '有效日期', headTitleStyle)
            workSheet.write(1, 8, '单位名称', headTitleStyle)
            workSheet.write(1, 9, '联系人', headTitleStyle)
            workSheet.write(1, 10, '联系电话', headTitleStyle)
            workSheet.write(1, 11, '单位名称', headTitleStyle)
            workSheet.write(1, 12, '联系人', headTitleStyle)
            workSheet.write(1, 13, '联系电话', headTitleStyle)
            workSheet.write(1, 16, '质量', headTitleStyle)
            workSheet.write(1, 17, '数量', headTitleStyle)

            for key in self.currentResult.keys():
                rowList = self.currentResult[key]
                workSheet.write(key + 2, 0, rowList[0], contentStyle)
                workSheet.write(key + 2, 1, rowList[1], contentStyle)
                workSheet.write(key + 2, 2, rowList[2], contentStyle)
                workSheet.write(key + 2, 3, rowList[3], contentStyle)
                workSheet.write(key + 2, 4, rowList[4], contentStyle)
                workSheet.write(key + 2, 5, rowList[5], contentStyle)
                workSheet.write(key + 2, 6, rowList[6], contentStyle)
                workSheet.write(key + 2, 7, rowList[7], contentStyle)
                workSheet.write(key + 2, 8, rowList[9], contentStyle)
                workSheet.write(key + 2, 9, rowList[10], contentStyle)
                workSheet.write(key + 2, 10, rowList[11], contentStyle)
                workSheet.write(key + 2, 11, rowList[12], contentStyle)
                workSheet.write(key + 2, 12, rowList[13], contentStyle)
                workSheet.write(key + 2, 13, rowList[14], contentStyle)
                workSheet.write(key + 2, 14, rowList[16], contentStyle)
                workSheet.write(key + 2, 15, rowList[17], contentStyle)
                workSheet.write(key + 2, 16, rowList[18], contentStyle)
                workSheet.write(key + 2, 17, rowList[19], contentStyle)
                workSheet.write(key + 2, 18, rowList[20], contentStyle)

            try:
                pathName = "%s/%s年陆军调拨单.xls" % (directoryPath, self.currentYear)
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
        pass