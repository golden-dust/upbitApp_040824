import sys
import time

import requests

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

form_class = uic.loadUiType("ui/upbitMain_ver2.ui")[0]
# REMEMBER!! index [0]!!

# signal class -> request coin info to upbit server
class UpbitCall(QThread):
    # defining signal function
    coinSignal = pyqtSignal(float, float, float, float, float, float, float, float)  # 실수 8개 (현재가~변화율)

    def run(self):
        while True: # 무한루프 (실전에서는 나중에 멈추게 해야 함)

            url = "https://api.upbit.com/v1/ticker"
            param = {"markets": "KRW-BTC"}

            response = requests.get(url, params=param)
            # 혹은 아예 파라미터를 넣은 url을 써도 됨
            # "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
            # parameter를 분리하면 나중에 바꾸기 쉬움

            result = response.json()
            # print(result)

            trade_price = result[0]['trade_price']    # 비트코인 현재가격
            high_price = result[0]['high_price']      # 고가
            low_price = result[0]['low_price']        # 저가
            prev_closing_price = result[0]['prev_closing_price']        # 종가
            trade_volume = result[0]['trade_volume']                    # 거래량
            acc_trade_volume_24h = result[0]['acc_trade_volume_24h']    # 24h 누적 거래량
            acc_trade_price_24h = result[0]['acc_trade_price_24h']      # 24h 누적 거래액
            signed_change_rate = result[0]['signed_change_rate']        # 변화율

            self.coinSignal.emit(
                float(trade_price),
                float(high_price),
                float(low_price),
                float(prev_closing_price),
                float(trade_volume),
                float(acc_trade_volume_24h),
                float(acc_trade_price_24h),
                float(signed_change_rate)
            )

            # 업비트 api 호출 딜레이 2초
            time.sleep(2)


class MainWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # ui 불러오기
        self.setWindowTitle("BitCoin Info App v0.7")
        self.statusBar().showMessage("Upbit API Application Ver 0.7")

        self.ubc = UpbitCall()  # signal class로 객체 선언
        self.ubc.coinSignal.connect(self.fillCoinData)
        self.ubc.start()



    @pyqtSlot(float, float, float, float, float, float, float, float)
    def fillCoinData(
            self, trade_price, high_price, low_price, prev_closing_price, trade_volume, acc_trade_volume_24h, acc_trade_price_24h, signed_change_rate):

        self.trade_price.setText(f"{trade_price:,.0f}")
        print(trade_price)
        self.high_price.setText(f"{high_price:,.0f}")
        self.low_price.setText(f"{low_price:,.0f}")
        self.closing_price.setText(f"{prev_closing_price:,.0f}")
        self.trade_volume.setText(f"{trade_volume:,.3f}")
        self.trade_volume_24h.setText(f"{acc_trade_volume_24h:,.3f}")
        self.trade_price_24h.setText(f"{acc_trade_price_24h:,.0f}")
        self.change_rate.setText(f"{signed_change_rate:.8f}")
        self.update_style()

    def update_style(self): # 변화율이 +이면 빨간색, -이면 파란색으로 표시
        if '-' in self.change_rate.text():
            self.change_rate.setStyleSheet("background-colo:blue;color:white;")
            self.trade_price.setStyleSheet("color:blue;")
        else:
            self.change_rate.setStyleSheet("background-color:red;color:white;")
            self.trade_price.setStyleSheet("color:red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exit(app.exec_())