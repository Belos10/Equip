from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QComboBox, QMessageBox,QDialog
from PyQt5.Qt import Qt
from widgets.strengthDisturb.chooseFactoryYear import widget_chooseFactoryYear
from database.strengthDisturbSql import selectEquipInputType, selectInfoAboutInput, selectNowNumAndStrengthNum, \
    selectAllStrengthYear, updateInputInfo,updateNumMutilInput, delFromInputInfo

'''
    类功能：
        选择显示的出厂年份
'''


allFactoryYearInt = list(range(1970, 2022))
allFactoryYear = [str(x) for x in allFactoryYearInt]

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

        self.setWindowTitle("选择查看的出厂年份范围")
        flags = Qt.Dialog
        flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)

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

        self.cb_factoryYearStart.addItems(allFactoryYear)
        self.cb_factoryYearEnd.addItems(allFactoryYear)