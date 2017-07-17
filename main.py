import sys
import configparser
from ui.wui_dialog import WUi_Dialog
from PyQt5 import QtWidgets

CONFIG_FILE_NAME = 'config.ini.bak'


def main():

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    apikey = config['virustotal']['private']

    # GUI앱을 만들겠다
    app = QtWidgets.QApplication(sys.argv)

    # GUI클래스 원본(scorerule_ui.py)을 바로 가져다 써도 되지만,
    # 원본은 Designer.exe 에서 업데이트할 때 마다 초기화 된다
    # 따라서 기왕이면 원본을 상속받는 새 래핑 클래스를 선언해서 쓰자
    # W는 Wrap의 약자
    wui_dialog = WUi_Dialog(apikey)

    # 화면에 띄우자, show는 해당 클래스 내부에서 해도됨
    wui_dialog.show()

    # 실행하자, 끝내자
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
