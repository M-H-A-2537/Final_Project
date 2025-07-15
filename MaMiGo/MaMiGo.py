import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt6.QtCore import Qt, QSize
import os, shutil
from Database.database import User, Contact, Message, engine, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import qtawesome as qta



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.session = get_session()
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
        if not username or not password :
            QMessageBox.warning(self, "error", "please complete the fields.")
            return
        user = self.session.query(User).filter_by(username = username, password = password).one_or_none()
        if user != None :
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
        self.session = get_session()
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
        self.session.add(new_user)
        self.session.commit()
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
    def __init__(self, user) :
        super().__init__()
        self.user = user
        self.session = get_session()
        self.contacts = session.query(Contact).filter_by(user_id=self.user.id).all()
        self.current_contact = None
        self.last_message_id = 0
        self.setWindowTitle("MaMiGo")
        self.setGeometry(275, 50, 1000, 800)
        self.setup_ui()
        self.load_contacts()

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

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("""
                    QLineEdit {
                        background-color: #f0f2f5;
                        border-radius: 15px;
                        padding: 10px 20px;
                        font-size: 14px;
                        border: 1px solid #d8dce6;
                    }
                """)
        self.search_input.textChanged.connect(self.find_contacts)

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
        settings_button.clicked.connect(self.open_settings)

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
        new_contact_button.clicked.connect(self.open_add_contact)

        options_layout.addWidget(self.search_input)
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
        self.contacts_list.itemClicked.connect(self.contact_selected)

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
        send_button.clicked.connect(self.send_message)

        message_layout.addWidget(self.message_input)
        message_layout.addWidget(send_button)
        chat_area_layout.addWidget(self.chat_display)
        chat_area_layout.addWidget(message_input_widget)
        main_area_layout.addWidget(self.chat_header)
        main_area_layout.addWidget(self.chat_area)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.main_area)

    def load_contacts(self):
        self.contacts_list.clear()
        for contact in self.contacts:
            item = QListWidgetItem()
            widget = self.create_contact_widget(contact.username, "online")
            item.setSizeHint(widget.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, contact.id)
            self.contacts_list.addItem(item)
            self.contacts_list.setItemWidget(item, widget)
        if self.contacts_list.count() > 0 :
            self.contacts_list.setCurrentRow(0)
            self.contact_selected(self.contacts_list.item(0))

    def create_contact_widget(self, name, status):
        widget = QWidget()

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10)

        profile_avatar = QLabel()
        pixmap = QPixmap(self.user.profile_image)
        profile_avatar.setPixmap(pixmap)
        profile_avatar.setScaledContents(True)
        profile_avatar.setFixedSize(50, 50)
        profile_avatar.setStyleSheet("border-radius: 25px; border: none;")

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(10, 0, 0, 0)

        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        status_label = QLabel(status)
        status_label.setFont(QFont("Arial", 9))
        status_label.setStyleSheet("color: #777;")

        info_layout.addWidget(name_label)
        info_layout.addWidget(status_label)
        info_layout.addStretch()
        layout.addWidget(profile_avatar)
        layout.addWidget(info_widget, 1)
        return widget

    def contact_selected(self, item):
        contact_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_contact = self.session.query(Contact).filter_by(id=contact_id).first()
        if self.current_contact:
            self.contact_name.setText(self.current_contact.username)
            base_profile = os.getcwd()
            base_profile = base_profile + "/Appearance_structure/pictures/base_profile.png"
            self.contact_avatar.setIconSize(QSize(50, 50))
            self.contact_avatar.setIcon(QIcon(base_profile))
            self.contact_avatar.setStyleSheet("border-radius: 25px; border: none")
        self.load_chat_history()

    def load_chat_history(self):
        if not self.current_contact :
            return
        self.chat_display.clear()
        self.last_message_id = 0
        messages = session.query(Message).filter(or_((Message.send_id == self.user.id) & (Message.receive_id == self.current_contact.id), (Message.send_id == self.current_contact.id) & (Message.receive_id == self.user.id)))
        for message in messages:
            send_id = message.send_id
            letter = message.message
            if send_id == self.user.id :
                direction = "outgoing"
            else :
                direction = "incoming"
            self.add_message(direction, letter)
            if message.id > self.last_message_id:
                self.last_message_id = message.id

    def add_message(self, direction, text):
        if direction == "outgoing":
            style = """
                background-color: #dcf8c6;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 50px 5px 100px;
            """
            alignment = Qt.AlignmentFlag.AlignRight
        else:
            style = """
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 10px;
                padding: 10px;
                margin: 5px 100px 5px 50px;
                border: 1px solid rgba(224, 224, 224, 0.7);
            """
            alignment = Qt.AlignmentFlag.AlignLeft
        html = f"""
        <div style='{style}'>
            <p style='margin:0;'>{text}</p>
            <p style='margin:0; text-align:right; font-size:9px; color:#777;'>12:30 PM</p>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.setAlignment(alignment)
        scroll_bar = self.chat_display.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

    def send_message(self):
        message = self.message_input.text()
        if message and self.current_contact :
            new_message = Message(send_id = self.user.id, receive_id = self.current_contact.id, message = message)
            self.session.add(new_message)
            self.session.commit()
            self.add_message("outgoing", message)
            self.message_input.clear()
            self.last_message_id = new_message.id

    def find_contacts(self, text):
        for i in range(self.contacts_list.count()):
            item = self.contacts_list.item(i)
            widget = self.contacts_list.itemWidget(item)
            name_label = widget.layout().itemAt(1).widget().layout().itemAt(0).widget()
            item.setHidden(text.lower() not in name_label.text().lower())

    def open_add_contact(self):
        dialog = AddContactDialog(self.user)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_contacts()

    def open_settings(self):
        dialog = SettingsDialog(self.user)
        dialog.exec()

    def check_new_messages(self):
        if not self.current_contact :
            return
        print("hi")
        messages = self.session.query(Message).filter(or_((Message.receive_id == self.user.id) & (Message.send_id == self.current_contact.id) & (Message.id > self.last_message_id))).all()
        for message in messages :
            self.add_message("incoming", message.message)
            self.last_message_id = message.id


class AddContactDialog(QDialog):
    def __init__(self, user):
        super().__init__()
        self.session = get_session()
        self.user = user
        self.setWindowTitle("add new contact")
        self.setFixedSize(200, 100)
        self.setup_ui()

    def setup_ui(self):
        back_photo_path = os.getcwd()
        back_photo_path = back_photo_path + "/Appearance_structure/pictures/back_intro.jpg"
        self.set_background(back_photo_path)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("enter username")

        add_button = QPushButton("Add Contact")
        add_button.clicked.connect(self.add_contact)

        layout.addWidget(QLabel("Enter username of the contact :"))
        layout.addWidget(self.username_input)
        layout.addWidget(add_button)
        self.setLayout(layout)

    def add_contact(self):
        username = self.username_input.text()
        if not username :
            QMessageBox.warning(self, "Error", "please enter username")
            return
        profile_photo_path = os.getcwd()
        profile_photo_path = profile_photo_path + "/Appearance_structure/pictures/base_profile.png"
        user = session.query(User).filter_by(username=username).one_or_none()
        if user == None :
            QMessageBox.critical(self, "Error", "user not found")
            return
        new_contact = Contact(phone = user.phone, username = user.username, password = user.password, bio = user.bio, profile_image = profile_photo_path, user_id = self.user.id)
        self.session.add(new_contact)
        self.session.commit()
        contact_for_user = Contact(phone = self.user.phone, username = self.user.username, password = self.user.password, bio = self.user.bio, profile_image = self.user.profile_image, user_id = user.id)
        contact = session.query(Contact).filter_by(username = username).one_or_none()
        self.session.add(contact_for_user)
        self.session.commit()
        if contact != None :
            QMessageBox.information(self, "Success", "contact added successfully")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "something wrong to add this user to your contacts")

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


class SettingsDialog(QDialog):
    def __init__(self, user):
        super().__init__()
        self.session = get_session()
        self.user = user
        self.setWindowTitle("settings")
        self.setFixedSize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.password_input = QLineEdit()
        self.username_input = QLineEdit(self.user)

        self.phone_input = QLineEdit(self.user[2])

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("New password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("New Password:", self.password_input)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)

        # دکمه‌های تغییر تصویر
        buttons_layout = QHBoxLayout()

        change_picture_button = QPushButton("Change Profile Picture")
        change_picture_button.clicked.connect(self.change_profile_image)

        buttons_layout.addWidget(change_picture_button)

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)

        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def change_profile_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Profile Picture",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if not file_path:
            return

        # Copy to application directory
        try:
            dest_dir = os.path.join(os.getcwd(), "profile_images")
            os.makedirs(dest_dir, exist_ok=True)

            filename = f"profile_{self.user.id}_{os.path.basename(file_path)}"
            dest_path = os.path.join(dest_dir, filename)

            shutil.copyfile(file_path, dest_path)

            # Update database
            session = get_session()
            try:
                user = session.query(User).filter_by(id=self.user.id).first()
                if user:
                    user.profile_image = dest_path
                    session.commit()
                    QMessageBox.information(self, "Success", "Profile picture updated!")
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Error", f"Could not update database: {str(e)}")
            finally:
                session.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not copy image: {str(e)}")

    def save_changes(selfself) :
        pass

def get_session():
    return SessionLocal()


#######START#######
SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())