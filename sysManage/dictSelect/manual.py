from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QVariant
from widgets.dictSelect.widget_manual import widget_manual
from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem
from docx import Document


class Manual(QWidget,widget_manual):
    def __init__(self,parent=None):
        super(Manual, self).__init__(parent)
        self.setupUi(self)
        self.initWord()
        self.initArticle()
        self.initHeading()




    def initWord(self):
        self.headingTxt={}
        self.allTxt= {}
        self.wordFile = Document('F:/Program/Python/NuclearManageSystem/装备性能手册.docx')
        for i,p in enumerate(self.wordFile.paragraphs):
            style_name = p.style.name

            self.allTxt[i]=p.text
            # print(p.row,p.text,sep=':')
            if style_name.startswith('Heading'):
                self.headingTxt[i]=p.text
                #print(style_name, p.text, sep=':')
        # print("self.allTxt",self.allTxt,"\nself.headingTxt = ",self.headingTxt)
        # stack = []
        # root = []
        # for i in self.headingTxt.values():
        #     stack.append(i)
        # root.append(self.tw_catalog)
        # self.initHeading(stack,root)


    def initHeading(self):
        for xx in self.headingTxt.values():
            item = QTreeWidgetItem()
            item.setText(0,xx)
            self.tw_catalog.addTopLevelItem(item)

        # while stack:
        #     EquipInfo = stack.pop(0)
        #     item = QTreeWidgetItem(root.pop(0))
        #     item.setText(0, EquipInfo)
        #     # self.second_treeWidget_dict[EquipInfo[0]] = item
        #     root.append(item)
        #     # result = selectEquipInfoByEquipUper(EquipInfo[0])
        #     # for resultInfo in result:
        #     #     stack.append(resultInfo)
        #     #     root.append(item)

    def initArticle(self):
        # self.tb_article.setFontPointSize(16)
        for p in self.wordFile.paragraphs:
            style_name = p.style.name
            if style_name.startswith('Title'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:24pt; font-weight:600;">%s</span></p>'% p.text)
            elif style_name.startswith('Heading 1'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:22pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 2'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:20pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 3'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:18pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 4'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:16pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Heading 5'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:14pt; font-weight:600;">%s</span></p>'%p.text)
            elif style_name.startswith('Normal'):
                self.tb_article.append('<p align="left" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; '
                                       'margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" '
                                       'font-size:12pt;">%s</span></p>'%p.text)



