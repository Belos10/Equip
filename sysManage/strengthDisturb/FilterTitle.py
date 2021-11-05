from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from widgets.strengthDisturb.filterTitle import Widget_filterTitle


class FilterTitle(QWidget, Widget_filterTitle):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(FilterTitle, self).__init__(parent)
        self.setupUi(self)

        self.result = []
        self.cbList = self.widget.findChildren(QCheckBox)
        self.setWindowFlags(Qt.WindowTitleHint|Qt.WindowCloseButtonHint)
        self.signalConnect()

    def signalConnect(self):
        # 全选
        self.pb_selectAll.clicked.connect(self.slotSelectAll)
        # 反选
        self.pb_inverse.clicked.connect(self.slotInverse)
        # 确定
        self.pb_Yes.clicked.connect(self.slotSave)

    def slotSelectAll(self):
        for i in self.cbList:
            if not i.isChecked():
                i.setChecked(1)

    def slotInverse(self):
        for i in self.cbList:
            if i.isChecked():
                i.setChecked(0)
            else:
                i.setChecked(1)


    def slotSave(self):
        self.result = []
        for info in self.cbList:
            if info.isChecked():
                # info1 = info.objectName().split('cb_check')
                self.result.append(info.text())
        self.signal.emit('1')
        self.close()

