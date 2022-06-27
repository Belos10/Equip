
from PyQt5.QtWidgets import QMessageBox, QPushButton,QInputDialog
from PyQt5.QtCore import Qt

def getMessageBox(title:str, context:str, confirm:bool, cancce:bool):
    messageBox = QMessageBox()
    messageBox.setWindowTitle(title)
    messageBox.setText(context)
    if confirm:
        messageBox.addButton(QPushButton('确定'), QMessageBox.YesRole)
    if cancce:
        messageBox.addButton(QPushButton('取消'), QMessageBox.NoRole)
    execResult = messageBox.exec_()
    result = QMessageBox.Cancel
    if execResult == 0:
        result = QMessageBox.Ok
    return result

def getIntInputDialog(title:str, context:str,  floor:int, top: int, step: int, confirm:bool, cancce:bool):
    inputDialog = QInputDialog()
    inputDialog.setWindowFlags(Qt.CustomizeWindowHint  | Qt.WindowCloseButtonHint)
    inputDialog.setFixedSize(400, 400)
    inputDialog.setInputMode(QInputDialog.IntInput)
    inputDialog.setWindowTitle(title)
    inputDialog.setLabelText(context)
    inputDialog.setIntRange(floor, top)
    inputDialog.setIntStep(step)
    if confirm:
        inputDialog.setOkButtonText("确定")
    if cancce:
        inputDialog.setCancelButtonText("取消")
    value = -1
    ok = False
    if inputDialog.exec_() == QInputDialog.Accepted:
        value = inputDialog.intValue()
        ok = True
    return ok, value

def getDoubleInputDialog(title:str, context:str,  floor:float, top: float, step: int, confirm:bool, cancce:bool):
    inputDialog = QInputDialog()
    inputDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    inputDialog.setFixedSize(400, 400)
    inputDialog.setInputMode(QInputDialog.DoubleInput)
    inputDialog.setWindowTitle(title)
    inputDialog.setLabelText(context)
    inputDialog.setDoubleStep(step)
    inputDialog.setDoubleRange(floor, top)
    if confirm:
        inputDialog.setOkButtonText("确定")
    if cancce:
        inputDialog.setCancelButtonText("取消")
    value = -1
    ok = False
    if inputDialog.exec_() == QInputDialog.Accepted:
        value = inputDialog.doubleValue()
        ok = True
    return ok, value

def getTextInputDialog(title:str, context:str,  floor:float, top: float, step: int, confirm:bool, cancce:bool):
    inputDialog = QInputDialog()
    inputDialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    inputDialog.setFixedSize(400, 400)
    inputDialog.setInputMode(QInputDialog.TextInput)
    inputDialog.setWindowTitle(title)
    inputDialog.setLabelText(context)
    if confirm:
        inputDialog.setOkButtonText("确定")
    if cancce:
        inputDialog.setCancelButtonText("取消")
    text = ""
    ok = False
    if inputDialog.exec_() == QInputDialog.Accepted:
        text = inputDialog.doubleValue()
        ok = True
    return ok, text