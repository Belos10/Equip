
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget

from sysManage.dangerGoods.StrengthStatistics import StrengthStatistics
from widgets.dangerGoods.dangerGoodsWidget import Danger_Goods_Widget
from widgets.positionEngineer.positionEngineerWidget import Position_Engineer_Widget

class DangerGoods(QMainWindow, Danger_Goods_Widget):
    def __init__(self, parent=None):
        super(DangerGoods, self).__init__(parent)
        self.setupUi(self)

        self.strengthStatistics = StrengthStatistics(self)
        self.directoryMaintenance = QWidget(self)
        self.stackedWidget.addWidget(self.strengthStatistics)
        self.stackedWidget.addWidget(self.directoryMaintenance)
        self.stackedWidget.setCurrentIndex(0)
        self.strengthStatistics.setDisabled(True)
        self.directoryMaintenance.setDisabled(True)
        self.connectSignal()


    def connectSignal(self):
        self.tb_strengthStatistics.clicked.connect(self.slotStrengthStatistics)
        self.tb_directoryMaintenance.clicked.connect(self.slotDirectoryMaintenance)

    def slotDisconnect(self):
        self.tb_strengthStatistics.clicked.disconnect(self.slotStrengthStatistics)
        self.tb_directoryMaintenance.clicked.connect(self.slotDirectoryMaintenance)



    def slotStrengthStatistics(self):

        self.tb_strengthStatistics.setDisabled(True)
        self.tb_directoryMaintenance.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget.currentWidget().setDisabled(False)
        self.strengthStatistics.init()
        self.connectSignal()

    def slotDirectoryMaintenance(self):
        self.tb_strengthStatistics.setDisabled(False)
        self.tb_directoryMaintenance.setDisabled(True)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        # self.directoryMaintenance._init() 初始化函数
        self.connectSignal()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DangerGoods()
    widget.show()
    sys.exit(app.exec_())