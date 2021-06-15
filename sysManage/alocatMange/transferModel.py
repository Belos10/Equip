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
            self.slotClickedOutput()
            self.signal.emit('1')

    def setCurrentYear(self, year):
        self.currentYear = year

    def getUnitIDList(self, unitInfoList, equipInfo, year, requireInfo):
        if unitInfoList == "" and equipInfo =="" and  year =="" and  requireInfo == "":
            self.pb_input.setDisabled(True)
            self.pb_output.setDisabled(True)
            self.pb_saveTotal.setDisabled(True)
            self.pb_saveSingle.setDisabled(True)
            self.pb_confirm.setDisabled(True)
            return
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
        self.totalModel = totalModel()
        self.totalModel.initTableWidget(self.unitInfoList, self.equipInfo, self.year, self.requireInfo)
        self.tw_transferModel.addTab(self.totalModel, "总单")
        for unitInfo, num in zip(unitInfoList, requireInfo[2: -2]):
            if num == "" or num == "0":
                continue
            page = singleModel()
            self.tw_transferModel.addTab(page, unitInfo[0])
            self.currentSingelUnitPage[unitInfo[0]] = page
            page.initTableWidget(unitInfo, self.equipInfo,self.year)

    def slotClickedOutput(self):
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            import xlwt
            workBook = xlwt.Workbook(encoding='utf-8')
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

           #画总单
            workSheet = workBook.add_sheet("总单")
            for i in range(self.totalModel.tw_ditalModel.columnCount()):
                workSheet.col(i).width = 4000
            self.initExcelTotalTable(workSheet,titileStyle,contentStyle,self.unitInfoList, self.equipInfo, self.year, self.requireInfo)

            #画分单
            for unitInfo, num in zip(self.unitInfoList, self.requireInfo[2: -2]):
                if num == "" or num == "0":
                    continue
                workSheet = workBook.add_sheet(num)
                for i in range(self.currentSingelUnitPage[unitInfo[0]].tw_ditalModel.columnCount()):
                    workSheet.col(i).width = 4000
                self.initToExcelSingleTable(unitInfo[0], workSheet, contentStyle, unitInfo, self.equipInfo, self.year)

            try:
                pathName = "%s/%s年调拨单.xls" % (directoryPath, self.year)
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

    def initExcelTotalTable(self,workSheet,titileStyle,contentStyle, unitInfoList, equipInfo, year, requireInfo):
        minSize = 13
        isMin = False
        unitNum = len(unitInfoList)
        crtColumnCount = len(unitInfoList) + 6
        title = '装备调拨分配计划'
        if crtColumnCount < minSize:
            crtColumnCount = minSize
            isMin = True
        else:
            isMin = False
        crtRowCount = 26
        workSheet.write_merge(0, 2, 0, crtColumnCount - 1, title,contentStyle)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'调拨单号:', '调拨日期:', 3)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'调拨依据:', '调拨性质:', 4)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'交装单位:', '单位地址:', 5)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'联系人:', '联系方式:', 6)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'军代表:', '联系方式:', 7)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'接装单位:', '', 8)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'单位地址:', '', 9)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'联系人:', '联系方式:', 10)
        half = int((crtColumnCount - 2) / 2)
        self.initExcelTotalTableNinethRow(workSheet,contentStyle,crtColumnCount,'调拨方式:', '运输方式:', 11)
        workSheet.write(15, 0, '1',contentStyle)
        workSheet.write(15, 1, equipInfo[1], contentStyle)
        workSheet.write(15, 2, equipInfo[5], contentStyle)
        workSheet.write(15, 3, requireInfo[0], contentStyle)
        workSheet.write(15, 4, requireInfo[1], contentStyle)

        for i, unitInfo in enumerate(unitInfoList):
            workSheet.write(14, 5 + i, unitInfo[3], contentStyle)
        workSheet.write(14, 0, '编号', contentStyle)
        workSheet.write(14, 1, '装备名称', contentStyle)
        workSheet.write(14, 2, '计量单位', contentStyle)
        workSheet.write(14, 3, '质量', contentStyle)
        workSheet.write(14, 4, '总数', contentStyle)
        workSheet.write(14, crtColumnCount - 1, '备注', contentStyle)
        for i, num in enumerate(requireInfo[2:-2]):
            workSheet.write(15, i + 5, num, contentStyle)
        workSheet.write_merge(crtRowCount - 9, crtRowCount -6, 0, 0, '备注', contentStyle )
        workSheet.write_merge(crtRowCount - 9, crtRowCount - 6, 1, crtColumnCount - 1, "1.火箭军装备分配，按照《装备调拨分配计划》执行；\n"
                     "2.火箭军部队接装，需凭《火箭军装备调拨通知单》；\n"
                     "3.完成装备调拨后，将《装备调拨分配计划》《火箭军装备调拨通知单》第一联，盖章签字后交我局；《火箭军装备调拨通知单》第三联，盖章签字后交接装单位。", contentStyle)
        self.initExcelTotalTableLastFourRow(workSheet,contentStyle,crtColumnCount,"承办单位:", "(盖章)", "交装单位:", "(盖章)", crtRowCount - 4)
        self.initExcelTotalTableLastFourRow(workSheet,contentStyle,crtColumnCount,"局    长:", '', "主管领导:", "", crtRowCount - 3)
        self.initExcelTotalTableLastFourRow(workSheet,contentStyle,crtColumnCount,"经 办 人:", '', "经 办 人:", "", crtRowCount - 2)
        self.initExcelTotalTableLastFourRow(workSheet,contentStyle,crtColumnCount,"日    期:", '', "日    期:", '', crtRowCount - 1)
        workSheet.write(13, 0, '有效期至: ', contentStyle)

        if self.totalModel.tw_ditalModel.cellWidget(13, 1):
            contextText = self.totalModel.tw_ditalModel.cellWidget(13, 1).text()
        else:
            contextText = ""
        workSheet.write(13, 1, contextText, contentStyle)



        # 初始化前9行
    def initExcelTotalTableNinethRow(self, workSheet, stlye, crtColumnCount, first, second, row):
        workSheet.write(row,0,first,stlye)
        half = int((crtColumnCount - 2) / 2)
        workSheet.write(row, half + 1, second, stlye)


        if row == 3:
            # 写第二列
            if self.totalModel.tw_ditalModel.item(row, 1):
                contextText = self.totalModel.tw_ditalModel.item(row, 1).text()
            else:
                contextText = ""
            workSheet.write_merge(row, row, 1, half, contextText,stlye)
            #写第四列
            half = int((crtColumnCount - 4) / 2)
            if self.totalModel.tw_ditalModel.cellWidget(row, half + 3):
                contextText = self.totalModel.tw_ditalModel.cellWidget(row, half + 3).text()
            else:
                contextText = ""
            workSheet.write_merge(row, row, half + 3, crtColumnCount - 1, contextText, stlye)

        elif row == 8 or row == 9:
            # 写第二列
            if self.totalModel.tw_ditalModel.item(row, 1):
                contextText = self.totalModel.tw_ditalModel.item(row, 1).text()
            else:
                contextText = ""
            workSheet.write_merge(row, row, 1, half, contextText,stlye)
            #写第四列
            workSheet.write_merge(row, row, half + 2, crtColumnCount - 1, '', stlye)
        elif row == 5:
            #写第二列
            if self.totalModel.tw_ditalModel.cellWidget(row, 1):
                Send_UnitName = self.totalModel.tw_ditalModel.cellWidget(5, 1).currentText()
            else:
                Send_UnitName = ""
            workSheet.write_merge(row, row, 1, half, Send_UnitName,stlye)
            #写第四列
            if self.totalModel.tw_ditalModel.item(row, half + 2):
                contextText = self.totalModel.tw_ditalModel.item(row, half + 2).text()
            else:
                contextText = ""
            workSheet.write_merge(row, row, half + 2, crtColumnCount - 1, contextText, stlye)

        else:
            #写第二列
            if self.totalModel.tw_ditalModel.item(row, 1):
                contextText = self.totalModel.tw_ditalModel.item(row, 1).text()
            else:
                contextText = ""

            workSheet.write_merge(row, row, 1, half, contextText,stlye)
            #写第四列
            if self.totalModel.tw_ditalModel.item(row, half + 2):
                contextText = self.totalModel.tw_ditalModel.item(row, half + 2).text()
            else:
                contextText = ""
            workSheet.write_merge(row, row, half + 2, crtColumnCount - 1, contextText,stlye)



    def initToExcelSingleTable(self,pageIndex, workSheet, style, unitInfo, equipInfo, year):
        crtColumnCount = 10
        crtRowCount = 27
        self.initSingleTable(pageIndex, workSheet, style,crtRowCount, crtColumnCount, unitInfo, equipInfo, 0)
        workSheet.write_merge(14, 14 + crtRowCount - 24, crtColumnCount, crtColumnCount,"第一联：存根" ,style)
        self.initSingleTable(pageIndex, workSheet, style,crtRowCount, crtColumnCount,unitInfo, equipInfo, crtColumnCount + 1)
        workSheet.write_merge(14, 14 + crtRowCount - 24, crtColumnCount * 2 + 1,  crtColumnCount * 2 + 1, "第二联：发物单位留存",style)
        self.initSingleTable(pageIndex, workSheet, style,crtRowCount, crtColumnCount,unitInfo, equipInfo, crtColumnCount * 2 + 2)
        workSheet.write_merge(14, 14 + crtRowCount - 24, crtColumnCount * 3 + 2,  crtColumnCount * 3 + 3, "第三联：收物单位留存",style)

    def initExcelTotalTableLastFourRow(self, workSheet, stlye,crtColumnCount, first, second, third, fourth, row):
        half = int((crtColumnCount - 4) / 2)
        workSheet.write(row, 0, first, stlye)
        if len(second) < 0:
            if self.totalModel.tw_ditalModel.item(row, 1) != None:
                contentText = self.totalModel.tw_ditalModel.item(row, 1).text()
            else:
                contentText = ''
        else:
            contentText = second
        workSheet.write(row, 1, contentText, stlye)
        workSheet.write_merge(row, row, 2, 1 + half, '', stlye)
        workSheet.write(row, half + 2, third, stlye)

        if len(fourth) < 0:
            if self.totalModel.tw_ditalModel.item(row, half + 3) != None:
                contentText = self.totalModel.tw_ditalModel.item(row, half + 3).text()
            else:
                contentText = ''
        else:
            contentText = fourth
        workSheet.write(row, half + 3, contentText, stlye)
        workSheet.write_merge(row, row, half + 4, crtColumnCount - 1, '', stlye)

    def initSingleTable(self,pageIndex, workSheet,stlye, crtRowCount, crtColumnCount,unitInfo, equipInfo, startColumn):
        workSheet.write_merge(0, 2, startColumn,startColumn + crtColumnCount - 1, '火箭军装备调拨通知单', stlye)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'调拨单号:', '调拨日期:', 3, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'调拨依据:', '调拨性质:', 4, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'交装单位:', '单位地址:', 5, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'联系人:', '联系方式:', 6, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'军代表:', '联系方式:', 7, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'接装单位:', '', 8, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'单位地址:', '', 9, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'联系人:', '联系方式:', 10, startColumn)
        self.initSingleTableExcelNinethRow(pageIndex, workSheet, stlye, crtColumnCount,'调拨方式:', '运输方式:', 11, startColumn)

        workSheet.write_merge(14, 15, startColumn , startColumn , "编号",stlye)
        workSheet.write_merge(14, 15, startColumn + 1, startColumn + 1, "装备名称",stlye)
        workSheet.write_merge(14, 15, startColumn + 2, startColumn + 2, "计量单位",stlye)
        workSheet.write_merge(14, 14, startColumn + 3, startColumn + 4, "应发数",stlye)
        workSheet.write(15, startColumn + 3, "质量",stlye)
        workSheet.write(15, startColumn + 4, "数量",stlye)
        workSheet.write_merge(14, 14, startColumn + 5, startColumn + 6, "实发数", stlye)
        workSheet.write(15, startColumn + 5, "质量", stlye)
        workSheet.write(15, startColumn + 6, "质量", stlye)
        workSheet.write_merge(14, 14, startColumn + 7, startColumn + 8, "接收数", stlye)
        workSheet.write(15, startColumn + 7, "质量", stlye)
        workSheet.write(15, startColumn + 8, "数量", stlye)
        workSheet.write(15, startColumn + 9, "备注", stlye)
        workSheet.write_merge(crtRowCount - 9, crtRowCount - 6, startColumn, startColumn, "备注", stlye)
        workSheet.write_merge(crtRowCount - 9, crtRowCount - 6, startColumn + 1, startColumn + crtColumnCount - 1, "1.凭《火箭军装备调拨通知单》接装；\n"
                     "2.完成接装后，将《火箭军装备调拨通知单》三联单，按要求分别盖章签字，并归档。", stlye)
        self.initSingleTableExcelLastFourRow(pageIndex, workSheet, stlye, crtColumnCount,"承办单位:", "(盖章)", "交装单位:", "(盖章)", crtRowCount - 4, startColumn)
        self.initSingleTableExcelLastFourRow(pageIndex, workSheet, stlye, crtColumnCount,"局    长:", "杨刚", "主管领导:", "", crtRowCount - 3, startColumn)
        self.initSingleTableExcelLastFourRow(pageIndex, workSheet, stlye, crtColumnCount,"经 办 人:", "", "经 办 人:", "", crtRowCount - 2, startColumn)
        self.initSingleTableExcelLastFourRow(pageIndex, workSheet, stlye, crtColumnCount,"日    期:", "", "日    期:", "", crtRowCount - 1, startColumn)



    def initSingleTableExcelNinethRow(self,pageIndex, workSheet, stlye, crtColumnCount, first, second, row, startColumn):
        half = int((crtColumnCount - 2) / 2)
        workSheet.write(row, startColumn, first, stlye)
        if self.currentSingelUnitPage[pageIndex].tw_ditalModel.item(row, 1):
            contextText = self.currentSingelUnitPage[pageIndex].tw_ditalModel.item(row, 1).text()
        else:
            contextText = ""
        workSheet.write_merge(row, row, startColumn + 1, startColumn + half, contextText, stlye)
        workSheet.write(row, startColumn + half + 1, second, stlye)
        if self.currentSingelUnitPage[pageIndex].tw_ditalModel.item(row, half + 2):
            contextText = self.currentSingelUnitPage[pageIndex].tw_ditalModel.item(row, half + 2).text()
        else:
            contextText = ""
        workSheet.write_merge(row, row, startColumn + half + 2,startColumn + crtColumnCount - 1 ,contextText, stlye)


    def initSingleTableExcelLastFourRow(self,pageIndex, workSheet, stlye, crtColumnCount, first, second, third, fourth, row, startColumn):
        #第一列
        workSheet.write(row, startColumn, first, stlye)
        #第二列
        workSheet.write(row, startColumn + 1, second, stlye)
        #第三列
        workSheet.write(row, startColumn + 2, '', stlye)
        #第四列
        workSheet.write(row, startColumn + 3, third, stlye)
        #第五列
        workSheet.write(row, startColumn + 4, fourth, stlye)
        #第六列
        workSheet.write(row, startColumn + 5, '', stlye)
        # 第四列
        if '交装单位' in third:
            third = '接装单位'
        workSheet.write(row, startColumn + 6, third, stlye)
        # 第五列
        workSheet.write(row, startColumn + 7, fourth, stlye)
        # 第六列
        workSheet.write(row, startColumn + 8, '', stlye)
        workSheet.write(row, startColumn + 9, '', stlye)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = transferModel()
    widget.getUnitIDList([["1", "", '', '96602' ], ["2","", '', '96603'],
                                         ['3', "", '', '96604' ]], ['3', '装备', '1', '', '', '车'],"2001",
                                        ("良好", "3", '1', '1', '1', '分配依据', '陆军调拨单单号'))
    widget.show()
    sys.exit(app.exec_())

