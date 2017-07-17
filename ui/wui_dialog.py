import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from ui.ui_dialog import Ui_Dialog

try:
    import requests
except ImportError:
    print('[!] Import Error, Try \'pip install requests\' and restart\n')
try:
    from virustotal import *
except ImportError:
    print('[!] Import Error, Visit https://github.com/jumpingwhale/virustotal and download package')


class WUi_Dialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, apikey):

        # 이 클래스를 사용하기 위해선 상속받은 부모를 초기화 해 줘야한다
        super(WUi_Dialog, self).__init__()

        # Designer 가 세팅해준 초기화 함수를 호출하자
        self.setupUi(self)

        # 다운로드 경로 설정
        home = os.path.expanduser("~")
        downloadpath = os.path.join(home, "Downloads")
        self.downloadPath.setText(downloadpath)

        # 추가로 들어갈 위젯이나.. 슬롯같은것들
        self.pushButton.clicked.connect(self.download)
        self.pushButton_path.clicked.connect(self.selectPath)
        self.pushButton_explore.clicked.connect(self.openExplorer)

        # 기타 필요 변수
        self.apiKey.setText(apikey)
        self.vt = VirusTotal([apikey, ], private=True)

    @pyqtSlot(name='openExplorer')
    def openExplorer(self):
        """다운로드 경로를 탐색기로 열어준다

        :return:
        """

        os.system('explorer.exe \"%s\"' % self.downloadPath.text())

    @pyqtSlot(name='download')
    def download(self):
        """다운로드 슬롯

        C++ 호환성을 위해 decorator 를 명시한다
        관련문서 - http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSlot
        :return:
        """

        # 입력 해쉬를 리스트화한다
        self.hashes = self.input_hashes.toPlainText().split('\n')

        # 해쉬별 다운로드 시도한다
        for hash in self.hashes:
            self.D('[+] Processing \'%s\'' % hash)
            try:
                sample = self.vt.download(hash)
            except Exception as e:
                self.D('%s' % str(e))
                continue

            # 결과값을 저장한다
            self.storeSample(hash, sample)

    @pyqtSlot(name='selectPath')
    def selectPath(self):
        """다운로드 경로설정 UI 출력 슬롯

        :return:
        """
        path = QtWidgets.QFileDialog.getExistingDirectory()
        self.downloadPath.setText(path)

    def storeSample(self, filename, sample):
        """샘플을 디스크에 저장한다

        :param filename: str, 일반적으로 MD5 해쉬
        :param sample: bytearray, 다운로드받은 데이터
        :return:
        """

        # 저장경로 설정
        path = os.path.join(self.downloadPath.text(), filename)

        # 저장
        with open(path, 'wb') as file:
            file.write(sample)

    def D(self, debugMsg, clear=False):
        """디버그 메시지 출력용 함수

        :param debugMsg: str, 디버그 문자열
        :param clear: bool, 디버깅창 초기화
        :return:
        """

        if clear:
            self.debugWnd.clear()
        self.debugWnd.insertPlainText(debugMsg + '\n')
