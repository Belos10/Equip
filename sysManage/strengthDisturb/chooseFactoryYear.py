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
        self.factoryYearList = []

    def initComBoxAboutYear(self):
        self.factoryYearList = ['全部']
        self.cb_factoryYear.clear()

        result = selectAllDataAboutFactoryYear()

        for yearInfo in result:
            self.factoryYearList.append(yearInfo[1])

        self.cb_factoryYear.addItems(self.factoryYearList)