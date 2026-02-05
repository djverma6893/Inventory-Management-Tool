from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from database_mongodb import DatabaseManager
# from database_manager import DatabaseManager


class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Login container
        login_container = QWidget()
        login_container.setObjectName('loginContainer')
        login_container.setMaximumWidth(450)
        login_container.setMinimumHeight(500)

        container_layout = QVBoxLayout()
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(40, 40, 40, 40)

        # Logo/Title
        title_label = QLabel('🔐')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 60px;')
        container_layout.addWidget(title_label)

        app_title = QLabel('INVENTORY MANAGEMENT')
        app_title.setObjectName('appTitle')
        app_title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(app_title)

        subtitle = QLabel('Please login to continue')
        subtitle.setObjectName('subtitle')
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)

        container_layout.addSpacing(20)

        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel('Username')
        username_label.setObjectName('inputLabel')
        self.username_input = QLineEdit()
        self.username_input.setObjectName('loginInput')
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setText('user')  # Pre-filled for demo
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        container_layout.addLayout(username_layout)

        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel('Password')
        password_label.setObjectName('inputLabel')
        self.password_input = QLineEdit()
        self.password_input.setObjectName('loginInput')
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setText('user123')  # Pre-filled for demo
        #show/hide password icon
        self.show_action = QAction(QIcon("hide.png"), "", self)
        self.show_action.setCheckable(True)
        self.show_action.toggled.connect(self.toggle_password)
        self.password_input.addAction(self.show_action, QLineEdit.TrailingPosition)

        # #Dard mode handle
        # palette = self.password_input.palette()
        # palette.setColor(QPalette.Text, QColor("grey"))  # text color
        # palette.setColor(QPalette.Base, QColor("#2b2b2b"))  # background color
        # self.password_input.setPalette(palette)

        self.password_input.returnPressed.connect(self.handle_login)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        container_layout.addLayout(password_layout)

        container_layout.addSpacing(10)

        # Login button
        self.login_btn = QPushButton('LOGIN')
        self.login_btn.setObjectName('loginButton')
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.handle_login)
        container_layout.addWidget(self.login_btn)

        # Error message label
        self.error_label = QLabel('')
        self.error_label.setObjectName('errorLabel')
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        container_layout.addWidget(self.error_label)

        # Info text
        info_label = QLabel('Member credentials:\nUsername: user\nPassword: user123')
        info_label.setObjectName('infoLabel')
        info_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(info_label)

        container_layout.addStretch()

        login_container.setLayout(container_layout)
        main_layout.addWidget(login_container)

        self.setLayout(main_layout)
    #Show/Hide function for password inpute
    def toggle_password(self,checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)  # Show password
            self.show_action.setIcon(QIcon("hide.png"))  # Optional: change icon
        else:
            self.password_input.setEchoMode(QLineEdit.Password)  # Hide password
            self.show_action.setIcon(QIcon("show.png"))
    #login Handle
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.show_error('Please enter both username and password')
            return

        # Authenticate user
        db_manager = DatabaseManager()
        user = db_manager.authenticate_user(username, password)

        if user:
            self.error_label.setText('')
            if self.parent_window:
                self.parent_window.on_login_success(user)
        else:
            self.show_error('Invalid username or password')
            self.password_input.clear()
            self.password_input.setFocus()

    def show_error(self, message):
        self.error_label.setText(f'❌ {message}')

