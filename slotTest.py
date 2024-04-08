import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# signal class / slot class 2개로 나눠서 만드릭
# 정보 받아오는 애와 출력하는 애?
# 분리하지 않으면 멈추게 되고, 실시간을 볼 수 없음
# 실시간으로 빠르게 자동으로 처리해야 하기 때문에 쓰레드, 시그널-슬롯 구조가 필요함

# signal class - signal 함수가 필요함
class SignalThread(QThread):
    # signal 함수(사실은 클래스)
    signal1 = pyqtSignal()
    # signal = pyqtSignal(실제값X, 윈도우로 전달할 값)
    signal2 = pyqtSignal(int, int)

    def run(self):
        self.signal1.emit() # emit() 자동완성 안됨
        self.signal2.emit(1000, 2000)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        # 위에서 만든 시그널 클래스 소환 -> 객체로
        signalClass = SignalThread()

        # signal 함수와 slot 함수를 연결
        signalClass.signal1.connect(self.signal1_print)
        signalClass.signal2.connect(self.signal2_print)

        # 실행
        signalClass.run()



    @pyqtSlot() # slot 함수임을 명시해줘야 함
    def signal1_print(self):    # slot 함수
        print("signal emitted")

    @pyqtSlot(int, int) # slot 함수 명시 + 매개변수 타입 명시
    def signal2_print(self, int1, int2):
        print(f"signal emitted -> {int1}, {int2}")
        # 실제 프로그램에서는 윈도우에 출력하는 내용이 와야 함 (연습이라 콘솔에 출력)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exit(app.exec_())
