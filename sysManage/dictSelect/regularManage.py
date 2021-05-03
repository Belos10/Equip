from PyQt5.QtWidgets import QWidget
from widgets.dictSelect.regularManage import Widget_Regular_Manage

class regularManage(QWidget, Widget_Regular_Manage):
    def __init__(self, parent=None):
        super(regularManage, self).__init__(parent)
        self.setupUi(self)