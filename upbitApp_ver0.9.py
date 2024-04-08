import sys
import time

import pyupbit
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

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True   # 무한루프를 막아줄 변수

    def run(self):
        while self.alive:   # 무한루프X / 필요에 따라 멈추게 설정

            url = "https://api.upbit.com/v1/ticker"
            param = {"markets": f"KRW-{self.ticker}"}
            # ticker를 받아 parameter로 사용 -> 매칭되는 정보 받아오기

            response = requests.get(url, params=param)

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

    # defining a function that stops the 'run' function from becoming an infinite loop
    def close(self):
        self.alive = False


class MainWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # ui 불러오기
        self.setWindowTitle("BitCoin Info App v0.9")
        self.setWindowIcon(QIcon("icon/Image20240408143645.png"))
        self.statusBar().showMessage("Upbit API Application Ver 0.9")

        # initial ticker = "BTC"
        self.ticker = "BTC"

        self.ubc = UpbitCall(self.ticker)  # signal class로 객체 선언
        self.ubc.coinSignal.connect(self.fillCoinData)
        self.ubc.start()

        self.combobox_setting()     # comboBox setting 실행
        self.coinComboBox.currentIndexChanged.connect(self.coin_combobox_seleted)

    # ui 속의 combo box에 항목 넣는 함수
    def combobox_setting(self):
        tickerList = pyupbit.get_tickers(fiat="KRW")    # 코인 종류(ticker list) 가져오기
        coinList = []

        # KRW-를 제거한 텍스트를 리스트로 생성
        for ticker in tickerList:
            coinList.append(ticker[4:])

        # 'BTC'를 제외한 나머지 리스트 오름차순으로 정렬
        coinList.remove("BTC")
        coinList = ["BTC"] + sorted(coinList)

        self.coinComboBox.addItems(coinList)

    # 콤보박스에서 새로운 코인 종류가 선택되었을 때 호출 함수
    def coin_combobox_seleted(self):
        selected_ticker = self.coinComboBox.currentText()
        self.ticker = selected_ticker
        self.ubc.close()    # 실행 루프 종료

        self.market_name.setText(self.ticker)

        # loop restarts with the new ticker
        self.ubc = UpbitCall(self.ticker)
        self.ubc.coinSignal.connect(self.fillCoinData)
        self.ubc.start()

    @pyqtSlot(float, float, float, float, float, float, float, float)
    def fillCoinData(
            self, trade_price, high_price, low_price, prev_closing_price, trade_volume, acc_trade_volume_24h, acc_trade_price_24h, signed_change_rate):

        print(self.ticker)
        self.trade_price.setText(f"{trade_price:,.0f}원")
        print(trade_price)
        self.high_price.setText(f"{high_price:,.0f}원")
        self.low_price.setText(f"{low_price:,.0f}원")
        self.closing_price.setText(f"{prev_closing_price:,.0f}원")
        self.trade_volume.setText(f"{trade_volume:,.3f}개")
        self.trade_volume_24h.setText(f"{acc_trade_volume_24h:,.3f}개")
        self.trade_price_24h.setText(f"{acc_trade_price_24h:,.0f}원")
        self.change_rate.setText(f"{signed_change_rate:.8f}%")
        print(signed_change_rate)
        self.update_style()
        # self.market_name.setText(f"{self.ticker}")

    def update_style(self):     # 변화율이 +이면 빨간색, -이면 파란색으로 표시
        if '-' in self.change_rate.text():
            self.change_rate.setStyleSheet("background-color:blue;color:white;")
            self.trade_price.setStyleSheet("color:blue;")
        else:
            self.change_rate.setStyleSheet("background-color:red;color:white;")
            self.trade_price.setStyleSheet("color:red;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exit(app.exec_())
