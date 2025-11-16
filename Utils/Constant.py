import pathlib

PROJECT_PATH = str(pathlib.Path(__file__).parent.parent.absolute())
RESOURCE_PATH = PROJECT_PATH + "\\resources"

APP_ICON_PATH = RESOURCE_PATH + '/./app_icon.png'
ICON_OK_PATH = RESOURCE_PATH + '/./ok.png'
ICON_NOK_PATH = RESOURCE_PATH + '/./nok.png'
ICON_ONE_EXCEL_PATH = RESOURCE_PATH + '/./one_excel_icon.png'
ICON_EXCEL_PATH = RESOURCE_PATH + '/./excel_icon.png'

ICON_OK_RELATIVE_PATH = "./resources/ok.png"
ICON_NOK_RELATIVE_PATH = "./resources/nok.png"

MIN_LABEL_WIDTH_TEXT = 500
MIN_LABEL_WIDTH_NUMBER = 500
MAIN_BUTTON_WIDTH = 200

LABEL_TITLE_COLOR = "#3742fa"

TABLE_HEADER = ["STT"," Tên hàng hóa, dịch vụ","Đơn vị tính","Số lượng",
            "Đơn giá","Tiền chưa thuế","% Thuế","Tiền thuế","Thành tiền"]
TABLE_HEADER_TAG = [
    "STT", "THHDVu", "DVTinh", "SLuong", "DGia",
    "TCThue", "TSuat", "TThue", "ThTien"
]
