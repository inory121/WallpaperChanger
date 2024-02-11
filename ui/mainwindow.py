import sys
from PyQt5.QtCore import QThread
from utils.log_util import logger
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from utils.wallpaper_change import change_wallpaper
from utils.wallpaper_downloader import ImageDownloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建一个ImageDownloader实例
        self.download_thread = None
        self.downloader = ImageDownloader()
        self.download_thread = QThread()
        self.downloader.moveToThread(self.download_thread)
        # 将finished信号连接到处理槽
        self.downloader.finished.connect(self.download_finished)
        self.setWindowTitle("Wallpaper Changer")
        change_button = QPushButton("Change Wallpaper", self)
        download_button = QPushButton("Download Wallpaper", self)
        change_button.clicked.connect(change_wallpaper)
        download_button.clicked.connect(self.start_download)
        layout = QVBoxLayout()
        layout.addWidget(change_button)
        layout.addWidget(download_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            logger.warning("下载线程已经在运行中...")
            return
        try:
            self.download_thread.started.connect(self.downloader.start_download)
            self.download_thread.start()
        except Exception as e:
            logger.error(f"An error occurred while starting download: {str(e)}")

    def download_finished(self):
        print("Download finished!")
        self.download_thread.quit()
        self.download_thread.wait()


def run_gui_app():
    logger.info('Starting the GUI application...')
    app = QApplication(sys.argv)
    main_win = MainWindow()
    # 设置窗口大小为宽度800像素，高度600像素
    main_win.resize(400, 300)
    main_win.show()
    sys.exit(app.exec_())
