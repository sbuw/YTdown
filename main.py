import os
import sys 
import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import *

class downloader(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = None

    def run(self):
        self.mysignal.emit('Прроцесс скачивания запущен!')

        with youtube_dl.YoutubeDL({}) as ydl:
            ydl.download([self.url])

        self.mysignal.emit('Процесс скачивания завершен!')
        self.mysignal.emit('finish')

    def init_args(self, url):
        self.url = url

class YoutubeDownloaderUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(YoutubeDownloaderUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()

        self.download_folder = None
        self.ui.pushButton_2.clicked.connect(self.get_folder)
        self.ui.pushButton.clicked.connect(self.start)
        self.mythread = downloader()
        self.mythread.mysignal.connect(self.handler)

    def start(self):
        if len(self.ui.lineEdit.text()) > 5:
            if self.download_folder != None:
                link = self.ui.lineEdit.text()
                self.mythread.init_args(link)
                self.mythread.start()
                self.locker(True)
            else:
              QtWidgets.QMessageBox.warning(self, "Ошибка", "Вы не выбрали папку!")  
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ссылка на видео не указана!")


    def init_ui(self):
        self.setWindowTitle('YTdown')

    def get_folder(self):
        self.download_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку для сохранения')
        os.chdir(self.download_folder)

    def handler(self, value):
        if value == 'finish':
            self.locker(False)
        else:
            self.ui.plainTextEdit.appendPlainText(value)

    def locker(self, lock_value):
        base = [self.ui.pushButton, self.ui.pushButton_2]

        for i in base:
            i.setDisabled(lock_value)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = YoutubeDownloaderUI()
    win.show()
    sys.exit(app.exec_())
