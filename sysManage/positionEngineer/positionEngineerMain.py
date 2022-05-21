
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
        self.stackedWidget.addWidget(self.installationSituation)
        self.stackedWidget.addWidget(self.equipmentStatistics)
        self.connectSignal()
        self.slotInstallation()




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
        self.stackedWidget.setCurrentIndex(0)
        self.connectSignal()
        self.installationSituation.init()

    def slotEquipmentStatistics(self):
        self.tb_installation.setDisabled(False)
        self.tb_equipmentStatistics.setDisabled(True)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.currentWidget().setDisabled(False)
        self.equipmentStatistics.initEquipmentStatistics()
        self.connectSignal()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PositionEngineerMain()
    widget.show()
    sys.exit(app.exec_())