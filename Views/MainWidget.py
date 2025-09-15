import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy, QGridLayout, QLayout, QTableView, QLineEdit )
from PyQt5.QtGui import QFont

from Views.BaseViews.SelectableLabel  import SelectableLabel
from Views.IView import IView
from Views.TableWidget import TableWidget
from Utils.Helper  import SpacerPos, HLayoutBuilder, GridLayoutBuilder

MIN_LABEL_WIDTH_TEXT = 500
MIN_LABEL_WIDTH_NUMBER = 500

class MainWidget(QWidget, IView):
    def __init__(self, parent):
        super().__init__(parent)
        self._generalWidgets = dict()
        self._tableWidget = TableWidget(self)
        self.initUi()

    def initUi(self):
        widget = QWidget(self)
        mainLayout = QVBoxLayout()
        components = list()
        self.initGeneralWidgets()
        # Ma co quan thue
        layoutBuilder = HLayoutBuilder()
        components.append(
            layoutBuilder.addWidget(QLabel("Mã cơ quan thuế:", self), color="blue", isBold=True)
                        .addWidget(self._generalWidgets["MaCoQuanThue"])
                        .addWidget(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
                        .build())
        # NBan + NMua + TTChung
        layoutBuilder = GridLayoutBuilder()
        components.append( layoutBuilder
            # NBan
            .addWidget(QLabel("Đơn vị bán hàng:", self), 0, 0)
            .addWidget(self._generalWidgets["NBan"]["Ten"], 0, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 0, 3)
            .addWidget(self._generalWidgets["NBan"]["MST"], 0, 4)
            .addWidget(QLabel("Địa chỉ:", self), 1, 0)
            .addWidget(self._generalWidgets["NBan"]["DChi"], 1, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 2, 0)
            .addWidget(self._generalWidgets["NBan"]["Sdt"], 2, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 2, 2, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["NBan"]["Email"], 2, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 3, 0)
            .addWidget(self._generalWidgets["NBan"]["Stk"], 3, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 3, 2, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["NBan"]["NganHang"], 3, 3, 1, 2)
            # NMua
            .addWidget(QLabel("Họ tên người mua hàng:", self), 4, 0)
            .addWidget(self._generalWidgets["NMua"]["HVTNMHang"], 4, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Đơn vị bán hàng:", self), 5, 0)
            .addWidget(self._generalWidgets["NMua"]["Ten"], 5, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 5, 3)
            .addWidget(self._generalWidgets["NMua"]["MST"], 5, 4)
            .addWidget(QLabel("Địa chỉ:", self), 6, 0)
            .addWidget(self._generalWidgets["NMua"]["DChi"], 6, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 7, 0)
            .addWidget(self._generalWidgets["NMua"]["Sdt"], 7, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 7, 2, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["NMua"]["Email"], 7, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 8, 0)
            .addWidget(self._generalWidgets["NMua"]["Stk"], 8, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 8, 2, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["NMua"]["NganHang"], 8, 3, 1, 2)
            # TTChung
            .addWidget(QLabel("Hình thức thanh toán:", self), 9, 0)
            .addWidget(self._generalWidgets["TTChung"]["HTTToan"], 9, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Loại tiền:", self), 9, 2, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["TTChung"]["DVTTe"], 9, 3, 1, 2)
            .addWidget(QLabel("Tỷ giá:", self), 9, 4, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["TTChung"]["TGia"], 9, 5, 1, 2)
            .build())
        # Table DS dich vu
        components.append(self._tableWidget)
        # TToan
        layoutBuilder = GridLayoutBuilder()
        components.append(layoutBuilder
            .addWidget(self._generalWidgets["TToan"]["TTThue"], 0, 0, 1, 3)
            .addWidget(QLabel("Tổng tiền chưa thuế:", self), 0, 3, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["TToan"]["TgTCThue"], 0, 4, align=Qt.AlignRight)
            .addWidget(QLabel("Thuế xuất GTGT:", self), 1, 0)
            .addWidget(self._generalWidgets["TToan"]["TSuat"], 1, 1)
            .addWidget(QLabel("Tiền thuế GTGT:", self), 1, 3, align=Qt.AlignRight)
            .addWidget(self._generalWidgets["TToan"]["TThue"], 1, 4, align=Qt.AlignRight)
            .addWidget(QLabel("Tổng tiền bằng chữ:", self), 2, 0)
            .addWidget(self._generalWidgets["TToan"]["TgTTTBChu"], 2, 1)
            .addWidget(QLabel("Tổng cộng tiền thanh toán:", self), 2, 3, align=Qt.AlignRight, isBold=True)
            .addWidget(self._generalWidgets["TToan"]["TgTTTBSo"], 2, 4, align=Qt.AlignRight)
            .build())
        # Khac
        layoutBuilder = GridLayoutBuilder()
        components.append(layoutBuilder
            .addWidget(QLabel("Đương dẫn file xml:", self), 0, 1)
            .addWidget(self._generalWidgets["XmlFilePath"], 0, 2)
            .build())

        for component in components:
            if isinstance(component, QLayout):
                mainLayout.addLayout(component)
            if isinstance(component, QTableView):
                mainLayout.addWidget(component)
            # TODO: add spliter
        # Add vSpacer
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(mainLayout)

    def initGeneralWidgets(self):
        # Ma co quan thue
        self._generalWidgets["MaCoQuanThue"] = SelectableLabel("ABCXYZ", self)
        # NBan
        self._generalWidgets["NBan"] = dict()
        self._generalWidgets["NBan"]["Ten"] = SelectableLabel("CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH", self)
        self._generalWidgets["NBan"]["MST"] = SelectableLabel("0106793535", self)
        self._generalWidgets["NBan"]["DChi"] = SelectableLabel("Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam", self)
        self._generalWidgets["NBan"]["Sdt"] = SelectableLabel("0356085567", self)
        self._generalWidgets["NBan"]["Email"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["Stk"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["NganHang"] = SelectableLabel("", self)
        # NMua
        self._generalWidgets["NMua"] = dict()
        self._generalWidgets["NMua"]["HVTNMHang"] = SelectableLabel("Đặng Khánh Hưng (03820000621)", self)
        self._generalWidgets["NMua"]["Ten"] = SelectableLabel("CÔNG TY TNHH FPT", self)
        self._generalWidgets["NMua"]["MST"] = SelectableLabel("0106793535", self)
        self._generalWidgets["NMua"]["DChi"] = SelectableLabel("129 Nguyễn Trãi, Phường Khương Đình, Thành phố Hà Nội", self)
        self._generalWidgets["NMua"]["Sdt"] = SelectableLabel("0356085567", self)
        self._generalWidgets["NMua"]["Email"] = SelectableLabel("hungpro549@gmail.com", self)
        self._generalWidgets["NMua"]["Stk"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["NganHang"] = SelectableLabel("", self)
        # TTChung
        self._generalWidgets["TTChung"] = dict()
        self._generalWidgets["TTChung"]["HTTToan"] = SelectableLabel("Tiền mặt/Chuyển khoản", self)
        self._generalWidgets["TTChung"]["DVTTe"] = SelectableLabel("VND", self)
        self._generalWidgets["TTChung"]["TGia"] = SelectableLabel("1", self)
        # TToan
        self._generalWidgets["TToan"] = dict()
        self._generalWidgets["TToan"]["TTThue"] = QLabel("Xem thông tin chi tiết từng loại thuế xuất <a href=\"https://www.google.com/\">Click vào đây!</a>", self)
        self._generalWidgets["TToan"]["TTThue"].setTextFormat(Qt.RichText)
        self._generalWidgets["TToan"]["TTThue"].setTextInteractionFlags(Qt.TextBrowserInteraction)
        self._generalWidgets["TToan"]["TTThue"].setOpenExternalLinks(True)
        self._generalWidgets["TToan"]["TgTCThue"] = SelectableLabel("407.000", self)
        self._generalWidgets["TToan"]["TSuat"] = SelectableLabel("KCT", self)
        self._generalWidgets["TToan"]["TThue"] = SelectableLabel("0", self)
        self._generalWidgets["TToan"]["TgTTTBSo"] = SelectableLabel("407.000", self)
        self._generalWidgets["TToan"]["TgTTTBChu"] = SelectableLabel("Bốn trăm lẻ bảy nghìn đồng chẵn.", self)
        # Khac
        self._generalWidgets["XmlFilePath"] = QLineEdit("E:\\Hwng\\Projects\\Invoice Tool\\data\\K25TTM-00218251-UKVF96OM2K5-DPH.pdf", self)
        self._generalWidgets["XmlFilePath"].setReadOnly(True)
        self._generalWidgets["XmlFilePath"].setStyleSheet("QLineEdit[readOnly=\"true\"] { color: #000000; background-color: #F0F0F0; }")

    def setModel(self, model):
        print("MainView set model")
        self._model = model
        self._tableWidget.setModel(model)
