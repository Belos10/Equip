
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget

from sysManage.positionEngineer.equipmentStatistics import EquipmentStatistics
from sysManage.positionEngineer.installationSituation import InstallationSituation

#new
from widgets.positionEngineer.positionEngineerWidget import Position_Engineer_Widget


class PositionEngineerMain(QMainWindow, Position_Engineer_Widget):
    def __init__(self, parent=None):
        super(PositionEngineerMain, self).__init__(parent)
        self.setupUi(self)

        self.installationSituation = InstallationSituation(self)
        self.equipmentStatistics = EquipmentStatistics(self)
        # self.directoryMaintenance = DirectoryMaintenance(self)

        self.stackedWidget.addWidget(self.installationSituation)
        self.stackedWidget.addWidget(self.equipmentStatistics)
        # self.stackedWidget.addWidget(self.directoryMaintenance)

        self.stackedWidget.setCurrentIndex(0)
        self.tb_installation.setDisabled(True)
        self.tb_equipmentStatistics.setDisabled(False)
        self.installationSituation.setDisabled(False)
        self.equipmentStatistics.setDisabled(True)
        # self.directoryMaintenance.setDisabled(True)
        self.connectSignal()


    def connectSignal(self):
        self.tb_installation.clicked.connect(self.slotInstallation)
        self.tb_equipmentStatistics.clicked.connect(self.slotEquipmentStatistics)

    def slotDisconnect(self):
        self.tb_installation.clicked.disconnect(self.slotInstallation)
        self.tb_equipmentStatistics.clicked.disconnect(self.slotEquipmentStatistics)
        # self.tb_directoryMaintenance.clicked.disconnect(self.slotDirectoryMaintenance)


    def slotInstallation(self):

        self.tb_installation.setDisabled(True)
        self.tb_equipmentStatistics.setDisabled(False)
        # self.tb_directoryMaintenance.setDisabled(False)

        self.slotDisconnect()
        self.installationSituation.init()
        self.stackedWidget.setCurrentIndex(0)
        self.installationSituation.init()
        #self.strenSelect._initStrenInquiry() #初始化函数
        self.connectSignal()

    def slotEquipmentStatistics(self):
        self.tb_installation.setDisabled(False)
        self.tb_equipmentStatistics.setDisabled(True)
        # self.tb_directoryMaintenance.setDisabled(False)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.currentWidget().setDisabled(False)
        self.equipmentStatistics.initEquipmentStatistics()
        self.connectSignal()
        # self.maintenMange._initAll_() 初始化函数

    # def slotDirectoryMaintenance(self):
    #     self.tb_installation.setDisabled(False)
    #
    #     self.tb_equipmentStatistics.setDisabled(False)
    #     self.tb_directoryMaintenance.setDisabled(True)
    #     self.slotDisconnect()
    #     self.stackedWidget.setCurrentIndex(2)
    #     self.stackedWidget.currentWidget().setDisabled(False)
    #     self.directoryMaintenance
    #     self.connectSignal()
    #     # self.directoryMaintenance._initAll_() 初始化函数


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PositionEngineerMain()
    widget.show()
    sys.exit(app.exec_())