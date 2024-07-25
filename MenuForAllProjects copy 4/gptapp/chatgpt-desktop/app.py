import os
import sys
import markdown
from datetime import datetime
from configparser import ConfigParser
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QSlider,
                             QTabWidget, QTextEdit, QTextBrowser, QMenu, QMenuBar, QSplitter,
                             QToolButton, QStatusBar,
                             QHBoxLayout, QVBoxLayout, QFormLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QEvent, QThread
from PyQt6.QtGui import QIcon, QTextCursor
from chatgpt import ChatGPT
from db import ChatGPTDatabase

def current_timestamp(format_pattern='%y_%m_%d_%H%M%S'):
    return datetime.now().strftime(format_pattern)

class ChatGPTThread(QThread):
    requestFinished = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self._stopped = True
        self.parent = parent


class AIAssistant(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.chatgpt = ChatGPT(API_KEY)
        self.t = ChatGPTThread(self)

        self.layout = {}
        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

    def init_ui(self):
        # add sub layout manager
        self.layout['inputs'] = QFormLayout

        # add sliders
        self.max_tokens = QSlider(Qt.Orientation.Horizontal, minimum=10, maximum=4096, singleStep=500, pageStep=500, value=200, toolTip='Maximum token ChatGpt can consume')
        self.temperature = QSlider(Qt.Orientation.Horizontal, minimum=0, maximum=200, value=10, toolTip='Randomess of the response')
class TabManager(QTabWidget):
    # add customized signals
    plusClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # add tab close button
        self.setTabsClosable(True)

        # Create the add tab button and implement signals
        self.add_tab_button = QToolButton(self, text='+')
        self.add_tab_button.clicked.connect(self.plusClicked)
        self.setCornerWidget(self.add_tab_button)

        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, tab_index):
        if self.count() == 1:
            return
        self.removeTab(tab_index)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.window_wodth, self.window_height = 720, 720
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'robot.png')))
        self.setWindowTitle('ChatGPT AI Assistant (By Ziaire Braggs) v1')
        self.setStyleSheet('''
            QWidget {
                font-size: 15px;
            }
        ''')
        self.tab_index_tracker = 1
        self.layout = {}

        self.layout['main'] = QVBoxLayout()
        self.setLayout(self.layout['main'])

        self.init_ui()
        self.init_configure_signal()

    def init_ui(self):
        # add tab manager
        self.tab_manager = TabManager()
        self.layout['main'].addWidget(self.tab_manager)

        ai_assistant = AIAssistant()
        self.tab_manager.addTab(AIAssistant(), 'Conversation #{0}'.format(self.tab_index_tracker))
        self.set_tab_focus()

    def set_tab_focus(self):
        activate_tab = self.tab_manager.currentWidget()
        # activate_tab.message_input.setFocus()

    def add_tab(self):
        self.tab_index_tracker += 1
        ai_assistant = AIAssistant()
        self.tab_manager.addTab(ai_assistant, 'Conversation #{0}'.format(self.tab_index_tracker))
        self.tab_manager.setCurrentIndex(self.tab_manager.count()-1)
        self.set_tab_focus()

    def init_configure_signal(self):
        self.tab_marager.plusClicked.connect(self.add_tab)

if __name__ == '__main__':
    # load openai API key
    config = ConfigParser()
    config.read('api_key.ini')
    API_KEY = config.get('openai', 'APIKEY')
    # init ChatGPT SQLite database
    db = ChatGPTDatabase('chatgpt.db')
    db.create_table(
        'message_logs ',
        '''
            message_log_no INTEGER PRIMARY KEY AUTOINCREMENT,
            messages TEXT,
            created TEXT
        '''
    )
    # construct application instance
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    qss_style = open(os.path.join(os.getcwd(), 'css_skins/dark_orange_style.qss'), 'r')
    app.setStyleSheet(qss_style.read())
    # launch app window
    app_window = AppWindow()
    app_window.show()
    sys.exit(app.exec())