from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *

from database.OrderManageSql import ifHaveContSource, selectOneOrderAdjustContData, udpateOrderAdjustContBid, \
    udpateOrderAdjustContSingle
from sysManage.orderManage.selectCont import SelectCont
from widgets.orderManage.Widget_OrderAdjustCont import Widget_OrderAdjustCont
from sysManage.component import getMessageBox


class OrderAdjustCont(QDialog, Widget_OrderAdjustCont):
    signal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(OrderAdjustCont, self).__init__(parent)
        self.setupUi(self)
        self.currentYear = ''
        self.equip_ID = ''
        self.selectCont = SelectCont()
        # 初始化当前界面
        self._initSelf_()
        # 存储当前结果，结构为：{i（行数）：一行数据}
        self.currentResult = {}
        self.signalConnect()


    '''
        初始化当前界面，设置当前查询结果界面为灰
    '''
    def _initSelf_(self):
        self.flagSource = 0
        self.contForm.clear()



    def signalConnect(self):
        self.pb_Save.clicked.connect(self.saveData)


    def saveData(self):
        # 招标
        if self.flagSource == 1:
            data = ['0','0','0','0','','0']
            for i in range(2, 6):
                if self.contForm.cellWidget(0, i).text() == '已完成':
                    data[i-2]='1'
            if self.contForm.cellWidget(0, 6).text() != '设置进度':
                data[4] = self.contForm.cellWidget(0, 6).text()
            if self.contForm.cellWidget(0, 7).text() == '已完成':
                data[5] = '1'
            udpateOrderAdjustContBid(self.equip_ID, data, self.currentYear)
        # 单一来源
        elif self.flagSource == 2:
            data = ['0', '', '0']
            if self.contForm.cellWidget(0, 2).text() == '已完成':
                data[0] = '1'
            if self.contForm.cellWidget(0, 3).text() != '设置进度':
                data[1] = self.contForm.cellWidget(0, 3).text()
            if self.contForm.cellWidget(0, 4).text() == '已完成':
                data[2] = '1'
            print(data)
            udpateOrderAdjustContSingle(self.equip_ID, data, self.currentYear)


    def setYearandEquipID(self, year,Equip_ID):
        self.currentYear = year
        self.equip_ID = Equip_ID
        self.slotSelectResult()

    '''
        查找当前要显示的数据并显示到tablewidget上
    '''
    def slotSelectResult(self):
        if ifHaveContSource(self.equip_ID,self.currentYear) == '招标':
            self.flagSource = 1
            self.contForm.clear()
            contData = selectOneOrderAdjustContData(self.equip_ID, self.currentYear)
            headerlist = ['名称', '合同来源', '确认技术状态', '拟制招标方案', '开评标', '招标结果报批', '签订合同', '交付']
            self.lenHeaderList = len(headerlist)
            self.contForm.setColumnCount(self.lenHeaderList)
            self.contForm.setRowCount(1)
            self.contForm.setHorizontalHeaderLabels(headerlist)
            item = QTableWidgetItem()
            item.setText(contData[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.contForm.setItem(0, 0, item)
            item = QTableWidgetItem()
            item.setText(contData[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.contForm.setItem(0, 1, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setBidCondition)
            if int(contData[7]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 2, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setBidCondition)
            if int(contData[4]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 3, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setBidCondition)
            if int(contData[5]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 4, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setBidCondition)
            if int(contData[6]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 5, item)

            item = QPushButton("设置进度")
            item.clicked.connect(self.makeContract)
            if contData[8] != '':
                item = QPushButton(contData[8])
            self.contForm.setCellWidget(0, 6, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setBidCondition)
            if int(contData[9]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 7, item)
        elif ifHaveContSource(self.equip_ID,self.currentYear) == '单一来源':
            self.flagSource = 2
            self.contForm.clear()
            contData = selectOneOrderAdjustContData(self.equip_ID, self.currentYear)
            headerlist = ['名称', '合同来源', '确认技术状态', '签订合同', '交付']
            self.lenHeaderList = len(headerlist)
            self.contForm.setColumnCount(self.lenHeaderList)
            self.contForm.setRowCount(1)
            self.contForm.setHorizontalHeaderLabels(headerlist)
            item = QTableWidgetItem()
            item.setText(contData[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.contForm.setItem(0, 0, item)
            item = QTableWidgetItem()
            item.setText(contData[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.contForm.setItem(0, 1, item)

            item = QPushButton("设置进度")
            item.clicked.connect(self.setSingleCondition)
            if int(contData[7]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 2, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.makeContract)
            if contData[8] != '':
                item = QPushButton(contData[8])
            self.contForm.setCellWidget(0, 3, item)
            item = QPushButton("设置进度")
            item.clicked.connect(self.setSingleCondition)
            if int(contData[9]):
                item = QPushButton("已完成")
            self.contForm.setCellWidget(0, 4, item)

    def setBidCondition(self):
        if self.flagSource == 1:
            column = self.contForm.currentColumn()
            if column < 0:
                return
            elif 5 >= column >= 2:
                reply = getMessageBox("设置条件", "是否已完成？", True, True)
                if reply == QMessageBox.Ok:
                    item = QPushButton("已完成")
                    self.contForm.setCellWidget(0, column, item)
            elif column == 7:
                data = selectOneOrderAdjustContData(self.equip_ID,self.currentYear)
                flag = True
                for i in range(4,8):
                    if data[i] == '0':
                        flag = False
                        break
                if data[8] == '':
                    flag = False
                if flag:
                    reply = getMessageBox("设置条件", "是否已完成？", True, True)
                    if reply == QMessageBox.Ok:
                        item = QPushButton("已完成")
                        self.contForm.setCellWidget(0, column, item)
                else:
                    getMessageBox("设置条件","存在未完成前置状态，无法设置完成", True, False)
                    return


    def setSingleCondition(self):
        if self.flagSource == 2:
            column = self.contForm.currentColumn()
            if column <0:
                return
            elif column == 2:
                reply = getMessageBox("设置接装条件", "是否具备接装条件？", True, True)
                if reply == QMessageBox.Ok:
                    item = QPushButton("已完成")
                    self.contForm.setCellWidget(0, column, item)
            elif column == 4:
                data = selectOneOrderAdjustContData(self.equip_ID, self.currentYear)
                if data[7] == '0' or data[8] == '':
                    flag = False
                else:
                    flag = True
                if flag:
                    reply = getMessageBox("设置条件", "是否已完成？", True, True)
                    if reply == QMessageBox.Ok:
                        item = QPushButton("已完成")
                        self.contForm.setCellWidget(0, column, item)
                else:
                    getMessageBox("设置条件", "存在未完成前置状态，无法设置完成", True, False)
                    return

    # 合同管理
    def makeContract(self):
        self.selectCont._initSelf_()
        self.selectCont.setYear(self.currentYear)
        self.selectCont.setWindowTitle("合同选择")
        self.selectCont.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.selectCont.show()
        self.selectCont.signal.connect(self.updateCont)

    def updateCont(self):
        txt = self.selectCont.returnNo()
        item = QPushButton(txt)
        self.contForm.setCellWidget(0, self.contForm.currentColumn(), item)