import cv2
import pyzbar.pyzbar as pyzbar
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication
import sys
import os
import requests
import threading


class WebBrowser(QWebEngineView):

    def __init__(self, url, parent=None):
        super().__init__()
        self.load(QtCore.QUrl(url))
        self.show()

    def navigate(self, url):
        self.load(QtCore.QUrl(url))

    def createWindow(self, WebWindowType):
        return self


def decodeDisplay(image, color):
    barcodes = pyzbar.decode(image)
    barcodeType = ''
    barcodeData = ''
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(color, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        text = "({}){}".format(barcodeType, barcodeData)
        cv2.putText(color, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (225, 225, 225), 2)

        # 向终端打印条形码数据和条形码类型
        #print("Found {} : {}".format(barcodeType, barcodeData))

    return color, barcodeType, barcodeData

response = ''
res_rdy = False

def display(url, w):
    global response
    global res_rdy
    print(url)
    response = requests.get(url).text
    res_rdy = True



def detect(cam, w):
    global res_rdy
    camera = cv2.VideoCapture(cam)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    t = threading.Thread()
    while True:
        # 读取当前帧
        ret, frame = camera.read()
        color = frame
        # 转为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        im, codetype, codedata = decodeDisplay(gray, color)

        if codedata[0:4] == 'http':
            if not t.is_alive():
                t = threading.Thread(target=display, args=(codedata, w))
                t.setDaemon(True)
                t.start()

        if res_rdy:
            res_rdy = False
            print(response)
            lines = response.splitlines()
            code = lines[0][5:]
            word = lines[1][5:]
            print({'code': code, 'word': word})
            w.navigate(
                'file:///' + (os.path.abspath('.') + '/display.htm?code={}&word={}'.format(code, word)).replace('\\',
                                                                                                                '/'))


        cv2.imshow("camera", im)
        # 如果按键q则跳出本次循环
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    web = WebBrowser('about:blank')

    detect(0, web)

    app.exec_()



    #detect()
