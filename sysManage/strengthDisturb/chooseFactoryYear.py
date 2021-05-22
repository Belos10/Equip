from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QComboBox, QMessageBox,QDialog
from widgets.strengthDisturb.chooseFactoryYear import widget_chooseFactoryYear
from database.strengthDisturbSql import selectEquipInputType, selectInfoAboutInput, selectNowNumAndStrengthNum, \
    selectAllStrengthYear, updateInputInfo, updateNumMutilInput, delFromInputInfo,selectAllDataAboutFactoryYear

'''
    类功能：
        选择显示的出厂年份
'''
class chooseFactoryYear(QDialog, widget_chooseFactoryYear):
    def __init__(self, parent=None):
        super(chooseFactoryYear, self).__init__(parent)
        self.setupUi(self)
        self.startFactoryYear = None
        self.endFactoryYear = None
        self.selectAll = True

        self.groupBox.setDisabled(True)

        self.cb_seeMethod.currentIndexChanged.connect(self.slotChangeSeeMethod)
        self.cb_factoryYearStart.currentIndexChanged.connect(self.slotStartChanged)
        self.cb_factoryYearEnd.currentIndexChanged.connect(self.slotEndChanged)

    def slotStartChanged(self):
        self.startFactoryYear = self.cb_factoryYearStart.currentText()

    def slotEndChanged(self):
        self.endFactoryYear = self.cb_factoryYearEnd.currentText()

    def slotChangeSeeMethod(self):
        if self.cb_seeMethod.currentText() != "全部":
            self.selectAll = False
            self.groupBox.setDisabled(False)
        else:
            self.selectAll = True
            self.groupBox.setDisabled(True)

    def initComBoxAboutYear(self):
        self.factoryYearList = []
        self.cb_factoryYearStart.clear()
        self.cb_factoryYearEnd.clear()

        result = selectAllDataAboutFactoryYear()

        for yearInfo in result:
            self.factoryYearList.append(yearInfo[1])

        self.cb_factoryYearStart.addItems(self.factoryYearList)
        self.cb_factoryYearEnd.addItems(self.factoryYearList)