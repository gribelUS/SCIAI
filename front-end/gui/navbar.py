from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from gui.login import logged_user_confirmation
from models.api import communication_mode

class NavBar(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user 
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Outer layout (holds the gold background container)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # Inner container that gets the gold background
        container = QWidget()
        container.setObjectName("navbar_container")
        container.setFixedHeight(100)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("gui/assets/logo.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        else:
            logo.setText("Logo")
        logo.setAlignment(Qt.AlignVCenter)
        logo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(logo)

        # Buttons
        self.dashboard_btn = QPushButton("PRT Dashboard")
        self.dashboard_btn.setCursor(Qt.PointingHandCursor)
        self.dashboard_btn.setCheckable(True)
        self.dashboard_btn.setChecked(True)
        layout.addWidget(self.dashboard_btn)

        self.activity_btn = QPushButton("Activity Log")
        self.activity_btn.setCursor(Qt.PointingHandCursor)
        self.activity_btn.setCheckable(True)
        layout.addWidget(self.activity_btn)

        # Add admin-only button
        if user["role"] == "admin":
            self.manage_users_btn = QPushButton("Manage Users")
            self.manage_users_btn.setCursor(Qt.PointingHandCursor)
            self.manage_users_btn.setCheckable(True)
            layout.addWidget(self.manage_users_btn)

            self.mode_switch_btn = QPushButton("PLC Mode")
            communication_mode(1)
            self.mode_switch_btn.setCursor(Qt.PointingHandCursor)
            self.mode_switch_btn.setCheckable(True)
            self.mode_switch_btn.setStyleSheet("background-color: white; color: #002855; border-radius: 5px;")
            self.mode_switch_btn.clicked.connect(self.check_logged_password)
            layout.addWidget(self.mode_switch_btn)

        else:
            self.manage_users_btn = None
            self.mode_switch_btn = None

        layout.addStretch()
        outer_layout.addWidget(container)

        # Style only the container
        self.setStyleSheet("""
            QWidget#navbar_container {
                background-color: #EAAA00;
                border-bottom: 2px solid #FFFFFF;
            }
            QWidget {
                background-color: #EAAA00;
                border-bottom: 2px solid #FFFFFF;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 8px 20px;
                margin: 10px;
            }

            QPushButton:hover {
                background-color: #ffc600;
                color: #002855;
                border-radius: 5px;
            }

            QPushButton:checked {
                background-color: white;
                color: #002855;
                border-radius: 5px;
            }
            QLineEdit {
                font-size: 16px;
                border: 1px solid black;
                background-color: transparent;
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            QInputDialog:getText {
                background-color: #EAAA00;
                color: #002855;
                font-size: 16px; 
            }
        """)

        # Switch state behavior
        self.dashboard_btn.clicked.connect(self.set_dashboard_active)
        self.activity_btn.clicked.connect(self.set_activity_active)

    def set_dashboard_active(self):
        self.dashboard_btn.setChecked(True)
        self.activity_btn.setChecked(False)
        if self.manage_users_btn:
            self.manage_users_btn.setChecked(False)

    def set_activity_active(self):
        self.dashboard_btn.setChecked(False)
        self.activity_btn.setChecked(True)
        if self.manage_users_btn:
            self.manage_users_btn.setChecked(False)

    def set_manage_users_active(self):
        if self.manage_users_btn:
            self.dashboard_btn.setChecked(False)
            self.activity_btn.setChecked(False)
            self.manage_users_btn.setChecked(True)

    def check_logged_password(self):
        password, ok = QInputDialog.getText(self, "Enter Password", "Please enter your password to switch modes:", QLineEdit.Password)
        if ok:
            if logged_user_confirmation(self.user, password):
                self.toggle_mode()
            else:
                QMessageBox.warning(self, "Error", "Incorrect password. Mode switch aborted.")
                self.mode_switch_btn.setChecked(not self.mode_switch_btn.isChecked())

    def toggle_mode(self):

        if self.mode_switch_btn.isChecked():
            self.mode_switch_btn.setText("Web Mode")
            self.mode_switch_btn.setStyleSheet("background-color: #002855; color: white; border-radius: 5px;")
            communication_mode(0)

        elif not self.mode_switch_btn.isChecked():
            communication_mode(1)
            self.mode_switch_btn.setStyleSheet("background-color: white; color: #002855; border-radius: 5px;")
            self.mode_switch_btn.setText("PLC Mode")
