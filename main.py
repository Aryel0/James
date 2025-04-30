import sys 
import os
import jamesllm
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextBrowser, QLineEdit
    , QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QAction, QMessageBox)
from PyQt5.QtGui import QIcon

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("James")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("ressources/james_icon.png"))
        self.widget =  QWidget()
        self.setCentralWidget(self.widget)

        self.vlayout = QVBoxLayout(self.widget)
        self.textBrowser = QTextBrowser()
        self.vlayout.addWidget(self.textBrowser)

        self.hlayout = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout)

        self.lineedit = QLineEdit()
        self.lineedit.setMinimumHeight(30)
        self.lineedit.setPlaceholderText("Ask something about games...")
        self.lineedit.setStyleSheet("padding-left: 5px;")
        self.hlayout.addWidget(self.lineedit)

        self.button = QPushButton("Send")
        self.button.clicked.connect(self.send)
        self.hlayout.addWidget(self.button) 

        self.create_menubar()

        self.vlayout.setContentsMargins(15, 15, 15, 15)
        self.vlayout.setSpacing(10)
        self.hlayout.setSpacing(10)

        self.apply_theme("ressources/dark.qss")

    def send(self):
        user_input = self.lineedit.text().strip()
        if not user_input:
            return
        self.add_message(user_input, is_user=True)
        response = jamesllm.ask(user_input)
        self.add_message(response, is_user=False)
        self.lineedit.clear()

    def create_menubar(self):
        self.menubar = self.menuBar()

        theme_menu = self.menubar.addMenu("Theme")

        main_theme_action = QAction("Default", self)
        main_theme_action.triggered.connect(lambda: self.apply_theme("ressources/dark.qss"))
        theme_menu.addAction(main_theme_action)

        grey_theme_action = QAction("Grey", self)
        grey_theme_action.triggered.connect(lambda: self.apply_theme("ressources/grey.qss"))
        theme_menu.addAction(grey_theme_action)

        green_theme_action = QAction("Green", self)
        green_theme_action.triggered.connect(lambda: self.apply_theme("ressources/green.qss"))
        theme_menu.addAction(green_theme_action)

        help_menu = self.menubar.addMenu("Help")
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        about_menu = self.menubar.addMenu("About")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

    def add_message(self, text, is_user=True):
        align = "right" if is_user else "left"
        name = "You" if is_user else "James"
        text_color = "#ffffff" if is_user else "#ccffcc"  # Optional: theme-consistent colors
        font_family = "Segoe UI, sans-serif"

        message_html = f"""
        <div style="text-align: {align}; margin: 8px 0;">
            <div style="display: inline-block;
                        padding: 6px 10px;
                        border-radius: 8px;
                        font-family: {font_family};
                        font-size: 14px;
                        color: {text_color};
                        max-width: 75%;
                        word-wrap: break-word;
                        text-align: left;">
                <b>{name}:</b> {text}
            </div>
        </div>
        """
        self.textBrowser.append(message_html)
        self.textBrowser.verticalScrollBar().setValue(
            self.textBrowser.verticalScrollBar().maximum()
        )

    def show_help(self):
        help_text = (
            "This is a simple chat application.\n"
            "You can ask questions about games:\n"
        )
        QMessageBox.information(self, "Help", help_text)
    
    def show_about(self):
        about_text = (
            "James Application v1.0\n\n"
            "Developed by Aryel.\n"
        )
        QMessageBox.information(self, "About", about_text)
    
    def apply_theme(self, theme_filename):
        if os.path.exists(theme_filename):
            try:
                with open(theme_filename, "r") as f:
                    qss = f.read()
                QApplication.instance().setStyleSheet(qss)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to apply theme: {e}")
        else:
            QMessageBox.warning(self, "Error", f"Theme file '{theme_filename}' not found.")

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())