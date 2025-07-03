import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('login.ui', self)

        # --- Widgets ---
        self.username = self.findChild(QLineEdit, 'username')
        self.password = self.findChild(QLineEdit, 'password_2')
        self.loginbutton = self.findChild(QPushButton, 'loginbutton')
        self.message_label = self.findChild(QLabel, 'message_label')
        self.forgot_password_label = self.findChild(QLabel, 'forgotPasswordLabel')
        self.registerLinkButton = self.findChild(QPushButton, 'registerLinkButton')
        self.backToLoginButton = self.findChild(QPushButton, 'backToLoginButton')
        self.login_title_label = self.findChild(QLabel, 'loginTitle')

        # --- Connect buttons ---
        if self.loginbutton:
            self.loginbutton.clicked.connect(self.handle_action_button)
        if self.registerLinkButton:
            self.registerLinkButton.clicked.connect(self.show_register_mode)
        if self.backToLoginButton:
            self.backToLoginButton.clicked.connect(self.show_login_mode)

        # --- Placeholder & Echo ---
        if self.username:
            self.username.setPlaceholderText("Enter User Name")
        if self.password:
            self.password.setPlaceholderText("Enter Password")
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        if self.message_label:
            self.message_label.setText("")
            self.message_label.setStyleSheet("color: red;")

        self.USERS = {
            "designer1": "designpass123",
            "john.doe": "mysecurepassword",
            "admin": "adminpass"
        }

        self.current_mode = "login"
        self.apply_styles()
        self.update_ui_for_mode()

    def apply_styles(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        main_frame = self.findChild(QFrame, 'mainFrame') or self
        main_frame.setStyleSheet("""
            QFrame#mainFrame, QDialog {
                background-color: white;
                border-radius: 20px;
            }
        """)

        left_panel = self.findChild(QFrame, 'leftPanel')
        if left_panel:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_filename = "background.jpg"  # ✅ Make sure this file exists
            absolute_image_path = os.path.join(current_dir, image_filename)
            image_url = QtCore.QUrl.fromLocalFile(absolute_image_path).toString()

            print("Image path exists:", os.path.exists(absolute_image_path))  # Debug

            left_panel.setStyleSheet(f"""
                QFrame#leftPanel {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0,0,0,0.6), stop:1 rgba(0,0,0,0.6)),
                        url('{image_url}');
                    background-position: center;
                    background-repeat: no-repeat;
                    background-size: cover;
                    border-top-left-radius: 20px;
                    border-bottom-left-radius: 20px;
                    color: white;
                }}
                QFrame#leftPanel QLabel {{
                    color: white;
                }}
                QFrame#leftPanel QLabel#mindZapTitle {{
                    font-size: 42px;
                    font-weight: bold;
                }}
                QFrame#leftPanel QLabel#quoteText {{
                    font-size: 16px;
                    font-style: italic;
                    margin-top: 20px;
                }}
            """)

        right_panel = self.findChild(QFrame, 'rightPanel')
        if right_panel:
            right_panel.setStyleSheet("""
                QFrame#rightPanel {
                    background-color: white;
                    border-top-right-radius: 20px;
                    border-bottom-right-radius: 20px;
                }
                QFrame#rightPanel QLabel {
                    color: #333;
                    font-size: 16px;
                    font-weight: 600;
                }
                QFrame#rightPanel QLabel#loginTitle {
                    font-size: 32px;
                    font-weight: bold;
                }
                QFrame#rightPanel QLineEdit {
                    border: none;
                    border-bottom: 2px solid #ddd;
                    padding: 8px 0;
                    font-size: 16px;
                }
                QFrame#rightPanel QLineEdit:focus {
                    border-bottom-color: #007bff;
                }
                QPushButton#loginbutton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #007bff, stop:1 #00c6ff);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 25px;
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 25px;
                }
                QPushButton#loginbutton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #0056b3, stop:1 #0099cc);
                }
                QLabel#forgotPasswordLabel {
                    color: #007bff;
                    text-decoration: underline;
                    font-size: 14px;
                    margin-top: 10px;
                }
                QLabel#message_label {
                    font-weight: bold;
                    margin-top: 15px;
                }
                QPushButton#registerLinkButton, QPushButton#backToLoginButton {
                    background-color: transparent;
                    color: #007bff;
                    border: none;
                    text-decoration: underline;
                    font-size: 14px;
                    padding: 5px;
                    margin-top: 5px;
                }
                QPushButton#registerLinkButton:hover, QPushButton#backToLoginButton:hover {
                    color: #0056b3;
                }
            """)

    def update_ui_for_mode(self):
        if self.current_mode == "login":
            self.login_title_label.setText("Log In")
            self.loginbutton.setText("Log In")
            self.loginbutton.setStyleSheet(self.get_login_button_style())
            self.forgot_password_label.setVisible(True)
            self.registerLinkButton.setVisible(True)
            self.backToLoginButton.setVisible(False)
        else:
            self.login_title_label.setText("Register")
            self.loginbutton.setText("Register")
            self.loginbutton.setStyleSheet(self.get_register_button_style())
            self.forgot_password_label.setVisible(False)
            self.registerLinkButton.setVisible(False)
            self.backToLoginButton.setVisible(True)

        self.message_label.setText("")
        if self.username: self.username.clear()
        if self.password: self.password.clear()

    def get_login_button_style(self):
        return """
            QPushButton#loginbutton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #00c6ff);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 18px;
                font-weight: bold;
                margin-top: 25px;
            }
            QPushButton#loginbutton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0056b3, stop:1 #0099cc);
            }
        """

    def get_register_button_style(self):
        return """
            QPushButton#loginbutton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:1 #218838);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 18px;
                font-weight: bold;
                margin-top: 25px;
            }
            QPushButton#loginbutton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #218838, stop:1 #1e7e34);
            }
        """

    def handle_action_button(self):
        if self.current_mode == "login":
            self.login_user()
        else:
            self.register_new_user()

    def login_user(self):
        username = self.username.text() if self.username else ""
        password = self.password.text() if self.password else ""

        self.message_label.setText("")
        self.message_label.setStyleSheet("color: red; font-weight: bold;")

        if not (username and password):
            self.message_label.setText("Please enter username and password.")
            return

        if username in self.USERS and self.USERS[username] == password:
            self.message_label.setText("Login successful!")
            self.message_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.message_label.setText("Invalid username or password.")

    def register_new_user(self):
        username = self.username.text() if self.username else ""
        password = self.password.text() if self.password else ""

        if not (username and password):
            self.message_label.setText("All fields are required!")
            self.message_label.setStyleSheet("color: red;")
            return

        if username in self.USERS:
            self.message_label.setText(f"Username '{username}' already exists.")
            self.message_label.setStyleSheet("color: orange; font-weight: bold;")
            return

        self.USERS[username] = password
        self.message_label.setText("Registration successful! You can now log in.")
        self.message_label.setStyleSheet("color: green;")
        QtCore.QTimer.singleShot(2000, self.show_login_mode)

    def show_register_mode(self):
        self.current_mode = "register"
        self.update_ui_for_mode()

    def show_login_mode(self):
        self.current_mode = "login"
        self.update_ui_for_mode()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = LoginScreen()
    main_window.setFixedSize(900, 550)
    main_window.setWindowTitle("MindZap Login/Register")
    main_window.show()
    sys.exit(app.exec_())
