import pickle
import sys
import xlrd
import xlwt
from PyQt5.Qt import QRegExp
from PyQt5.Qt import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, \
    QFileDialog

from database.strengthDisturbSql import *
from sysManage.showInputResult import showInputResult
from sysManage.strengthDisturb.FilterTitle import FilterTitle
from sysManage.strengthDisturb.chooseFactoryYear import chooseFactoryYear
from widgets.strengthDisturb.inquiry_result import Widget_Inquiry_Result
from sysManage.component import getMessageBox

regx = QRegExp("[0-9]*")
#new
'''
    类功能：
        管理实力分布下实力查询结果界面，包含查询结果相关逻辑代码
        实力查询 右边部分 结果界面
'''
class Inquiry_Result(QWidget, Widget_Inquiry_Result):
    def __init__(self, parent=None):
        super(Inquiry_Result, self).__init__(parent)
        self.setupUi(self)

        #存储当前查询结果，结构为：{'行号':该行数据'}
        self.currentInquiryResult = {}
        self.unitList = []
        self.equipList = []
        self.year = None
        self.resultList = []
        self.titleList = []
        self.chooseFactoryYear = chooseFactoryYear(self)
        self.filterTitle = FilterTitle()
        self.chooseFactoryYear.hide()
        self.currentFactoryYear = ''
        self.NewStrength = None
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        #信号和槽连接
        self.signalConnect()
        self.startFactoryYear = None
        self.endFactoryYear = None
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.tw_inquiryResult.setColumnCount(len(headerlist))
        self.tw_inquiryResult.setSelectionBehavior(QAbstractItemView.SelectRows)


    '''
        信号和槽连接
    '''
    def signalConnect(self):
        #当点击按装备展开时
        self.rb_equipShow.clicked.connect(self.slotClickedRB)

        #当点击按单位展开时
        self.rb_unitShow.clicked.connect(self.slotClickedRB)

        #当展开到末级被点击时
        self.cb_showLast.clicked.connect(self.slotClickedRB)

        #当只列存在偏差被点击时
        self.cb_showDistence.clicked.connect(self.slotClickedRB)

        #当不显示0值被点击时
        self.cb_showValue0.clicked.connect(self.slotClickedRB)

        #删除当前装备
        self.pb_clearCheck.clicked.connect(self.slotClearCurrentRow)

        #清除当前页面全部装备实力数
        self.pb_clearAll.clicked.connect(self.slotClearCurrentPage)

        #选择展示的出厂年份
        self.pb_factoryYear.clicked.connect(self.slotChooseFactoryYear)

        #筛选表头
        self.pb_filterTitle.clicked.connect(self.slotShowFilterTitle)

        #修改实力数
        self.tw_inquiryResult.itemChanged.connect(self.slotItemChange)

        self.chooseFactoryYear.tb_cancel.clicked.connect(self.slotCancelChooseFactoryYear)

        self.chooseFactoryYear.tb_yes.clicked.connect(self.slotChangeSeeMethod)

        self.filterTitle.signal.connect(self.slotFilterTitle)
        self.filterTitle.pb_Cancel.clicked.connect(self.slotFilterTitleHide)
        #导出数据至Excel
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)

        # 导出数据包
        self.pb_output.clicked.connect(self.slotOutputData)
        # 导入数据包
        self.pb_input.clicked.connect(self.slotInputData)
        self.pb_inputFromExcel.clicked.connect(self.slotInputDataFromExcel)
        # 导入数据到数据库
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoDatabase)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoDatabase)

    def allButtonDisabled(self):
        # self.pb_input.setCheckable(False)
        # self.pb_output.setCheckable(False)
        # self.pb_outputToExcel.setCheckable(False)
        self.cb_showLast.setChecked(False)
        self.cb_showDistence.setChecked(False)
        self.cb_showValue0.setChecked(False)
        # self.pb_clearCheck.setCheckable(False)
        # self.pb_clearAll.setCheckable(False)
        # self.pb_factoryYear.setCheckable(False)
        # self.pb_filterTitle.setCheckable(False)
        self.rb_equipShow.setChecked(False)
        self.rb_unitShow.setChecked(False)
        self.pb_input.setDisabled(True)
        self.pb_inputFromExcel.setDisabled(True)
        self.pb_output.setDisabled(True)
        self.pb_outputToExcel.setDisabled(True)
        self.cb_showLast.setDisabled(True)
        self.cb_showDistence.setDisabled(True)
        self.cb_showValue0.setDisabled(True)
        self.pb_clearCheck.setDisabled(True)
        self.pb_clearAll.setDisabled(True)
        self.pb_factoryYear.setDisabled(True)
        self.pb_filterTitle.setDisabled(True)
        self.rb_equipShow.setDisabled(True)
        self.rb_unitShow.setDisabled(True)

    def allButtonAvailabled(self):
        # self.pb_input.setCheckable(False)
        # self.pb_output.setCheckable(False)
        # self.pb_outputToExcel.setCheckable(False)
        self.cb_showLast.setChecked(False)
        self.cb_showDistence.setChecked(False)
        self.cb_showValue0.setChecked(False)
        # self.pb_clearCheck.setCheckable(False)
        # self.pb_clearAll.setCheckable(False)
        # self.pb_factoryYear.setCheckable(False)
        # self.pb_filterTitle.setCheckable(False)
        self.rb_equipShow.setChecked(False)
        self.rb_unitShow.setChecked(False)
        self.pb_input.setDisabled(False)
        self.pb_inputFromExcel.setDisabled(False)
        self.pb_output.setDisabled(False)
        self.pb_outputToExcel.setDisabled(False)
        self.cb_showLast.setDisabled(False)
        self.cb_showDistence.setDisabled(False)
        self.cb_showValue0.setDisabled(False)
        self.pb_clearCheck.setDisabled(False)
        self.pb_clearAll.setDisabled(False)
        self.pb_factoryYear.setDisabled(False)
        self.pb_filterTitle.setDisabled(False)
        self.rb_equipShow.setDisabled(False)
        self.rb_unitShow.setDisabled(False)


    def slotChangeSeeMethod(self):
        if self.chooseFactoryYear.selectAll:
            self.currentFactoryYear = ""
            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
            self.lb_factoryYear.setText("当前查询出厂年份为：全部")
            self.chooseFactoryYear.hide()
        else:
            self.currentFactoryYear = "---"
            self.startFactoryYear = self.chooseFactoryYear.startFactoryYear
            self.endFactoryYear = self.chooseFactoryYear.endFactoryYear
            #print("===============0", self.startFactoryYear, self.endFactoryYear)
            if int(self.startFactoryYear) > int(self.endFactoryYear):
                getMessageBox("查询", "请重新选择，开始年份必须小于等于结束年份", True, False)
                return
            else:
                self.lb_factoryYear.setText("当前查询出厂年份为：" + self.startFactoryYear + "年 至 " + self.endFactoryYear + "年")
                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                self.chooseFactoryYear.hide()


    '''
        信号和槽连接断开
    '''
    def slotDisconnect(self):
        pass


    def slotChooseFactoryYear(self):
        self.chooseFactoryYear.initComBoxAboutYear()
        self.chooseFactoryYear.show()

    # 筛选表头
    def slotShowFilterTitle(self):
        self.filterTitle.show()

    def slotFilterTitle(self):
        self.titleList = self.filterTitle.result
        if len(self.unitList) < 1 or len(self.equipList) < 1:
            self.tw_inquiryResult.setHorizontalHeaderLabels(self.titleList)
            self.tw_inquiryResult.setColumnCount(len(self.titleList))
        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
        # self.filterTitle.hide()

    def slotFilterTitleHide(self):
        self.filterTitle.hide()

    '''
        清除当前结果页面所有的实力数
    '''
    def slotClearCurrentPage(self):
        if self.currentFactoryYear != "":
            getMessageBox('清除', '清除失败,请将出厂年份设置为全部', True, False)
            return
        if self.year == '全部':
            getMessageBox('清除', '只能某一年，清除失败', True, False)
            return
        reply = getMessageBox('清除', '是否清除当前页面所有行的实力数？', True, True)
        if reply == QMessageBox.Cancel:
            return

        for i, resultInfo in self.currentInquiryResult.items():
            Unit_ID = resultInfo[1]
            Equip_ID = resultInfo[0]
            orginNum = resultInfo[4]
            year = resultInfo[15]
            unitHaveChild = selectUnitIsHaveChild(Unit_ID)
            equipHaveChild = selectEquipIsHaveChild(Equip_ID)
            if unitHaveChild or equipHaveChild:
                getMessageBox('清除', '第' + str(i) + "行清除失败，只能清除末级单位和装备实力数", True, False)
                continue
            else:
                updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, "0", orginNum)
                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)


    def changeCurrentFactoryYear(self):
        self.currentFactoryYear = self.chooseFactoryYear.cb_factoryYear.currentText()

        text = "当前显示的出厂年份：" + self.currentFactoryYear
        self.lb_factoryYear.setText(text)

        if self.currentFactoryYear == "全部":
            self.currentFactoryYear = ''
        self.chooseFactoryYear.hide()

        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)


    def slotCancelChooseFactoryYear(self):
        self.chooseFactoryYear.hide()


    '''
        清除当前行的实力数
    '''
    def slotClearCurrentRow(self):
        currentRow = self.tw_inquiryResult.currentRow()
        if currentRow < 0:
            return
        else:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    Unit_ID = resultInfo[1]
                    Equip_ID = resultInfo[0]
                    orginNum = resultInfo[4]
                    year = resultInfo[15]
                    unitHaveChild = selectUnitIsHaveChild(Unit_ID)
                    equipHaveChild = selectEquipIsHaveChild(Equip_ID)
                    if unitHaveChild or equipHaveChild:
                        getMessageBox('清除', '只能清除末级单位和装备的实力数', True, False)
                        return
                    elif self.year == '全部':
                        getMessageBox('清除', '只能某一年，清除失败', True, False)
                        return
                    else:
                        getMessageBox('清除', '是否清除当前行的实力数？', True, True)
                        updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, "0", orginNum)
                        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)


    '''
        功能：
            当前表格中某个值被修改
    '''
    def slotItemChange(self):
        currentRow = self.tw_inquiryResult.currentRow()
        currentColumn = 2
        # if currentRow < 0:
        #     reply = QMessageBox.information(self, "修改", "请选中某行", QMessageBox.Yes)
        #     return
        if currentColumn > 0:
            try:
                for i, resultInfo in self.currentInquiryResult.items():
                    if i == currentRow:
                        Unit_ID = resultInfo[1]
                        Equip_ID = resultInfo[0]
                        # unitHaveChild = selectUnitIsHaveChild(Unit_ID)
                        # equipHaveChild = selectEquipIsHaveChild(Equip_ID)
                        if self.NewStrength == str(resultInfo[4]):
                            return
                        if self.currentFactoryYear != "":
                            getMessageBox('清除', '清除失败,请将出厂年份设置为全部', True, False)
                            self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[4])
                            return
                        # if unitHaveChild or equipHaveChild:
                        #     reply = QMessageBox.question(self, '修改', '只能修改末级实力数，修改失败', QMessageBox.Yes)
                        #     self.tw_inquiryResult.item(currentRow, currentColumn).setText(str(resultInfo[4]))
                        #     return
                        elif self.year == '全部':
                            getMessageBox('修改', '只能某一年，修改失败', True, False)
                            self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[4])
                            return
                        else:
                            if self.tw_inquiryResult.item(currentRow, currentColumn).text() != resultInfo[4]:
                                num = self.tw_inquiryResult.item(currentRow,currentColumn).text()
                                updateSuccess = updateStrengthAboutStrengrh\
                                    (Unit_ID, Equip_ID, self.year,num,str(resultInfo[4]))
                                if not updateSuccess:
                                    getMessageBox("修改", str(updateSuccess) + "修改失败", True, False)
                                    # QMessageBox.information(self, "修改", "修改成功！", QMessageBox.Yes)
                                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                                # except ValueError:
                                #     reply = QMessageBox.question(self, '修改失败', '只能修改为整数', QMessageBox.Yes)
                                #     self.tw_inquiryResult.item(currentRow, currentColumn).setText(str(resultInfo[4]))
                                #     return
            except ValueError:
                getMessageBox("提示", "请输入正确的数字", True, False)
                # self.disturbResult.item(self.currentRow, self.currentColumn).setText(0)


    #当某个单击按钮被选中时
    def slotClickedRB(self):
        if len(self.unitList) < 1 or len(self.equipList) < 1:
            return
        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    #初始化tableWidget
    def _initTableWidgetByUnitListAndEquipList(self, UnitList, EquipList, year):
        self.tw_inquiryResult.clear()
        self.tw_inquiryResult.setRowCount(0)
        self.unitList = UnitList
        self.equipList = EquipList
        print("self.unitList=",self.unitList,"self.equipList=",self.equipList)
        self.year = year
        self.resultList = []
        flagValue0 = False
        if self.cb_showValue0.isChecked():
            flagValue0 = True
        if self.titleList:
            headerlist = self.titleList
        else:
            headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        print("headerlist=",headerlist)
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.tw_inquiryResult.setColumnCount(len(headerlist))
        if self.rb_equipShow.isChecked():
            #按装备展开
            self.resultList= selectAboutStrengthByEquipShow(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear,flagValue0)
        elif self.rb_unitShow.isChecked():
            #按单位展开
            self.resultList = selectAboutStrengthByUnitShow(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear,flagValue0)
        else:
            self.resultList = selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear,flagValue0)

        if self.cb_showLast.isChecked():
            self.resultList = selectAboutStrengthByLast(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear,flagValue0)
            self.rb_unitShow.setCheckable(False)
            self.rb_equipShow.setCheckable(False)
            self.rb_equipShow.setDisabled(True)
            self.rb_unitShow.setDisabled(True)
        else:
            self.rb_unitShow.setCheckable(True)
            self.rb_equipShow.setCheckable(True)
            self.rb_equipShow.setDisabled(False)
            self.rb_unitShow.setDisabled(False)

        self.tw_inquiryResult.setRowCount(len(self.resultList))
        isMinyear = selectIsMinStrengthYear(year)
        i = 0
        index1=-1
        for LineInfo in self.resultList:
            if self.cb_showDistence.isChecked():
                if int(LineInfo[7]) != 0:
                    item = QTableWidgetItem(LineInfo[3])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('单位名称'), item)
                    except ValueError:
                        pass

                    item = QTableWidgetItem(LineInfo[2])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('装备名称'), item)
                    except ValueError:
                        pass

                    # item = QLineEdit()
                    # item.setText(str(LineInfo[4]))
                    # item.textChanged.connect(self.slotItemChange)
                    # item.setStyleSheet("background:transparent;border-width:0")
                    # validator = QRegExpValidator(regx)
                    # item.setValidator(validator)
                    # self.tw_inquiryResult.setCellWidget(i, 2, item)

                    item = QTableWidgetItem(str(LineInfo[4]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                    # item.setBackground(QBrush(QColor(154, 200, 226)))
                    # self.tw_inquiryResult.setItem(i, 2, item)
                    try:
                        index1 = headerlist.index('实力数')
                        self.tw_inquiryResult.setItem(i, index1, item)
                    except ValueError:
                        pass


                    item = QTableWidgetItem(str(LineInfo[5]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 3, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('编制数'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[6]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 4, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('现有数'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[7]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 5, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('偏差'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[8]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 6, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('准备退役数'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[9]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 7, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('未到位数'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[10]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 8, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('提前退役'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[11]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 9, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('待核查无实物'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[12]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 10, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('待核查无实力'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[13]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 11, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('单独建账'), item)
                    except ValueError:
                        pass
                    item = QTableWidgetItem(str(LineInfo[14]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    # self.tw_inquiryResult.setItem(i, 12, item)
                    try:
                        self.tw_inquiryResult.setItem(i, headerlist.index('正常到位'), item)
                    except ValueError:
                        pass

                    self.currentInquiryResult[i] = LineInfo
                    i = i + 1
                else:
                    pass
            else:
                item = QTableWidgetItem(LineInfo[3])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 0, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('单位名称'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(LineInfo[2])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 1, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('装备名称'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[4]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                # item.setBackground(QBrush(QColor(154, 200, 226)))
                # self.tw_inquiryResult.setItem(i, 2, item)
                try:
                    index1 = headerlist.index('实力数')
                    self.tw_inquiryResult.setItem(i, index1, item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[5]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 3, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('编制数'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[6]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 4, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('现有数'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[7]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 5, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('偏差'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[8]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 6, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('准备退役数'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[9]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 7, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('未到位数'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[10]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 8, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('提前退役'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[11]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 9, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('待核查无实物'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[12]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 10, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('待核查无实力'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[13]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 11, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('单独建账'), item)
                except ValueError:
                    pass
                item = QTableWidgetItem(str(LineInfo[14]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # self.tw_inquiryResult.setItem(i, 12, item)
                try:
                    self.tw_inquiryResult.setItem(i, headerlist.index('正常到位'), item)
                except ValueError:
                    pass

                self.currentInquiryResult[i] = LineInfo
                i = i + 1
        self.tw_inquiryResult.setRowCount(i)
        if self.equipList and self.unitList:
            self.ifEquipAndUnitHaveNoChild(index1)

    def ifEquipAndUnitHaveNoChild(self, index):
        if index == -1:
            return
        row1=0
        for i in self.unitList:
            if selectUnitIsHaveChild(i):
                row1+=len(self.equipList)
                continue
            for j in self.equipList:
                if selectEquipIsHaveChild(j):
                    row1+=1
                else:
                    item = self.tw_inquiryResult.item(row1, index)
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                    item.setBackground(QBrush(QColor(154, 200, 226)))
                    row1+=1




    #导出至Excel
    def slotOutputToExcel(self):

        if len(self.resultList) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('修改导出Excel', '是否保存修改并导出Excel？', True, True)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList,
                                                        self.year)
            return
        for i, result in self.currentInquiryResult.items():
            if result[13] == True:
                checkbox = self.tw_result.cellWidget(i + 2, 5)
                num = checkbox.itemText(0)
                apply = self.tw_result.item(i + 2, 8).text()
                other = self.tw_result.item(i + 2, 9).text()
                updateRetireAboutRetire(num, apply, other, result)

        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList,self.year)
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

            contentStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_LEFT
            alignment.vert = xlwt.Alignment.VERT_TOP

            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            contentStyle.font = font  # 设定样式
            contentStyle.alignment = alignment
            contentStyle.borders = borders

            #画表头
            headerlist = [ '单位编号','单位名称', '装备编号', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力',
                          '单独建账',
                          '正常到位']
            for i in range(len(headerlist)):
                workSheet.col(i).width = 4000
                workSheet.write(0, i, headerlist[i], titileStyle)

            #填表
            for index,LineInfo in enumerate(self.resultList):
                #  装备号 单位号
                # ['5', '6', 'A车', '六十一旅团', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2001']
                workSheet.write(index + 1, 0, str(LineInfo[1]), contentStyle)
                workSheet.write(index + 1, 1, str(LineInfo[3]), contentStyle)
                workSheet.write(index + 1, 2, str(LineInfo[0]), contentStyle)
                workSheet.write(index + 1, 3, str(LineInfo[2]), contentStyle)

                workSheet.write(index + 1, 4, str(LineInfo[4]), contentStyle)
                workSheet.write(index + 1, 5, str(LineInfo[5]), contentStyle)
                workSheet.write(index + 1, 6, str(LineInfo[6]), contentStyle)
                workSheet.write(index + 1, 7, str(LineInfo[7]), contentStyle)
                workSheet.write(index + 1, 8, str(LineInfo[8]), contentStyle)
                workSheet.write(index + 1, 9, str(LineInfo[9]), contentStyle)
                workSheet.write(index + 1, 10, str(LineInfo[10]), contentStyle)
                workSheet.write(index + 1, 11, str(LineInfo[11]), contentStyle)
                workSheet.write(index + 1, 12, str(LineInfo[12]), contentStyle)
                workSheet.write(index + 1, 13, str(LineInfo[13]), contentStyle)
                workSheet.write(index + 1, 14, str(LineInfo[14]), contentStyle)
            try:
                pathName = "%s/%s年%s实力对比表.xls" % (directoryPath,self.year, selectUnitNameByUnitID(self.unitList[0]))
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                getMessageBox("导出成功", "导出成功！", True, False)
                return
            except Exception as e:
                getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                return
        else:
            getMessageBox("未选中导出目录", "导出失败！", True, False)
            return

    # 导出数据包
    def slotOutputData(self):
        if len(self.resultList) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('导出数据包', '是否导出数据包？', True, True)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList,
                                                        self.year)
            return
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            # 填表数据
            dataList = self.resultList
            dataList.insert(0, "实力查询数据")
            print("实力查询数据")
            print(dataList)  # ['实力查询数据'， ['5', '10', 'A车', '六十一旅团一阵地', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2000']]
            if dataList is None or len(dataList) == 1:
                return
            else:
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s实力查询.nms" % (directoryPath, installData)
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                getMessageBox("导出成功", "导出成功！", True, False)
        else:
            getMessageBox("导出数据失败！", "请选择正确的文件夹！", True, False)

    # 导入实力查询数据
    def slotInputData(self):
        self.inputList = []
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            with open(filename, "rb") as file:
                self.inputList = pickle.load(file)
                if self.inputList[0] != "实力查询数据":
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            getMessageBox("加载文件失败！", "请检查文件格式及内容格式！", True, False)
            return
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(headerlist))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(headerlist)
        self.showInputResult.tw_result.setRowCount(len(self.inputList) - 1)
        print("self.inputList", self.inputList)
        for i, LineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            i = i - 1
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(str(LineInfo[4]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 2, item)

            item = QTableWidgetItem(str(LineInfo[5]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(str(LineInfo[6]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)
            item = QTableWidgetItem(str(LineInfo[7]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(str(LineInfo[8]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(str(LineInfo[9]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)
            item = QTableWidgetItem(str(LineInfo[10]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 8, item)
            item = QTableWidgetItem(str(LineInfo[11]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 9, item)
            item = QTableWidgetItem(str(LineInfo[12]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 10, item)
            item = QTableWidgetItem(str(LineInfo[13]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 11, item)
            item = QTableWidgetItem(str(LineInfo[14]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 12, item)
        pass

    '''
        从Excel导入实力数
    '''
    def slotInputDataFromExcel(self):
        self.inputList = []
        self.setDisabled(True)
        self.showInputResult.setDisabled(False)
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.xls);;Excel Files (*.xlsx)")
        try:
            workBook = xlrd.open_workbook(filename)
            self.workSheet = workBook.sheet_by_index(0)

            if self.workSheet.ncols != 15:
                getMessageBox("打开失败", "打开文件失败，请检查文件是否正确", True, False)
                self.setDisabled(False)
                return
            year = ((filename.split('/'))[-1])[0:4]
            print('year')
            print(year)
            try:
                year = str(int(year))
            except:
                getMessageBox("读取失败", "读取年份失败，年份是否正确！", True, False)
                self.setDisabled(False)
                return
            print("year: " + year)
            title = ['单位编号', '单位名称', '装备编号', '装备名称', '实力数']
            for r in range(1, self.workSheet.nrows):
                unitId = (self.workSheet.cell(r, 0).value)
                unitName = self.workSheet.cell(r, 1).value
                equipId = (self.workSheet.cell(r, 2).value)
                equipName = self.workSheet.cell(r, 3).value
                strength = (self.workSheet.cell(r, 4).value)
                try:
                    unitId = str(int(unitId))
                    equipId = str(int(equipId))
                    strength = str(int(strength))
                except:
                    getMessageBox("读取失败", "读取第%d行数据失败，请检测数据是否正确！" % (r), True, False)
                    continue
                inputInfo = []
                inputInfo.append(unitId)
                inputInfo.append(unitName)
                inputInfo.append(equipId)
                inputInfo.append(equipName)
                inputInfo.append(strength)
                inputInfo.append(year)
                self.inputList.append(inputInfo)
            self.showInputResult.setWindowTitle("从Excel导入%s实力数"%year)
            self.showInputResult.tw_result.setColumnCount(len(title))
            self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
            self.showInputResult.tw_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.showInputResult.tw_result.setRowCount(len(self.inputList))
            self.showInputResult.tw_result.verticalHeader().setVisible(False)
            for r, list_item in enumerate(self.inputList):
                item = QTableWidgetItem(list_item[0])
                self.showInputResult.tw_result.setItem(r, 0, item)
                item = QTableWidgetItem(list_item[1])
                self.showInputResult.tw_result.setItem(r, 1, item)
                item = QTableWidgetItem(list_item[2])
                self.showInputResult.tw_result.setItem(r, 2, item)
                item = QTableWidgetItem(list_item[3])
                self.showInputResult.tw_result.setItem(r, 3, item)
                item = QTableWidgetItem(list_item[4])
                self.showInputResult.tw_result.setItem(r, 4, item)
            self.showInputResult.show()

        except BaseException as e:
            print(e)
            getMessageBox("打开失败", "打开文件失败，请检查文件", True, False)
            self.setDisabled(False)




    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoDatabase(self):
        print(self.inputList)
        if len(self.inputList[0]) == 6:
            for i, lineInfo in enumerate(self.inputList):
                try:
                    if inputOneDataIntoStrenth(lineInfo):
                        pass
                except Exception as e:
                    print(e)
                    getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)
        else:
            for i, lineInfo in enumerate(self.inputList):
                if i == 0:
                    continue
                try:
                    if insertOneDataIntoStrenth(lineInfo):
                        pass
                except Exception as e:
                    print(e)
                    getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)
        self.showInputResult.hide()
        self.setDisabled(False)
        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Inquiry_Result()
    widget.show()
    sys.exit(app.exec_())
