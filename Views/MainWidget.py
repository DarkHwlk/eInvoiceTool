import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                             QSizePolicy, QGridLayout)

from Views.BaseViews.SelectableLabel  import SelectableLabel
from Utils.Helper  import SpacerPos, HLayoutBuilder, GridLayoutBuilder

MIN_LABEL_WIDTH_TEXT = 500
MIN_LABEL_WIDTH_NUMBER = 500

class MainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.generalWidgets = dict()
        self.initUi()

    def initUi(self):
        widget = QWidget(self)
        mainLayout = QVBoxLayout()
        componentLayouts = list()
        self.initGeneralWidgets()
        # Ma co quan thue
        layoutBuilder = HLayoutBuilder()
        componentLayouts.append(
            layoutBuilder.addWidget(QLabel("Mã cơ quan thuế:", self))
                        .addWidget(self.generalWidgets["MaCoQuanThue"])
                        .addWidget(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
                        .build())

        layoutBuilder = GridLayoutBuilder()
        componentLayouts.append( layoutBuilder
            # NBan
            .addWidget(QLabel("Đơn vị bán hàng:", self), 0, 0)
            .addWidget(self.generalWidgets["NBan"]["Ten"], 0, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 0, 3)
            .addWidget(self.generalWidgets["NBan"]["MST"], 0, 4)
            .addWidget(QLabel("Địa chỉ:", self), 1, 0)
            .addWidget(self.generalWidgets["NBan"]["DChi"], 1, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 2, 0)
            .addWidget(self.generalWidgets["NBan"]["Sdt"], 2, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 2, 2, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["NBan"]["Email"], 2, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 3, 0)
            .addWidget(self.generalWidgets["NBan"]["Stk"], 3, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 3, 2, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["NBan"]["NganHang"], 3, 3, 1, 2)
            # NMua
            .addWidget(QLabel("Họ tên người mua hàng:", self), 4, 0)
            .addWidget(self.generalWidgets["NMua"]["HVTNMHang"], 4, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Đơn vị bán hàng:", self), 5, 0)
            .addWidget(self.generalWidgets["NMua"]["Ten"], 5, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 5, 3)
            .addWidget(self.generalWidgets["NMua"]["MST"], 5, 4)
            .addWidget(QLabel("Địa chỉ:", self), 6, 0)
            .addWidget(self.generalWidgets["NMua"]["DChi"], 6, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 7, 0)
            .addWidget(self.generalWidgets["NMua"]["Sdt"], 7, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 7, 2, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["NMua"]["Email"], 7, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 8, 0)
            .addWidget(self.generalWidgets["NMua"]["Stk"], 8, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 8, 2, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["NMua"]["NganHang"], 8, 3, 1, 2)
            # TTChung
            .addWidget(QLabel("Hình thức thanh toán:", self), 9, 0)
            .addWidget(self.generalWidgets["TTChung"]["HTTToan"], 9, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Loại tiền:", self), 9, 2, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["TTChung"]["DVTTe"], 9, 3, 1, 2)
            .addWidget(QLabel("Tỷ giá:", self), 9, 4, align=Qt.AlignRight)
            .addWidget(self.generalWidgets["TTChung"]["TGia"], 9, 5, 1, 2)
            .build())

        for layout in componentLayouts:
            mainLayout.addLayout(layout)
            # TODO: add spliter
        # Add vSpacer
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(mainLayout)

    def initGeneralWidgets(self):
        self.generalWidgets["MaCoQuanThue"] = SelectableLabel("ABCXYZ", self)

        self.generalWidgets["NBan"] = dict()
        self.generalWidgets["NBan"]["Ten"] = SelectableLabel("CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH", self)
        self.generalWidgets["NBan"]["MST"] = SelectableLabel("0106793535", self)
        self.generalWidgets["NBan"]["DChi"] = SelectableLabel("Số 8 đường Châu Văn Liêm, Phường Từ Liêm, Thành phố Hà Nội, Việt Nam", self)
        self.generalWidgets["NBan"]["Sdt"] = SelectableLabel("0356085567", self)
        self.generalWidgets["NBan"]["Email"] = SelectableLabel("", self)
        self.generalWidgets["NBan"]["Stk"] = SelectableLabel("", self)
        self.generalWidgets["NBan"]["NganHang"] = SelectableLabel("", self)
        
        self.generalWidgets["NMua"] = dict()
        self.generalWidgets["NMua"]["HVTNMHang"] = SelectableLabel("Đặng Khánh Hưng (03820000621)", self)
        self.generalWidgets["NMua"]["Ten"] = SelectableLabel("CÔNG TY TNHH FPT", self)
        self.generalWidgets["NMua"]["MST"] = SelectableLabel("0106793535", self)
        self.generalWidgets["NMua"]["DChi"] = SelectableLabel("129 Nguyễn Trãi, Phường Khương Đình, Thành phố Hà Nội", self)
        self.generalWidgets["NMua"]["Sdt"] = SelectableLabel("0356085567", self)
        self.generalWidgets["NMua"]["Email"] = SelectableLabel("hungpro549@gmail.com", self)
        self.generalWidgets["NMua"]["Stk"] = SelectableLabel("", self)
        self.generalWidgets["NMua"]["NganHang"] = SelectableLabel("", self)

        self.generalWidgets["TTChung"] = dict()
        self.generalWidgets["TTChung"]["HTTToan"] = SelectableLabel("Tiền mặt/Chuyển khoản", self)
        self.generalWidgets["TTChung"]["DVTTe"] = SelectableLabel("VND", self)
        self.generalWidgets["TTChung"]["TGia"] = SelectableLabel("1", self)
