from widgets.positionEngineer.posEngneerInstallationUI import PosEngneerInstallationUI
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from sysManage.strengthDisturb.Stren_Inquiry import Stren_Inquiry
from sysManage.strengthDisturb.strengthDisturbSet import strengthDisturbSet
from sysManage.strengthDisturb.maintenMange import maintenManage
from sysManage.strengthDisturb.equipmentBalanceControl import Equip_Balance_Control
from sysManage.strengthDisturb.retirement import retirement
#new
class InstallationSituation(QWidget, PosEngneerInstallationUI):
    def __init__(self, parent=None):
        super(InstallationSituation, self).__init__(parent)
        self.setupUi(self)
        # 当前选中的单位列表和装备列表
        self.first_treeWidget_dict = {}









if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InstallationSituation()
    widget.show()
    sys.exit(app.exec_())