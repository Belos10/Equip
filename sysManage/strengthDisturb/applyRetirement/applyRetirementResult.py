import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

from widgets.strengthDisturb.applyRetirement.ApplyRetirementResultUI import ApplyRetirementResultUI


class Apply_Retirement_Result(QWidget, ApplyRetirementResultUI):
    def __init__(self, parent=None):
        super(Apply_Retirement_Result, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}








if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Apply_Retirement_Result()
    widget.show()
    sys.exit(app.exec_())