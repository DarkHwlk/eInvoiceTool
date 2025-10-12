from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication, Qt
import sys
from Utils.Helper import singleton

@singleton
class MainThreadInvoker(QObject):
    __signal = pyqtSignal(object, tuple, dict)

    def __init__(self):
        super().__init__() 
        self.__signal.connect(self.__invoke_callback)

    def __invoke_callback(self, callback, args, kwargs):
        try:
            callback(*args, **kwargs)
        except Exception as e:
            print(f"Lỗi khi thực thi callback trong main thread: {e}", file=sys.stderr)

    def run(self, callback, *args, **kwargs):
        try:
            self.__signal.emit(callback, args, kwargs)
        except RuntimeError as e:
            print(f"Lỗi: Không thể chạy trên main thread. {e}", file=sys.stderr)
        except Exception as e:
            print(f"Lỗi không xác định khi phát tín hiệu: {e}", file=sys.stderr)
