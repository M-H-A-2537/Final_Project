import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush, QColor, QIcon
from PyQt6.QtCore import Qt, QSize
import os, shutil
from Database.database import User, Contact, engine
from sqlalchemy.orm import sessionmaker
import qtawesome as qta




class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIGN IN")
        self.setFixedSize(1000, 700)
        self.setup_ui()

    def setup_ui(self):
        back_photo_path = os.getcwd()
        back_photo_path = back_photo_path + "/Appearance_structure/pictures/back_intro.jpg"
        self.set_background(back_photo_path)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(50, 80, 50, 50)

        header = QLabel("Welcome to MaMiGo !")
        header_font = QFont("B Nazanin", 24, QFont.Weight.Bold)
        header.setFont(header_font)
        header.setStyleSheet("""
            color: white;
            padding: 15px;
            border-radius: 10px;
            background-color: rgba(0, 0, 0, 150);
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_widget.setStyleSheet("""
            background-color: rgba(255, 255, 255, 200);
            border-radius: 15px;
            padding: 30px;
        """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)

        username_layout = QHBoxLayout()
        username_label = QLabel("USERNAME")
        username_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_label = QLabel("PASSWORD")
        password_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        self.show_password_check = QCheckBox("show password")
        self.show_password_check.setStyleSheet("""
                    QCheckBox {
                        font-size: 18px;
                        spacing: 10px;
                    }
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border: 2px solid #3498db;
                        border-radius: 5px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #3498db;
                        image: url(:/tick.png);
                    }
                """)
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_check)

        login_button = QPushButton("login")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        login_button.clicked.connect(self.authenticate)

        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addWidget(login_button)

        signup_link = QLabel(
            '<html><a href="signup" style="color:#3498db; text-decoration:none; font-weight:bold;">'
            'No account? Creat one!'
            '</a></html>'
        )
        signup_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        signup_link.linkActivated.connect(self.open_signup)

        main_layout.addWidget(header)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(signup_link)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(main_widget)

    def set_background(self, image_path):
        if os.path.exists(image_path):
            palette = QPalette()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            self.setPalette(palette)
        else:
            print(f"⚠️ Image not found: {image_path}")
            self.setStyleSheet("background-color: #2c3e50;")

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "error", "please complete the fields.")
            return
        user = session.query(User).filter_by(username = username, password = password).one_or_none()
        if user != None :
            print("OK!")
            self.open_main_window(user)
        else:
            QMessageBox.critical(self, "error", "there is no one with this username and password!")
    def toggle_password_visibility(self, state):
        if state == 2 :
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def open_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()

    def open_main_window(self, user):
        self.main_window = MainWindow(user)
        self.main_window.show()
        self.hide()


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.db = db
        self.setWindowTitle("SIGN UP")
        self.setFixedSize(1000, 700)
        self.setup_ui()

    def setup_ui(self):
        back_photo_path = os.getcwd()
        back_photo_path = back_photo_path + "/Appearance_structure/pictures/back_intro.jpg"
        self.set_background(back_photo_path)
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(50, 50, 50, 50)

        header = QLabel("Create account")
        header_font = QFont("B Nazanin", 24, QFont.Weight.Bold)
        header.setFont(header_font)
        header.setStyleSheet("""
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    background-color: rgba(0, 0, 0, 150);
                """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_widget.setStyleSheet("""
                    background-color: rgba(255, 255, 255, 200);
                    border-radius: 15px;
                    padding: 30px;
                """)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)

        phone_layout = QHBoxLayout()
        phone_label = QLabel("PHONE NUMBER")
        phone_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        self.phone_input.setStyleSheet("""
                    QLineEdit {
                        padding: 12px;
                        font-size: 16px;
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        background-color: rgba(255, 255, 255, 200);
                    }
                """)
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)

        username_layout = QHBoxLayout()
        username_label = QLabel("USERNAME")
        username_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
                    QLineEdit {
                        padding: 12px;
                        font-size: 16px;
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        background-color: rgba(255, 255, 255, 200);
                    }
                """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_label = QLabel("PASSWORD")
        password_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
                    QLineEdit {
                        padding: 12px;
                        font-size: 16px;
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        background-color: rgba(255, 255, 255, 200);
                    }
                """)
        self.show_password_check = QCheckBox("show password")
        self.show_password_check.setStyleSheet("""
                            QCheckBox {
                                font-size: 18px;
                                spacing: 10px;
                            }
                            QCheckBox::indicator {
                                width: 20px;
                                height: 20px;
                                border: 2px solid #3498db;
                                border-radius: 5px;
                            }
                            QCheckBox::indicator:checked {
                                background-color: #3498db;
                                image: url(:/tick.png);
                            }
                        """)
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_check)

        re_password_layout = QHBoxLayout()
        re_password_label = QLabel("RE-ENTER PASSWORD")
        re_password_label.setStyleSheet("font-size: 20px; font-weight: bold; min-width: 100px;")
        self.re_password_input = QLineEdit()
        self.re_password_input.setPlaceholderText("Enter your password again")
        self.re_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.re_password_input.setStyleSheet("""
                    QLineEdit {
                        padding: 12px;
                        font-size: 16px;
                        border: 2px solid #3498db;
                        border-radius: 8px;
                        background-color: rgba(255, 255, 255, 200);
                    }
                """)
        self.show_re_password_check = QCheckBox("show password")
        self.show_re_password_check.setStyleSheet("""
                            QCheckBox {
                                font-size: 18px;
                                spacing: 10px;
                            }
                            QCheckBox::indicator {
                                width: 20px;
                                height: 20px;
                                border: 2px solid #3498db;
                                border-radius: 5px;
                            }
                            QCheckBox::indicator:checked {
                                background-color: #3498db;
                                image: url(:/tick.png);
                            }
                        """)
        self.show_re_password_check.stateChanged.connect(self.toggle_re_password_visibility)

        re_password_layout.addWidget(re_password_label)
        re_password_layout.addWidget(self.re_password_input)
        re_password_layout.addWidget(self.show_re_password_check)

        signup_button = QPushButton("create your account")
        signup_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        padding: 15px;
                        font-size: 18px;
                        font-weight: bold;
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
        signup_button.clicked.connect(self.register)

        form_layout.addLayout(phone_layout)
        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(re_password_layout)

        main_layout.addWidget(header)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(signup_button)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(main_widget)

    def set_background(self, image_path):
        if os.path.exists(image_path):
            palette = QPalette()
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            self.setPalette(palette)
        else:
            print(f"⚠️ Image not found: {image_path}")
            self.setStyleSheet("background-color: #2c3e50;")

    def register(self):
        phone = self.phone_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        re_password = self.re_password_input.text()
        if not phone :
            QMessageBox.warning(self, "error", "completing the phone field is required.")
            return
        if not username:
            QMessageBox.warning(self, "error", "completing the username field is required.")
            return
        if not password:
            QMessageBox.warning(self, "error", "completing the password field is required.")
            return
        if not re_password :
            QMessageBox.warning(self, "error", "completing the re_password field is required.")
            return
        if password != re_password:
            QMessageBox.warning(self, "error", "completing the re_password field is required.")
            return

        profile_photo_path = os.getcwd()
        profile_photo_path = profile_photo_path + "/Appearance_structure/pictures/base_profile.png"
        new_user = User(phone = phone, username = username, password = password, bio = "(empty)", profile_image = profile_photo_path)
        session.add(new_user)
        session.commit()
        if new_user :
            QMessageBox.information(self, "congratulations", "your account created successfully.")
            self.close()
        else:
            QMessageBox.critical(self, "error", "the username, phone number or password is duplicated.")

    def toggle_password_visibility(self, state):
        if state == 2:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_re_password_visibility(self, state):
        if state == 2:
            self.re_password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.re_password_input.setEchoMode(QLineEdit.EchoMode.Password)


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("MaMiGo")
        self.setGeometry(275, 50, 1000, 800)
        self.setup_ui()

    def setup_ui(self):
#######CENTERAL-WIDGET#######
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
#######LEFT-SIDEBAR#######
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(330)
        self.sidebar.setStyleSheet("background-color: white;")

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_header = QWidget()
        sidebar_header.setFixedHeight(150)
        sidebar_header.setStyleSheet("background-color: white; border-bottom: 5px solid #d8dce6;")

        header_layout = QVBoxLayout(sidebar_header)
        header_layout.setSpacing(5)

        profile_layout = QHBoxLayout(sidebar_header)
        profile_layout.setContentsMargins(15, 0, 15, 0)
        profile_layout.setSpacing(15)

        profile_avatar = QLabel()
        pixmap = QPixmap(self.user.profile_image)
        profile_avatar.setPixmap(pixmap)
        profile_avatar.setScaledContents(True)
        profile_avatar.setFixedSize(70, 70)
        profile_avatar.setStyleSheet("border-radius: 35px; border: none;")

        profile_name = QLabel()
        profile_name.setText(self.user.username)
        profile_name.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        profile_name.setStyleSheet("border: none;")

        profile_layout.addWidget(profile_avatar)
        profile_layout.addWidget(profile_name)

        options_layout = QHBoxLayout(sidebar_header)
        options_layout.setContentsMargins(15, 0, 15, 0)
        options_layout.setSpacing(10)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search...")
        search_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #f0f2f5;
                        border-radius: 15px;
                        padding: 10px 20px;
                        font-size: 14px;
                        border: 1px solid #d8dce6;
                    }
                """)
        settings_icon = qta.icon("mdi.cog", color="black")
        settings_button = QPushButton()
        settings_button.setIcon(settings_icon)
        settings_button.setFixedSize(40, 40)
        settings_button.setStyleSheet("""
                        QPushButton {
                            border-radius: 20px;
                            background-color: #3498db;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #0077bb;
                            border: 2px solid #1c638e;
                        }
                        QPushButton:pressed {
                            background-color: #1c638e;
                        }
                    """)

        new_contact_button = QPushButton()
        new_contact_button.setIcon(QIcon.fromTheme("contact-new"))
        new_contact_button.setFixedSize(40, 40)
        new_contact_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        border-radius: 20px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #0077bb;
                        border: 2px solid #1c638e;
                    }
                    QPushButton:pressed {
                            background-color: #1c638e;
                    }
                """)

        options_layout.addWidget(search_input)
        options_layout.addWidget(settings_button)
        options_layout.addWidget(new_contact_button)
        header_layout.addLayout(profile_layout)
        header_layout.addLayout(options_layout)

        self.contacts_list = QListWidget()
        self.contacts_list.setStyleSheet("""
                    QListWidget {
                        background-color: transparent;
                        border: none;
                        font-size: 16px;
                    }
                    QListWidget::item {
                        padding: 10px 15px;
                        border-bottom: 1px solid #e0e0e0;
                    }
                    QListWidget::item:selected {
                        background-color: #e6e6e6;
                    }
                """)

        sidebar_layout.addWidget(sidebar_header)
        sidebar_layout.addWidget(self.contacts_list)
#######MAIN-AREA-CHAT#######
        self.main_area = QWidget()
        main_area_layout = QVBoxLayout(self.main_area)
        main_area_layout.setContentsMargins(0, 0, 0, 0)
        main_area_layout.setSpacing(0)
#######CHAT-HEADER#######
        self.chat_header = QWidget()
        self.chat_header.setFixedHeight(70)
        self.chat_header.setStyleSheet("background-color: white; border-bottom: 1px solid #d8dce6;")

        chat_header_layout = QHBoxLayout(self.chat_header)
        chat_header_layout.setContentsMargins(15, 0, 15, 0)
#######CONTACT-INFO#######
        self.contact_info = QWidget()
        contact_info_layout = QHBoxLayout(self.contact_info)

        self.contact_avatar = QPushButton()
        self.contact_avatar.setIconSize(QSize(50, 50))
        print(self.user.profile_image)
        self.contact_avatar.setIcon(QIcon(self.user.profile_image))
        self.contact_avatar.setStyleSheet("border-radius: 25px; border: none")

        self.contact_name = QLabel("select contact")
        self.contact_name.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.contact_name.setStyleSheet("border: none;")

        contact_info_layout.addWidget(self.contact_avatar)
        contact_info_layout.addWidget(self.contact_name)
        contact_info_layout.addStretch()
        chat_header_layout.addWidget(self.contact_info)
#######CAHT-AREA#######
        self.chat_area = QWidget()
        chat_area_layout = QVBoxLayout(self.chat_area)
        chat_area_layout.setContentsMargins(0, 0, 0, 0)
        chat_area_layout.setSpacing(0)

        base_chat_path = os.getcwd()
        base_chat_path = base_chat_path.split('\\')
        base_chat_path = '/'.join(base_chat_path)
        base_chat_path = base_chat_path + "/Appearance_structure/pictures/base_chat.jpg"
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(f"""
                    QTextEdit {{
                        background-image: url({base_chat_path});
                        background-position: center;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        background-size: cover;
                        border: none;
                        font-size: 14px;
                        padding: 15px;
                    }}
                """)

        message_input_widget = QLabel()
        message_input_widget.setFixedHeight(70)
        message_input_widget.setStyleSheet("background-color: white; border-top: 1px solid #d8dce6;")

        message_layout = QHBoxLayout(message_input_widget)
        message_layout.setContentsMargins(15, 10, 15, 10)

        attach_button = QPushButton()
        attach_button.setIcon(QIcon.fromTheme("mail-attachment"))
        attach_button.setFixedSize(40, 40)
        attach_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #e9ecef;
                                        border-radius: 20px;
                                        border: none;
                                    }
                                    QPushButton:pressed {
                                            background-color: #dee2e6;
                                    }
                                """)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Write a message...")
        self.message_input.setStyleSheet("""
                    QLineEdit {
                        background-color: white;
                        border-radius: 20px;
                        padding: 10px 20px;
                        font-size: 15px;
                        border: 1px solid #d8dce6;
                    }
                """)

        send_button = QPushButton()
        send_button.setIcon(QIcon.fromTheme("mail-send"))
        send_button.setFixedSize(45, 45)
        send_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        border-radius: 22px;
                    }
                    QPushButton:hover {
                        background-color: #0077bb;
                        border: 2px solid #1c638e;
                    }
                    QPushButton:pressed {
                            background-color: #1c638e;
                    }
                """)

        message_layout.addWidget(attach_button)
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(send_button)
        chat_area_layout.addWidget(self.chat_display)
        chat_area_layout.addWidget(message_input_widget)
        main_area_layout.addWidget(self.chat_header)
        main_area_layout.addWidget(self.chat_area)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_area)



SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())