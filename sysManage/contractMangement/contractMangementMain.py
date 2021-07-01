
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget

from sysManage.contractMangement.orderManagememt import OrderManagement
from widgets.contractMangement.ContractManagementMainUI import ContractManagementMainUI


class ContractManagementMain(QMainWindow, ContractManagementMainUI):
    def __init__(self, parent=None):
        super(ContractManagementMain, self).__init__(parent)
        self.setupUi(self)

        self.orderManagement = OrderManagement()
        self.maintenanceManagement = QWidget(self)

        self.stackedWidget.addWidget(self.orderManagement)
        self.stackedWidget.addWidget(self.maintenanceManagement)

        self.stackedWidget.setCurrentIndex(0)
        self.maintenanceManagement.setDisabled(False)

        self.connectSignal()


    def connectSignal(self):
        self.tb_orderManagement.clicked.connect(self.slotOrderManagement)
        self.tb_maintenanceManagement.clicked.connect(self.slotMaintenanceManagement)
        # self.tb_directoryMaintenance.clicked.connect(self.slotDirectoryMaintenance)

    def slotDisconnect(self):
        self.tb_orderManagement.clicked.disconnect(self.slotOrderManagement)
        self.tb_maintenanceManagement.clicked.disconnect(self.slotMaintenanceManagement)


    def slotOrderManagement(self):

        self.tb_orderManagement.setDisabled(True)
        self.tb_maintenanceManagement.setDisabled(False)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(0)
        # 初始化
        self.connectSignal()

    def slotMaintenanceManagement(self):
        self.tb_maintenanceManagement.setDisabled(True)
        self.tb_orderManagement.setDisabled(False)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget.currentWidget().setDisabled(False)
        #  初始化函数
        self.connectSignal()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ContractManagementMain()
    widget.show()
    sys.exit(app.exec_())