from widgets.alocatMange.select_set import Widget_Dict_Set
import sys
from PyQt5.QtWidgets import QApplication,QWidget, QListWidgetItem, QComboBox, QTableWidgetItem, QDateEdit, \
    QInputDialog,QMessageBox,QAbstractItemView,QTreeWidgetItem
from database.strengthDisturbSql import *
from sysManage.alocatMange.config import ArmyTransferReceiveUnit, ArmyTransferSendUnit
from PyQt5.Qt import Qt
#new
'''
    功能：
        陆军调拨单管理
'''
class alocatDictSet(QWidget, Widget_Dict_Set):
    def __init__(self, parent=None):
        super(alocatDictSet, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()  # 删除单位目录所有数据显示
        self.tw_second.clear()  # 删除装备目录所有数据显示
        self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeUnit = True  # 是否是修改单元的目录

        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)

        self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}
        self.signalConnect()

    '''
        功能：
            所有信号的连接
    '''
    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据

        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 选中当前tablewidget的某行

        self.pb_setUnit.clicked.connect(self.slotUnitDictInit)  # 设置单元目录

        self.pb_setEquip.clicked.connect(self.slotEquipDictInit)  # 设置装备目录

    '''
            功能：
                所有信号的断开
    '''
    def slotDisconnect(self):
        self.pb_add.clicked.disconnect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.disconnect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.disconnect(self.slotDelDict)  # 删除数据

        self.tb_result.itemClicked.disconnect(self.slotClickedRow)  # 选中当前tablewidget的某行

        self.pb_setUnit.clicked.disconnect(self.slotUnitDictInit)  # 设置单元目录

        self.pb_setEquip.clicked.disconnect(self.slotEquipDictInit)  # 设置装备目录

    '''
        功能：
            清除所有数据
    '''
    def delAllData(self):
        self.tw_first.clear()  # 清除单元目录所有数据
        self.tw_second.clear()  # 清除装备目录所有数据
        self.tb_result.clear()  # 清除tableWidget中所有数据
        self.le_first.clear()
        self.le_second.clear()
        self.le_equipID.clear()
        self.le_unitID.clear()
        self.le_unitName.clear()
        self.le_equipName.clear()
        self.le_uperID.clear()

    '''
        功能：
            点击设置单元目录按钮后的初始化
    '''
    def slotUnitDictInit(self):
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)        #设置tablewidget不能修改
        #设置当前控件状态
        self.tw_second.setDisabled(True)     #设置装备目录为灰色
        self.le_second.setDisabled(True)
        self.pb_secondSelect.setDisabled(True)   #设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(False)    #设置单位目录为可选中
        self.le_first.setDisabled(False)
        self.pb_firstSelect.setDisabled(False)
        self.le_equipID.setDisabled(True)
        self.le_equipName.setDisabled(True)
        self.le_uperID.setDisabled(True)
        self.cb_equipType.setDisabled(True)
        self.cb_inputType.setDisabled(True)
        self.le_UnitUper.setDisabled(False)
        self.le_unitName.setDisabled(False)
        self.le_unitID.setDisabled(False)
        self.pb_setEquip.setDisabled(False)
        self.pb_setUnit.setDisabled(True)
        self.pb_add.setDisabled(1)
        self.pb_update.setDisabled(1)

        #从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
        self._initUnitTreeWidget("", self.tw_first)
        self._initUnitTableWidget()

        self.changeUnit = True              #设置当前为修改单位状态

    '''
            功能：
                点击设置装备目录按钮后的初始化
    '''
    def slotEquipDictInit(self):
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置tablewidget不能修改
        # 设置当前控件状态
        self.tw_second.setDisabled(False)  # 设置装备目录为灰色
        self.le_second.setDisabled(False)
        self.pb_secondSelect.setDisabled(False)  # 设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(True)  # 设置单位目录为可选中
        self.le_first.setDisabled(True)
        self.pb_firstSelect.setDisabled(True)
        self.le_equipID.setDisabled(False)
        self.le_equipName.setDisabled(False)
        self.le_uperID.setDisabled(False)
        self.cb_equipType.setDisabled(False)
        self.cb_inputType.setDisabled(False)
        self.le_unitName.setDisabled(True)
        self.le_unitID.setDisabled(True)
        self.pb_setEquip.setDisabled(True)
        self.pb_setUnit.setDisabled(False)
        self.le_UnitUper.setDisabled(True)
        self.pb_add.setDisabled(0)
        self.pb_update.setDisabled(0)

        # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
        self._initEquipTreeWidget("", self.tw_second)
        self._initEquipTableWidget()

        self.changeUnit = False  # 设置当前为修改单位状态

    '''
        功能：
            单位目录的初始化，显示整个单位表
            参数表：root为上级单位名字，mother为上级节点对象
    '''
    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectDisturbPlanUnitInfoByDeptUper('')
        else:
            result = selectDisturbPlanUnitInfoByDeptUper(root)

        #rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.first_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    '''
        功能：
            设置单元时的初始化tableWidget，显示整个单位表
    '''
    def _initUnitTableWidget(self):
        result = selectAllDataAboutDisturbPlanUnit()

        header = ['单位编号', '单位名称', '上级单位编号','单位别名']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)
            item = QTableWidgetItem(data[3])
            self.tb_result.setItem(i, 3, item)

        # print(result)   #测试查找到的数据

    '''
        功能：
            装备目录的初始化，显示整个装备表
            参数表：root为上级装备名字，mother为上级节点对象
    '''
    def _initEquipTreeWidget(self, root, mother):
        if root == '':
            result = selectEquipInfoByEquipUper('')
        else:
            result = selectEquipInfoByEquipUper(root)

        #rowData: (装备编号，装备名称，上级装备编号, 录入类型, 装备类型)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.second_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initEquipTreeWidget(rowData[0], item)

    '''
        功能：
            设置装备时的初始化tableWidget，显示整个装备表
    '''
    def _initEquipTableWidget(self):
        result = selectAllDataAboutEquip()

        header = ['装备编号', '装备名称', '上级装备编号', '录入类型', '装备类型']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)
            item = QTableWidgetItem(data[3])
            self.tb_result.setItem(i, 3, item)
            item = QTableWidgetItem(data[4])
            self.tb_result.setItem(i, 4, item)

        # print(result)   #测试查找到的数据

    '''
        功能：
            当选中tablewidget某行时，显示对应的lineedit
    '''
    def slotClickedRow(self):

        currentRow = self.tb_result.currentRow()
        if self.changeUnit:
            self.le_unitID.setText(self.tb_result.item(currentRow, 0).text())
            self.le_unitName.setText(self.tb_result.item(currentRow, 1).text())
            self.le_UnitUper.setText(self.tb_result.item(currentRow, 2).text())
        else:
            self.le_equipID.setText((self.tb_result.item(currentRow,0).text()))
            self.le_equipName.setText((self.tb_result.item(currentRow, 1).text()))
            self.le_uperID.setText((self.tb_result.item(currentRow, 2).text()))
            inputType = self.tb_result.item(currentRow, 3).text()
            equipType = self.tb_result.item(currentRow, 4).text()

            if inputType == '空':
                self.cb_inputType.setCurrentIndex(0)
            elif inputType == '逐号录入':
                self.cb_inputType.setCurrentIndex(1)
            else:
                self.cb_inputType.setCurrentIndex(2)

            if equipType == '空':
                self.cb_equipType.setCurrentIndex(0)
            elif equipType == '通用装备':
                self.cb_equipType.setCurrentIndex(1)
            else:
                self.cb_equipType.setCurrentIndex(2)

    '''
        功能：
            添加目录
    '''
    def slotAddDict(self):
        # 单位目录
        if self.changeUnit:
            pass
        #     if self.le_unitID.text() == "" or self.le_unitName.text() == "":
        #         reply = QMessageBox.question(self, '新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', QMessageBox.Yes,
        #                                      QMessageBox.Cancel)
        #     else:
        #         Unit_ID = self.le_unitID.text()
        #         Unit_Name = self.le_unitName.text()
        #         Unit_Uper = self.le_unitUper.text()
        #         unitInfoTuple = selectAllDataAboutDisturbPlanUnit()
        #
        #         haveID = False
        #         haveUperID = False
        #         if Unit_Uper == '':
        #             haveUperID = True
        #
        #         for unitInfo in unitInfoTuple:
        #             if Unit_ID == unitInfo[0]:
        #                 reply = QMessageBox.question(self, '新增失败', '单位ID已存在, 请重新填写', QMessageBox.Yes,
        #                                              QMessageBox.Cancel)
        #                 haveID = True
        #                 break
        #             elif Unit_Uper == unitInfo[0]:
        #                 haveUperID = True
        #
        #         if haveUperID == False:
        #             reply = QMessageBox.question(self, '新增失败', '上级单位ID不存在, 请重新填写', QMessageBox.Yes,
        #                                          QMessageBox.Cancel)
        #         elif haveUperID == True and haveID == False:
        #             addDataIntoDisturbPlanUnit(Unit_ID, Unit_Name, Unit_Uper)
        #
        #         self.slotUnitDictInit()
        # 装备目录
        else:
            if self.le_equipID.text() == "" or self.le_equipName.text() == "":
                reply = QMessageBox.question(self, '新增失败', '装备ID或装备名字为空，拒绝增加，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.le_uperID.text()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                equipInfoTuple = selectAllDataAboutEquip()

                haveID = False
                haveUperID = False
                if Equip_Uper == '':
                    haveUperID = True

                for equipInfo in equipInfoTuple:
                    if Equip_ID == equipInfo[0]:
                        reply = QMessageBox.question(self, '新增失败', '装备ID已存在, 请重新填写', QMessageBox.Yes,
                                                     QMessageBox.Cancel)
                        haveID = True
                        break
                    elif Equip_Uper == equipInfo[0]:
                        haveUperID = True

                if haveUperID == False:
                    reply = QMessageBox.question(self, '新增失败', '上级装备ID不存在, 请重新填写', QMessageBox.Yes,
                                                 QMessageBox.Cancel)
                elif haveUperID == True and haveID == False:
                    addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type)
                self.slotEquipDictInit()

    '''
        功能：
            修改目录
    '''
    def slotUpdate(self):
        # 单位目录
        if self.changeUnit:
            pass
            # if (self.tb_result.item(self.tb_result.currentRow(),
            #                         0).text() != self.le_unitID.text()) or self.le_unitName.text() == "":
            #     reply = QMessageBox.question(self, '修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
            #                                  QMessageBox.Cancel)
            # else:
            #     Unit_ID = self.le_unitID.text()
            #     Unit_Name = self.le_unitName.text()
            #     Unit_Uper = self.le_unitUper.text()
            #     unitInfoTuple = selectAllDataAboutDisturbPlanUnit()
            #     haveUperID = False
            #
            #     if Unit_Uper == '':
            #         haveUperID = True
            #
            #     for unitInfo in unitInfoTuple:
            #         if Unit_Uper == unitInfo[0]:
            #             haveUperID = True
            #
            #     if haveUperID == False:
            #         reply = QMessageBox.question(self, '修改失败', '上级单位ID在单位列表中不存在，拒绝修改，请重新填写', QMessageBox.Yes,
            #                                      QMessageBox.Cancel)
            #     else:
            #         updateDataIntoDisturbPlanUnit(Unit_ID, Unit_Name, Unit_Uper)
            #         self.slotUnitDictInit()
        # 装备目录
        else:
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_equipID.text()) or self.le_equipName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '装备ID不能修改或装备名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.le_uperID.text()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                haveUperID = False
                equipInfoTuple = selectAllDataAboutEquip()
                for equipInfo in equipInfoTuple:
                    if Equip_Uper == equipInfo[0]:
                        haveUperID = True

                if haveUperID == False:
                    reply = QMessageBox.question(self, '修改失败', '上级装备ID在装备列表中不存在，拒绝修改，请重新填写', QMessageBox.Yes,
                                                 QMessageBox.Cancel)
                else:
                    updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type)
                    self.slotEquipDictInit()

    '''
        功能：
            删除目录
    '''

    def slotDelDict(self):
        # 单位目录
        if self.changeUnit:
            reply = QMessageBox.question(self, '删除', '是否将下级单位以及所涉及的其他表关于该单位的信息一起删除？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delDataInDisturbPlanUnit(self.le_unitID.text())
                reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                self.slotUnitDictInit()

            else:
                reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
        #装备目录
        else:
            reply = QMessageBox.question(self, '删除', '是否将下级装备以及所涉及的其他表关于该装备的信息一起删除？', QMessageBox.Yes,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delDataInEquip(self.le_equipID.text())
                reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                self.slotEquipDictInit()
            else:
                reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)

'''
    功能：
        单元测试
'''