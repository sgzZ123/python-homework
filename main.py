from GUI import *
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(a.exec_())