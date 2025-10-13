import sys
import logging

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
                            QSizePolicy, QGridLayout, QLayout, QTableView, QLineEdit,
                            QPushButton, QFrame)
from PyQt5.QtGui import QFont, QIcon, QPixmap

from Views.BaseViews.SelectableLabel  import SelectableLabel
from Views.BaseViews.DigitalSignatureWidget  import DigitalSignatureWidget
from Views.BaseViews.AdjustableLineEdit  import AdjustableLineEdit
from Views.BaseViews.IconButton  import IconButton
from Views.IView import IView
from Views.TableWidget import TableWidget
from Utils.Helper  import (VLayoutBuilder, HLayoutBuilder, GridLayoutBuilder,
                        Spliter)
from Utils.Constant  import *
from Utils.DataTypes  import Action, ActionMessage

class MainWidget(QWidget, IView):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        IView.__init__(self, parent)
        self._buttons = dict()
        self._initUi()

    def _initUi(self):
        # Left Widget
        leftWidget = QWidget(self)
        leftWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        leftVLayout = QVBoxLayout()
        leftComponents = list()
        self._initGeneralWidgets()
        # Ma co quan thue
        leftComponents.append(
            HLayoutBuilder().addWidget(QLabel("Mã cơ quan thuế:", self), color=LABEL_TITLE_COLOR)
                        .addWidget(self._generalWidgets["MCCQT"])
                        .addWidget(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
                        .build())
        # NBan + NMua + TTChung
        layoutBuilder = GridLayoutBuilder()
        leftComponents.append( layoutBuilder
            # NBan
            .addWidget(QLabel("Đơn vị bán hàng:", self), 0, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["Ten"], 0, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 0, 3, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["MST"], 0, 4)
            .addWidget(QLabel("Địa chỉ:", self), 1, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["DChi"], 1, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 2, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["Sdt"], 2, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 2, 2, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["Email"], 2, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 3, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["Stk"], 3, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 3, 2, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NBan"]["NganHang"], 3, 3, 1, 2)
            .addWidget(self.__createBorder(), 4, 0, 1, 8)
            # NMua
            .addWidget(QLabel("Họ tên người mua hàng:", self), 5, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["HVTNMHang"], 5, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Đơn vị bán hàng:", self), 6, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["Ten"], 6, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Mã số thuế:", self), 6, 3, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["MST"], 6, 4)
            .addWidget(QLabel("Địa chỉ:", self), 7, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["DChi"], 7, 1, 1, 2, minW=MIN_LABEL_WIDTH_TEXT)
            .addWidget(QLabel("Số điện thoại:", self), 8, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["Sdt"], 8, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Email:", self), 8, 2, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["Email"], 8, 3, 1, 2)
            .addWidget(QLabel("Số tài khoản:", self), 9, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["Stk"], 9, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Ngân hàng:", self), 9, 2, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["NMua"]["NganHang"], 9, 3, 1, 2)
            # TTChung
            .addWidget(QLabel("Hình thức thanh toán:", self), 10, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["HTTToan"], 10, 1, 1, 1, minW=MIN_LABEL_WIDTH_NUMBER)
            .addWidget(QLabel("Loại tiền:", self), 10, 2, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["DVTTe"], 10, 3, 1, 2)
            .addWidget(QLabel("Tỷ giá:", self), 10, 4, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["TGia"], 10, 5, 1, 2)
            .build())
        # Table DS dich vu
        leftComponents.append(self._tableWidget)
        # TToan
        layoutBuilder = GridLayoutBuilder()
        leftComponents.append(layoutBuilder
            .addWidget(QLabel("Thuế xuất GTGT:", self), 0, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TToan"]["LTSuat"]["TSuat"], 0, 1)
            .addWidget(QLabel("Tổng tiền chưa thuế:", self), 0, 3, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TToan"]["TgTCThue"], 0, 4, align=Qt.AlignRight)
            .addWidget(QLabel("Tổng tiền chiết khấu:", self), 1, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TToan"]["TTCKTMai"], 1, 1)
            .addWidget(QLabel("Tiền thuế GTGT:", self), 1, 3, align=Qt.AlignRight, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TToan"]["LTSuat"]["TThue"], 1, 4, align=Qt.AlignRight)
            .addWidget(QLabel("Tổng tiền bằng chữ:", self), 2, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TToan"]["TgTTTBChu"], 2, 1)
            .addWidget(QLabel("Tổng cộng tiền thanh toán:", self), 2, 3, align=Qt.AlignRight, isBold=True)
            .addWidget(self._generalWidgets["TToan"]["TgTTTBSo"], 2, 4, align=Qt.AlignRight)
            .addWidget(QLabel("Giải pháp Hóa đơn Điện tử:", self), 3, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["GPHDDT"], 3, 1, 1, 3)
            .addWidget(self._generalWidgets["TToan"]["ThongTinThue"], 4, 0, 1, 3)
            .build())
        # Duong dan file xml
        layoutBuilder = GridLayoutBuilder()
        leftComponents.append(layoutBuilder
            .addWidget(QLabel("Đương dẫn file xml:", self), 0, 1, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["XmlFilePath"], 0, 2)
            .build())

        for index, component in enumerate(leftComponents):
            if isinstance(component, QLayout):
                leftVLayout.addLayout(component)
            if isinstance(component, QTableView):
                leftVLayout.addWidget(component)

            if index < len(leftComponents) - 1:
                leftVLayout.addWidget(self.__createBorder())

        # Add vSpacer
        leftWidget.setLayout(leftVLayout)

        # Right Widget
        rightWidget = QWidget(self)
        rightVLayout = QVBoxLayout()
        rightComponents = list()
        # Tieu de hoa don
        layoutBuilder = GridLayoutBuilder()
        rightComponents.append(layoutBuilder
            .addWidget(QLabel("Mẫu số - ký hiệu:", self), 0, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["KHHDon"], 0, 1)
            .addWidget(QLabel("Số hóa đơn:", self), 1, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["SHDon"], 1, 1)
            .addWidget(QLabel("Ngày lập:", self), 2, 0, color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["TTChung"]["NLap"], 2, 1)
            .build())
        # Chu ki so nguoi ban
        layoutBuilder = VLayoutBuilder()
        rightComponents.append(layoutBuilder
            .addWidget(QLabel("Người bán hàng:", self), color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["DSCKS"]["NBan"])
            .build())
        # Chu ki so nguoi mua
        layoutBuilder = VLayoutBuilder()
        rightComponents.append(layoutBuilder
            .addWidget(QLabel("Người mua hàng:", self), color=LABEL_TITLE_COLOR)
            .addWidget(self._generalWidgets["DSCKS"]["NMua"])
            .build())
        # Init buttons
        self._initButtons()
        # Page control
        layoutBuilder = HLayoutBuilder()
        pageWidget = QWidget(self)
        pageWidget.setLayout(layoutBuilder \
            .addWidget(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) \
            .addWidget(self._buttons[Action.PREV_PAGE]) \
            .addWidget(QLabel("Hóa đơn:", self), color=LABEL_TITLE_COLOR) \
            .addWidget(self._generalWidgets["CurrentPage"]) \
            .addWidget(self._generalWidgets["TotalPage"]) \
            .addWidget(self._buttons[Action.NEXT_PAGE]) \
            .addWidget(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)) \
            .build())
        pageWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        rightComponents.append(pageWidget)
        # Buttons control
        layoutBuilder = VLayoutBuilder()
        rightComponents.append(layoutBuilder
            .addWidget(self._buttons[Action.EXPORT_ONE_EXCEL], align=Qt.AlignCenter)
            .addWidget(self._buttons[Action.EXPORT_ALL_EXCEL], align=Qt.AlignCenter)
            .build())

        for index, component in enumerate(rightComponents):
            if isinstance(component, QLayout):
                rightVLayout.addLayout(component)
            if isinstance(component, QWidget):
                rightVLayout.addWidget(component)

            if index < len(leftComponents) - 1:
                rightVLayout.addWidget(self.__createBorder())

        rightVLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        rightWidget.setLayout(rightVLayout)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(leftWidget)
        mainLayout.addWidget(rightWidget)
        self.setLayout(mainLayout)

    def _initGeneralWidgets(self):
        # Ma co quan thue
        self._generalWidgets["MCCQT"] = SelectableLabel("", self)
        # NBan
        self._generalWidgets["NBan"] = dict()
        self._generalWidgets["NBan"]["Ten"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["MST"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["DChi"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["Sdt"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["Email"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["Stk"] = SelectableLabel("", self)
        self._generalWidgets["NBan"]["NganHang"] = SelectableLabel("", self)
        # NMua
        self._generalWidgets["NMua"] = dict()
        self._generalWidgets["NMua"]["HVTNMHang"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["Ten"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["MST"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["DChi"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["Sdt"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["Email"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["Stk"] = SelectableLabel("", self)
        self._generalWidgets["NMua"]["NganHang"] = SelectableLabel("", self)
        # TTChung
        self._generalWidgets["TTChung"] = dict()
        self._generalWidgets["TTChung"]["HTTToan"] = SelectableLabel("", self)
        self._generalWidgets["TTChung"]["DVTTe"] = SelectableLabel("", self)
        self._generalWidgets["TTChung"]["TGia"] = SelectableLabel("", self)
        self._generalWidgets["TTChung"]["KHHDon"] = SelectableLabel("", self)
        self._generalWidgets["TTChung"]["SHDon"] = SelectableLabel("", self)
        self._generalWidgets["TTChung"]["NLap"] = SelectableLabel("", self)
        # TToan
        self._generalWidgets["TToan"] = dict()
        self._generalWidgets["TToan"]["ThongTinThue"] = QLabel("Xem thông tin chi tiết từng loại thuế xuất <a href=\"https://www.google.com/\">Click vào đây!</a>", self)
        self._generalWidgets["TToan"]["ThongTinThue"].setTextFormat(Qt.RichText)
        self._generalWidgets["TToan"]["ThongTinThue"].setTextInteractionFlags(Qt.TextBrowserInteraction)
        self._generalWidgets["TToan"]["ThongTinThue"].setOpenExternalLinks(True)
        self._generalWidgets["TToan"]["TgTCThue"] = SelectableLabel("", self)
        self._generalWidgets["TToan"]["LTSuat"] = dict()
        self._generalWidgets["TToan"]["LTSuat"]["TSuat"] = SelectableLabel("", self)
        self._generalWidgets["TToan"]["LTSuat"]["TThue"] = SelectableLabel("", self)
        self._generalWidgets["TToan"]["TTCKTMai"] = SelectableLabel("", self)
        self._generalWidgets["TToan"]["TgTTTBSo"] = SelectableLabel("", self)
        self._generalWidgets["TToan"]["TgTTTBChu"] = SelectableLabel("", self)
        # Giai phap HDDT
        self._generalWidgets["GPHDDT"] = SelectableLabel("", self)
        # Khac
        self._generalWidgets["XmlFilePath"] = QLineEdit("", self)
        self._generalWidgets["XmlFilePath"].setReadOnly(True)
        self._generalWidgets["XmlFilePath"].setStyleSheet("QLineEdit[readOnly=\"true\"] { color: #000000; background-color: #F0F0F0; }")
        # Chu ky so
        self._generalWidgets["DSCKS"] = dict()
        self._generalWidgets["DSCKS"]["NBan"] = DigitalSignatureWidget(self,
            "CÔNG TY TNHH BỆNH VIỆN ĐKTN AN SINH - PHÚC TRƯỜNG MINH",
            "2025-09-06",
            True)
        self._generalWidgets["DSCKS"]["NMua"] = DigitalSignatureWidget(self,
            "CÔNG TY Invoice Tool",
            "2025-09-17",
            False)
        # Chu ky so
        self._generalWidgets["CurrentPage"] = AdjustableLineEdit("0", self)
        self._generalWidgets["CurrentPage"].editingFinished.connect(
            self.onCurrentPageEditingFinished)
        self._generalWidgets["TotalPage"] = QLabel("/ 0", self)

    def _initButtons(self):
        # Page control
        self._buttons[Action.PREV_PAGE] = QPushButton("<",self)
        self._buttons[Action.PREV_PAGE].setFixedSize(32, 32)
        self._buttons[Action.PREV_PAGE].clicked.connect(
            lambda: self._controller.triggerAction(ActionMessage(Action.PREV_PAGE)))
        self._buttons[Action.PREV_PAGE].setEnabled(False)
        self._buttons[Action.NEXT_PAGE] = QPushButton(">",self)
        self._buttons[Action.NEXT_PAGE].setFixedSize(32, 32)
        self._buttons[Action.NEXT_PAGE].clicked.connect(
            lambda: self._controller.triggerAction(ActionMessage(Action.NEXT_PAGE)))
        self._buttons[Action.NEXT_PAGE].setEnabled(False)
        # Export one file excel
        self._buttons[Action.EXPORT_ONE_EXCEL] = IconButton(ICON_ONE_EXCEL_PATH, "Xuất 1 HĐ ra Excel", self)
        self._buttons[Action.EXPORT_ONE_EXCEL].clicked.connect(lambda x: self.onExportExcelClicked(isAll=False))
        # Export all files excel
        self._buttons[Action.EXPORT_ALL_EXCEL] = IconButton(ICON_EXCEL_PATH, "Xuất tất cả HĐ ra Excel", self)
        self._buttons[Action.EXPORT_ALL_EXCEL].clicked.connect(lambda x: self.onExportExcelClicked(isAll=True))

    def __createBorder(self):
        border = QFrame()
        border.setFrameShape(QFrame.HLine)
        border.setFrameShadow(QFrame.Sunken)
        border.setLineWidth(2)
        return border

    def onExportExcelClicked(self, isAll=False):
        if isAll:
            self._controller.triggerAction(ActionMessage(Action.EXPORT_ALL_EXCEL))
        else:
            self._controller.triggerAction(ActionMessage(Action.EXPORT_ONE_EXCEL))

    def onPrevPageClicked(self):
        self._controller.triggerAction(ActionMessage(Action.EXPORT_ALL_EXCEL))

    def onNextPageClicked(self):
        self._controller.triggerAction(ActionMessage(Action.EXPORT_ALL_EXCEL))

    def onCurrentPageEditingFinished(self):
        if (not self._generalWidgets["CurrentPage"].isModified()):
            return
        self._generalWidgets["CurrentPage"].setModified(False)
        self._controller.triggerAction(
            ActionMessage(
                Action.SET_CURRENT_PAGE, 
                {Action.page: self._generalWidgets["CurrentPage"].text()}
            ))

    def onCurrentPageUpdated(self, page):
        super().onCurrentPageUpdated(page)
        if page == self._model.totalPage() - 1:
            self._buttons[Action.NEXT_PAGE].setEnabled(False)
            self._buttons[Action.PREV_PAGE].setEnabled(True)
        elif page == 0:
            self._buttons[Action.NEXT_PAGE].setEnabled(True)
            self._buttons[Action.PREV_PAGE].setEnabled(False)
        else:
            self._buttons[Action.NEXT_PAGE].setEnabled(True)
            self._buttons[Action.PREV_PAGE].setEnabled(True)

    def onTotalPageUpdated(self, total):
        super().onTotalPageUpdated(total)
        self._generalWidgets["TotalPage"].setText(f" / {str(total)}")
        if total <= 1:
            self._buttons[Action.PREV_PAGE].setEnabled(False)
            self._buttons[Action.NEXT_PAGE].setEnabled(False)
