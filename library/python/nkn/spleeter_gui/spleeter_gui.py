import sys

import os
import subprocess
from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from nkn.core import (
    config,
)
from nkn.gui import (
    appearance,
    log,
)
from nkn.spleeter_gui.spleeter_gui_ui import Ui_MainWindow

APP_NAME = 'SpleeterGui'
__version__ = '0.1.0'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(f'{APP_NAME} {__version__}')
        self.setWindowFlags(
            Qt.Window
        )
        self.resize(500, 500)

        # combo box
        w = self.ui.modelComboBox
        w.addItem('2stems')
        w.addItem('4stems')
        w.addItem('5stems')
        w.setCurrentIndex(0)

        # event
        self.ui.srcToolButton.clicked.connect(self.srcToolButton_clicked)
        self.ui.dstToolButton.clicked.connect(self.dstToolButton_clicked)

        self.ui.splitButton.clicked.connect(self.split)
        self.ui.closeButton.clicked.connect(self.close)

    def split(self) -> None:
        self.ui.logTextEdit.clear()
        self.add2log('processing...')

        # get data
        src = Path(self.ui.srcLineEdit.text())
        if not src.is_file():
            self.add2log('Audio File: Not Found', log.ERROR_COLOR)
        dst_text = self.ui.dstLineEdit.text().strip()
        if dst_text == '':
            self.add2log('Output Directory: Not Found', log.ERROR_COLOR)
        dst = Path(dst_text)
        if not dst.is_dir():
            self.add2log('Output Directory: Not Found', log.ERROR_COLOR)
        model = self.ui.modelComboBox.currentText()

        args = [
            'separate',
            '-p',
            f'spleeter:{model}',
            '-o',
            str(dst),
            str(src),
        ]
        cmd = [
                  'spleeter.exe',
              ] + args
        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
            )

            buf = []
            while True:
                data = proc.stdout.readline()
                line = data.decode('utf-8').rstrip()
                buf.append(line)
                self.add2log(line)

                if not line and proc.poll() is not None:
                    break
            self.add2log('done!')

        except Exception as e:
            self.add2log(str(e), log.ERROR_COLOR)

    def srcToolButton_clicked(self) -> None:

        w = self.ui.srcLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select Audio File',
            w.text(),
            'Audio File (*.*)',
        )
        if path != '':
            w.setText(path)

    def dstToolButton_clicked(self) -> None:
        w = self.ui.dstLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)


def run() -> None:
    os.environ['PATH'] = os.pathsep.join([
        str(config.BIN_PATH),
        str(config.PYTHON_INSTALL_PATH),
        str(config.PYTHON_SCRIPTS_PATH),
        os.getenv('PATH'),
    ])

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
