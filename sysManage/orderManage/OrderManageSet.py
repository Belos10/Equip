from widgets.orderManage.orderManageSet import widget_orderManageSet
from PyQt5.QtWidgets import QMainWindow,QWidget,QToolBar,QStackedWidget


class OrderManageSet(QMainWindow, widget_orderManageSet):
    def __init__(self, parent=None):
        super(OrderManageSet, self).__init__(parent)
        self.setupUi(self)
