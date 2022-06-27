import base64
import pickle
from PyQt5.QtCore import Qt, QDate, QDateTime, pyqtSlot
from database.contractManagementSql import getContractMaintenanceInfoByNo
from database.contractSigningSql import *
from sysManage.maintainSupport.MaintenanceContractSignTransferModel import MaintenanceContractSignTransferModel

from sysManage.userInfo import get_value
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QFileDialog, QDateEdit, QCheckBox, QPushButton

from widgets.serviceSupport.maintenanceContractSigningUI import MaintenanceContractSigningUI


class MaintenanceContractSigning(QWidget, MaintenanceContractSigningUI):
    def __init__(self, parent=None):
        super(MaintenanceContractSigning, self).__init__(parent)
        self.setupUi(self)
        self.startInfo = None
        self.infoDict = {}
        self.init()
        self.shutdown = True
        self.deleteSilence = False

    result = []
    contactNo = ''
    bureauName = ''
    currentLastRow = 0

    # 信号和槽连接
    def signalConnection(self):
        self.pb_select.clicked.connect(self.slotSelect)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        
        self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)


    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    # 信号和槽断开
    def slotDisconnect(self):
        pass

    # 定义初始化函数
    def init(self):
        self.initUserInfo()
        if self.userInfo:
            from database.strengthDisturbSql import selectUnitInfoByUnitID
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        self.signalConnection()
        self.displayData()
        pass




    '''
        功能：
            根据下拉列表框以及文本框的内容，筛选数据。
    '''

    def slotSelect(self):
        self.pb_select.disconnect()
        if len(self.le_contactNo.text()) > 0:
            self.contactNo = self.le_contactNo.text()
        else:
            self.contactNo = ''
        if len(self.le_Unit.text()) > 0:
            self.bureauName = self.le_Unit.text()
        else:
            self.bureauName = ''
        self.displayData()
        self.pb_select.clicked.connect(self.slotSelect)


    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.result = getResult(self.contactNo, self.bureauName)
        self.tw_result.clear()
        self.tw_result.setColumnCount(31)
        dataList = self.result
        if dataList is None or len(dataList) == 0:
            self.tw_result.setRowCount(3)
            self.initTableHeader()
        else:
            self.tw_result.setRowCount(3 + len(dataList))
            self.initTableHeader()
            for i in range(len(dataList)):
                contactInfo = getContractMaintenanceInfoByNo(dataList[i][4])
                item = QTableWidgetItem(str(i + 1))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 0, item)

                bureauNames = getBureauNamesFromAgentRoom()
                item = QComboBox()
                item.setEditable(False)
                itemElement = [dataList[i][1]]
                if len(bureauNames) > 0:
                    for j in range(len(bureauNames)):
                        if bureauNames[j][0] != dataList[i][1]:
                            itemElement.append(bureauNames[j][0])
                item.addItems(itemElement)
                item.setCurrentIndex(0)
                self.tw_result.setCellWidget(3 + i, 1, item)
                item.activated.connect(self.bureauNameChange)

                agentIds, agentNames = getAgentNamesAndIds(dataList[i][1])
                # print("agentIds:" ,agentIds)
                # print("agentNames:", agentNames)
                combox = QComboBox()
                for j in range(len(agentNames)):
                    combox.addItem(agentNames[j], agentIds[j])
                    if agentIds[j] == dataList[i][3]:
                        combox.setCurrentIndex(j)
                combox.setEditable(False)
                self.tw_result.setCellWidget(3 + i, 2, combox)
                combox.activated.connect(self.slotAlterAndSava)

                #合同乙方
                item = QTableWidgetItem(contactInfo[5])
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 3, item)

                #合同号
                print('dataList-i',dataList[i])
                item = QTableWidgetItem(dataList[i][4])
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 4, item)

                #价格批复件
                item = QTableWidgetItem(dataList[i][5])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 5, item)

                #价格情况合同
                item = QTableWidgetItem(dataList[i][6])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 6, item)

                #价格工作依据
                item = QTableWidgetItem(dataList[i][7])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 7, item)

                #进度
                item = QTableWidgetItem(dataList[i][8])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 8, item)

                #价格方案依据
                item = QTableWidgetItem(dataList[i][9])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 9, item)

                #合同签订时间
                item = QTableWidgetItem(contactInfo[-3])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3 + i, 10, item)

                # 交付签订时间
                item = QTableWidgetItem(contactInfo[-2])
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 11, item)

                #合同名称
                item = QTableWidgetItem(contactInfo[3])
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 12, item)

                #送修单位
                if len(getAllocationByContractNo(contactInfo[2])) > 0:
                    allocationUnit = getAllocationByContractNo(contactInfo[2])[0][0]
                else:
                    allocationUnit = ''
                item = QTableWidgetItem(allocationUnit)
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 13, item)

                #总体进度
                item = QTableWidgetItem(dataList[i][10])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 14, item)

                #计划年度
                item = QTableWidgetItem(dataList[i][11])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 15, item)

                #数量计划
                item = QTableWidgetItem(dataList[i][12])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 16, item)

                # 数量明细
                item = QTableWidgetItem(dataList[i][13])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 17, item)

                # 计划价格单价
                item = QTableWidgetItem(dataList[i][14])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 18, item)

                # 计划价格单价
                item = QTableWidgetItem(dataList[i][15])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 19, item)

                # 报价单位
                item = QTableWidgetItem(dataList[i][16])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 20, item)

                # 报价金额
                item = QTableWidgetItem(dataList[i][17])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 21, item)

                # 合同单价
                item = QTableWidgetItem(str(contactInfo[-6]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3 + i, 22, item)

                # 合同金额
                item = QTableWidgetItem(str(contactInfo[-4]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3 + i, 23, item)

                #已支付金额
                item = QTableWidgetItem(str(dataList[i][18]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 24, item)

                #待支付金额
                item = QTableWidgetItem(str(dataList[i][19]))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 25, item)

                # 目前进度
                item = QTableWidgetItem(str(dataList[i][20]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 26, item)

                # 是否入库
                item = QComboBox()
                if dataList[i][21] == 1:
                    itemElement = ['是', '否']
                else:
                    itemElement = ['否', '是']
                item.addItems(itemElement)
                self.tw_result.setCellWidget(3 + i, 27, item)
                item.activated.connect(self.slotAlterAndSava)
                #开具调拨单
                item = QPushButton()
                item.setText('开具调拨单')
                if dataList[i][22] == 1:
                    item.setEnabled(False)
                self.tw_result.setCellWidget(3 + i, 28, item)
                item.clicked.connect(self.formDialOrder)
                item.clicked.connect(self.slotAlterAndSava)

                # 完成调拨
                item = QComboBox()
                if dataList[i][23] == 1:
                    itemElement = ['是']
                    item.setEnabled(True)
                else:
                    itemElement = ['否', '是']
                item.addItems(itemElement)
                self.tw_result.setCellWidget(3 + i, 29, item)
                item.activated.connect(self.slotAlterAndSava)

                # 备注
                item = QTableWidgetItem(dataList[i][24])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 30, item)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)


    def bureauNameChange(self):
        currentRow = self.tw_result.currentIndex().row()
        item = self.tw_result.cellWidget(currentRow, 1)
        if item != None:
            item.activated.disconnect(self.bureauNameChange)
            agentNameCombox = self.tw_result.cellWidget(currentRow, 2)
            currentBureauName = item.currentText()
            agentIds, agentNames = getAgentNamesAndIds(currentBureauName)
            agentNameCombox.clear()
            for i in range(len(agentNames)):
                agentNameCombox.addItem(agentNames[i], agentIds[i])
            item.activated.connect(self.bureauNameChange)



    #开具调拨单
    def formDialOrder(self):
        ShowRocket = MaintenanceContractSignTransferModel()
        ShowRocket.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        ShowRocket.pb_output.setDisabled(1)
        ShowRocket.pb_input.setDisabled(1)
        ShowRocket.pb_confirm.setDisabled(1)
        ShowRocket.pb_saveSingle.setDisabled(1)
        ShowRocket.pb_saveTotal.setDisabled(1)
        ShowRocket.getUnitIDList([['', '', '', '' ], ['','', '', ''],['', '', '', '' ]], ['', '', '', '', '', ''],'',('', "", '', '', '', '', ''))
        ShowRocket.show()
        ShowRocket.exec_()

        basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        sourceDirectoryPath = basepath + "\\resource\\装备实物资产调拨回执凭证.docx"
        print('sourceDirectoryPath')
        print(sourceDirectoryPath)
        savaDirectoryPath = QFileDialog.getExistingDirectory(self, "请选择调拨单保存目录", "c:/")
        if len(savaDirectoryPath) > 0:
            try:
                savaDirectoryPath = savaDirectoryPath + "\\装备实物资产调拨回执凭证.docx"
                with open(sourceDirectoryPath, "rb") as source_file:
                    with open(savaDirectoryPath, "wb") as aim_file:
                        while True:
                            data = source_file.read(1024)
                            if data:
                                aim_file.write(data)
                            else:
                                # count += 1
                                # self.progerss.setValue(count)
                                break
                import win32api
                win32api.ShellExecute(0, 'open', savaDirectoryPath, '', '', 1)
                currentRow = self.tw_result.currentIndex().row()
                item = self.tw_result.cellWidget(currentRow, 28)
                if item != None:
                    item.setEnabled(False)
            except Exception as e:
                print(e)
                QMessageBox.about(self, "开具调拨单失败！", "请检查文件名是否正确、文件是否已存在、是否安装word或word正在被占用！")
                return
    '''
        功能：
            画表头,行数至少有3行
    '''

    def initTableHeader(self):
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        #self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()

        # 绘制表头
        item = QTableWidgetItem("装备维修合同签订情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 0, 1, 31)

        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 0, 2, 1)

        item = QTableWidgetItem("分管军代表机构")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 1, 1, 2)

        item = QTableWidgetItem("军代局")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 1, item)

        item = QTableWidgetItem("军代室")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 2, item)

        item = QTableWidgetItem("承制单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 2, 1)

        item = QTableWidgetItem("批准合同号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        self.tw_result.setSpan(1, 4, 2, 1)

        item = QTableWidgetItem("价格批复件")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)
        self.tw_result.setSpan(1, 5, 2, 1)

        item = QTableWidgetItem("价格情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)
        self.tw_result.setSpan(1, 6, 1, 4)

        item = QTableWidgetItem("合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 6, item)
        item = QTableWidgetItem("价格工作依据")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 7, item)
        item = QTableWidgetItem("进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 8, item)
        item = QTableWidgetItem("价格方案依据")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 9, item)

        item = QTableWidgetItem("合同签订时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)
        self.tw_result.setSpan(1, 10, 2, 1)

        item = QTableWidgetItem("交付时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)
        self.tw_result.setSpan(1, 11, 2, 1)

        item = QTableWidgetItem("合同项目")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)
        self.tw_result.setSpan(1, 12, 1, 2)

        item = QTableWidgetItem("合同名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 12, item)

        item = QTableWidgetItem("送修单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 13, item)

        item = QTableWidgetItem("总进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 14, item)
        self.tw_result.setSpan(1, 14, 2, 1)

        item = QTableWidgetItem("计划年度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 15, item)
        self.tw_result.setSpan(1, 15, 2, 1)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 16, item)
        self.tw_result.setSpan(1, 16, 1, 2)

        item = QTableWidgetItem("计划")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 16, item)
        item = QTableWidgetItem("明细")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 17, item)

        item = QTableWidgetItem("计划价格")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 18, item)
        self.tw_result.setSpan(1, 18, 1, 2)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 18, item)
        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 19, item)

        item = QTableWidgetItem("报价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 20, item)
        self.tw_result.setSpan(1, 20, 1, 2)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 20, item)
        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 21, item)

        item = QTableWidgetItem("合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 22, item)
        self.tw_result.setSpan(1, 22, 1, 2)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 22, item)
        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 23, item)

        item = QTableWidgetItem("已支付金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 24, item)
        self.tw_result.setSpan(1, 24, 2, 1)

        item = QTableWidgetItem("待支付金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 25, item)
        self.tw_result.setSpan(1, 25, 2, 1)

        item = QTableWidgetItem("目前进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 26, item)
        self.tw_result.setSpan(1, 26, 2, 1)

        item = QTableWidgetItem("是否入库")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 27, item)
        self.tw_result.setSpan(1, 27, 2, 1)

        item = QTableWidgetItem("调拨情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 28, item)
        self.tw_result.setSpan(1, 28, 1, 2)

        item = QTableWidgetItem("开具调拨单")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 28, item)
        item = QTableWidgetItem("完成接装")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 29, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 30, item)
        self.tw_result.setSpan(1, 30, 2, 1)
    '''
        功能：
            新增一行的数据
    '''

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) > 0:
            currentRow = selectRow[0].row()
        else:
            currentRow = self.tw_result.currentIndex().row()
        if self.shutdown:
            return
        if self.checkData(currentRow):
            print('currentRow',currentRow)
            print('currentLastRow',self.currentLastRow)
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            elif currentRow > 2:
                self.alterRowData(currentRow)
        else:
            return

    def checkData(self,row):
        if row < 3:
            return False
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        
        checkColomns = [20, 21, 22, 23, 24]
        for i in range(len(checkColomns)):
            item = self.tw_result.item(row, checkColomns[i])
            if item != None:
                text = item.text()
                from utills.CommomHelper import CommonHelper
                if len(text) > 0 and CommonHelper.isNumber(text):
                    continue
                else:
                    item.setText('')
                    self.tw_result.itemChanged.connect(self.slotAlterAndSava)
                    return False
            else:
                self.tw_result.itemChanged.connect(self.slotAlterAndSava)
                return False
        contractMoney = float(self.tw_result.item(row,checkColomns[-2]).text())
        paidMoney = float(self.tw_result.item(row,checkColomns[-1]).text())
        dueMonet = contractMoney - paidMoney
        self.tw_result.item(row, 25).setText(str(dueMonet))
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        return True

    def savaRowData(self, row):
        print('保存一行')
        rowData = []
        for i in range(1, self.tw_result.columnCount()):
            if i == 1 or i == 2 or i == 4 or i == 27 or i == 28 or i == 29:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    if i == 1 or i == 4:
                        rowData.append(item.currentText())
                    elif i == 2:
                        rowData.append(item.currentText())
                        rowData.append(item.currentData())
                    elif i == 27:
                        if item.currentText() == '是':
                            rowData.append(1)
                        else:
                            rowData.append(0)
                    elif i == 28:
                        if item.isEnabled() == True:
                            rowData.append(0)
                        else:
                            rowData.append(1)
                    elif i == 29:
                        if item.currentText() == '是':
                            rowData.append(1)
                        else:
                            rowData.append(0)
                else:
                    print('item', item)
                    print('colomn',i)
                    return
            elif i == 5 or i == 6 or i == 7 or i == 8 or i == 9 or i == 14 or  i == 15 or i == 16 or i == 17 or i == 18 or i== 19 or i == 20 or i == 21 or i == 24 or i == 25 or i == 26 or  i == 30:
                item = self.tw_result.item(row, i)
                if item != None:
                    rowData.append(item.text())
                else:
                    print('item', item)
                    return
            else:
                continue
        print('rowData',rowData)
        print('length', len(rowData))
        if len(rowData) < 24:
            return
        else:
            insertOneDataIntContactSign(rowData)
            self.currentLastRow = -1
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def alterRowData(self, row):
        print("修改一行数据")
        rowData = []
        rowData.append(self.result[row - 3][0])
        for i in range(1,self.tw_result.columnCount()):
            if i == 1 or i == 2 or i == 27 or i == 28 or i == 29:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    if i == 1:
                        rowData.append(item.currentText())
                    elif i == 2:
                        rowData.append(item.currentText())
                        rowData.append(item.currentData())
                    elif i == 27:
                        if item.currentText() == '是':
                            rowData.append(1)
                        else:
                            rowData.append(0)
                    elif i == 28:
                        if item.isEnabled() == True:
                            rowData.append(0)
                        else:
                            rowData.append(1)
                    elif i == 29:
                        if item.currentText() == '是':
                            rowData.append(1)
                        else:
                            rowData.append(0)
                else:
                    return
            elif i == 4 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9 or i == 14 or i == 15 or i == 16 or i == 17 or i == 18 or i == 19 or i == 20 or i == 21 or i == 24 or i == 25 or i == 26 or i == 30:
                item = self.tw_result.item(row, i)
                if item != None:
                    rowData.append(item.text())
                else:
                    return
            else:
                continue
        print(rowData)
        print(len(rowData))
        if len(rowData) < 25:
            return
        else:
            if (updataOneDataIntoContractSign(rowData) == True):
                QMessageBox.warning(self, "修改成功", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "修改失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()


    '''
        功能：
            新增按钮槽函数
    '''

    @pyqtSlot()
    def slotAdd(self):
        print('SlotAdd')
        self.tb_add.disconnect()
        self.shutdown = True
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        if self.tw_result.rowCount() <= 3 + len(self.result):
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            print("rowCount: ", rowCount)
            print("3 + result: ", 3 + len(self.result))
            print(self.result)
            self.tw_result.insertRow(rowCount)

            if (rowCount + 1 == 4):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3, 0, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1, 0).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)
            bureauNames = getBureauNamesFromAgentRoom()
            item = QComboBox()
            item.setEditable(False)
            itemElement = []
            if len(bureauNames) > 0:
                for j in range(len(bureauNames)):
                    itemElement.append(bureauNames[j][0])
            item.addItems(itemElement)
            self.tw_result.setCellWidget(rowCount, 1, item)
            item.activated.connect(self.bureauNameChange)

            item = QComboBox()
            if len(bureauNames) > 0:
                agentIds, agentNames = getAgentNamesAndIds(itemElement[0])
                for i in range(len(agentNames)):
                    item.addItem(agentNames[i], agentIds[i])
                item.setEditable(False)
            self.tw_result.setCellWidget(rowCount, 2, item)

            contractNos = getContractNos()
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            if len(contractNos) > 0:
                contractInfo = getContractMaintenanceInfoByNo(contractNos[0])
                if len(contractNos) > 0:
                    item.setText(contractInfo[5])
            self.tw_result.setItem(rowCount, 3, item)

            item = QComboBox()
            item.setEditable(False)
            item.addItems(contractNos)
            self.tw_result.setCellWidget(rowCount, 4, item)
            item.activated.connect(self.contactNoChange)
            allocationUnit = []
            if len(contractNos) > 0:
                allocationUnit = getAllocationByContractNo(contractNos[0])
            if len(allocationUnit) > 0:
                item = QTableWidgetItem(allocationUnit[0][0])
            else:
                item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 13, item)
            contractInfo = []
            if len(contractNos) > 0:
                contractInfo = getContractMaintenanceInfoByNo(contractNos[0])
            self.setContractInfo(contractInfo, rowCount)
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 25, item)
            item = QComboBox()
            item.setEditable(False)
            item.addItems(['否', '是'])
            self.tw_result.setCellWidget(rowCount, 27, item)
            # 开具调拨单
            item = QPushButton()
            item.setText('开具调拨单')
            self.tw_result.setCellWidget(rowCount, 28, item)
            item.clicked.connect(self.formDialOrder)
            item = QComboBox()
            item.setEditable(False)
            item.addItems(['否', '是'])
            self.tw_result.setCellWidget(rowCount, 29, item)
        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes)
        self.tb_add.clicked.connect(self.slotAdd)
        self.shutdown = False
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)



    def contactNoChange(self):
        currentRow = self.tw_result.currentIndex().row()
        item = self.tw_result.cellWidget(currentRow, 4)
        if item != None:
            contractNo = item.currentText()
            contractInfo = getContractMaintenanceInfoByNo(contractNo)
            self.setContractInfo(contractInfo, currentRow)

    def setContractInfo(self,contractInfo, row):
        columns = [3, 10, 11, 12, 22, 23]
        if len(contractInfo) == 0:
            for i in range(len(columns)):
                item = QTableWidgetItem('')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(row, columns[i], item)
        else:
            infos = [contractInfo[5], contractInfo[-3], contractInfo[-2], contractInfo[3], str(contractInfo[6]), str(contractInfo[-4])]
            for i in range(len(columns)):
                item = QTableWidgetItem(infos[i])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(row, columns[i], item)


    @pyqtSlot()
    def slotDelete(self):
        self.tb_del.disconnect()
        if self.deleteSilence == True:
            return
        self.deleteSilence = True
        rowCount = self.tw_result.currentRow()
        if self.result == None:
            resultCount = 0
        else:
            resultCount = len(self.result)

        if rowCount < 3:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
        elif rowCount >= 3 and rowCount < 3 + resultCount:
            reply = QMessageBox.question(self, '警告', '是否删除该行数据？', QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                deleteDataByContractSignId(self.result[rowCount - 3][0])
                self.tw_result.removeRow(rowCount)
                self.displayData()
            else:
                self.deleteSilence = False
                self.tb_del.clicked.connect(self.slotDelete)
                return
        else:
            self.tw_result.removeRow(rowCount)
        self.deleteSilence = False
        self.tb_del.clicked.connect(self.slotDelete)


    #导出至Excel
    def slotOutputToExcel(self):
        self.tb_outputToExcel.disconnect()

        if len(self.result) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            self.displayData()
            return
        self.displayData()
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
            for i in range(13):
                workSheet.col(i).width = 5000
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

            workSheet.write_merge(0, 0, 0, 30, "装备维修合同签订情况",titileStyle)
            workSheet.write_merge(1, 2, 0, 0,'序号', titileStyle)
            workSheet.write_merge(1, 1, 1, 2, '分管军代机构', titileStyle)
            workSheet.write(2, 1, "军代局", titileStyle)
            workSheet.write(2, 2, "军代室", titileStyle)
            workSheet.write_merge(1, 2, 3, 3, '承制单位', titileStyle)
            workSheet.write_merge(1, 2, 4, 4, '批准的合同号', titileStyle)
            workSheet.write_merge(1, 2, 5, 5, '价格批复件', titileStyle)
            workSheet.write_merge(1, 1, 6, 9, '价格情况', titileStyle)
            workSheet.write(2, 6, "合同", titileStyle)
            workSheet.write(2, 7, "价格工作依据", titileStyle)
            workSheet.write(2, 8, "进度", titileStyle)
            workSheet.write(2, 9, "价格方案依据", titileStyle)
            workSheet.write_merge(1, 2, 10, 10, '合同签订时间', titileStyle)
            workSheet.write_merge(1, 2, 11, 11, '交付时间', titileStyle)
            workSheet.write_merge(1, 1, 12, 13, '合同项目', titileStyle)
            workSheet.write(2, 12, "合同名称", titileStyle)
            workSheet.write(2, 13, "送修单位", titileStyle)
            workSheet.write_merge(1, 2, 14, 14, '总体进度', titileStyle)
            workSheet.write_merge(1, 2, 15, 15, '计划年度', titileStyle)
            workSheet.write_merge(1, 1, 16, 17, '数量', titileStyle)
            workSheet.write(2, 16, "计划", titileStyle)
            workSheet.write(2, 17, "明细", titileStyle)
            workSheet.write_merge(1, 1, 18, 19, '计划价格', titileStyle)
            workSheet.write(2, 18, "单价", titileStyle)
            workSheet.write(2, 19, "金额", titileStyle)
            workSheet.write_merge(1, 1, 20, 21, '报价', titileStyle)
            workSheet.write(2, 20, "单价", titileStyle)
            workSheet.write(2, 21, "金额", titileStyle)
            workSheet.write_merge(1, 1, 22, 23, '合同', titileStyle)
            workSheet.write(2, 22, "单价", titileStyle)
            workSheet.write(2, 23, "金额", titileStyle)
            workSheet.write_merge(1, 2, 24, 24, '已支付金额', titileStyle)
            workSheet.write_merge(1, 2, 25, 25, '待支付金额', titileStyle)
            workSheet.write_merge(1, 2, 26, 26, '目前进度', titileStyle)
            workSheet.write_merge(1, 2, 27, 27, '是否入库', titileStyle)
            workSheet.write_merge(1, 1, 28, 29, '调拨情况', titileStyle)
            workSheet.write(2, 28, "开具调拨单", titileStyle)
            workSheet.write(2, 29, "完成装接", titileStyle)
            workSheet.write_merge(1, 2, 30, 30, '调拨情况', titileStyle)




            #填表数据
            dataList = self.result
            if dataList is None or len(dataList) == 0:
                return
            else:
                for i in range(len(dataList)):

                    contactInfo = getContractMaintenanceInfoByNo(dataList[i][4])
                    workSheet.write(3 + i, 0, str(i + 1), contentStyle)
                    workSheet.write(3 + i, 1, dataList[i][1], contentStyle)
                    workSheet.write(3 + i, 2, dataList[i][2], contentStyle)
                    workSheet.write(3 + i, 3, contactInfo[5], contentStyle)
                    workSheet.write(3 + i, 4, dataList[i][4], contentStyle)
                    workSheet.write(3 + i, 5, dataList[i][5], contentStyle)
                    workSheet.write(3 + i, 6, dataList[i][6], contentStyle)
                    workSheet.write(3 + i, 7, dataList[i][7], contentStyle)
                    workSheet.write(3 + i, 8, dataList[i][8], contentStyle)
                    workSheet.write(3 + i, 9, dataList[i][9], contentStyle)
                    workSheet.write(3 + i, 10, contactInfo[-3], contentStyle)
                    workSheet.write(3 + i, 11, contactInfo[-2], contentStyle)
                    workSheet.write(3 + i, 12, contactInfo[3], contentStyle)
                    # 送修单位
                    allocationUnit = getAllocationByContractNo(contactInfo[2])[0][0]
                    workSheet.write(3 + i, 13, allocationUnit, contentStyle)
                    workSheet.write(3 + i, 14, dataList[i][10], contentStyle)
                    workSheet.write(3 + i, 15, dataList[i][11], contentStyle)
                    workSheet.write(3 + i, 16, dataList[i][12], contentStyle)
                    workSheet.write(3 + i, 17, dataList[i][13], contentStyle)
                    workSheet.write(3 + i, 18, dataList[i][14], contentStyle)
                    workSheet.write(3 + i, 19, dataList[i][15], contentStyle)
                    workSheet.write(3 + i, 20, dataList[i][16], contentStyle)
                    workSheet.write(3 + i, 21, dataList[i][17], contentStyle)
                    workSheet.write(3 + i, 22, str(contactInfo[-6]), contentStyle)
                    workSheet.write(3 + i, 23, str(contactInfo[-4]), contentStyle)
                    workSheet.write(3 + i, 24, str(dataList[i][18]), contentStyle)
                    workSheet.write(3 + i, 25, str(dataList[i][19]), contentStyle)
                    workSheet.write(3 + i, 26, str(dataList[i][20]), contentStyle)
                    if dataList[i][21] == 1:
                        workSheet.write(3 + i, 27, '是', contentStyle)
                    else:
                        workSheet.write(3 + i, 27, '否', contentStyle)
                    if dataList[i][22] == 1:
                        workSheet.write(3 + i, 28, '是', contentStyle)
                    else:
                        workSheet.write(3 + i, 28, '否', contentStyle)

                    if dataList[i][23] == 1:
                        workSheet.write(3 + i, 29, '是', contentStyle)
                    else:
                        workSheet.write(3 + i, 29, '否', contentStyle)
                    workSheet.write(3 + i, 30, dataList[i][24], contentStyle)

            try:
                pathName = "%s/装备维修合同签订情况.xls" % (directoryPath)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return
        self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)

if __name__ == "__main__":
    arr = ['1dads','2','3',[2]]
    with open("test.nms","wb") as file:
        pickle.dump(arr,file)

    with open("test.nms","rb") as file:
        arr1 = pickle.load(file)
    print(arr1)

