import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #내장함수 super를 이용한다.


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()

# x를 누를때까지 창이 꺼지지 않도록 해준다.