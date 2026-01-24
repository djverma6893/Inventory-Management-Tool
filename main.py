import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login_page import LoginPage
from inventory_page import InventoryPage
from Inventory_page_user import InventoryPageUser
# from menubar import MenuBarManager


class InventoryManagementTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Equipment Inventory Management System')
        self.setGeometry(100, 100, 1400, 800)
        self.current_user = None
        # self.menu_manager = MenuBarManager(self)
        self.setStyleSheet(self.get_main_style())
        self.init_ui()

    def init_ui(self):
        # Create stacked widget to switch between login and inventory pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create login page
        self.login_page = LoginPage(self)
        self.stacked_widget.addWidget(self.login_page)

        # Show login page first
        self.stacked_widget.setCurrentWidget(self.login_page)

        # Status bar
        self.statusBar().setStyleSheet("background-color: #2c3e50; color: white; font-weight: bold;")
        self.statusBar().showMessage('Please login to continue')

    def on_login_success(self, user_info):
        """Called when user successfully logs in"""
        self.current_user = user_info
        print(user_info)
        if user_info["username"]=="admin":
            # Create inventory page with user info
            self.inventory_page = InventoryPage(self, user_info)
            self.stacked_widget.addWidget(self.inventory_page)

            # Switch to inventory page
            self.stacked_widget.setCurrentWidget(self.inventory_page)
            self.statusBar().showMessage(f'Welcome, {user_info.get("full_name", "User")}!')
        else:
            print("moye moye")
            self.inventory_page = InventoryPageUser(self, user_info)
            self.stacked_widget.addWidget(self.inventory_page)

            # Switch to inventory page
            self.stacked_widget.setCurrentWidget(self.inventory_page)
            self.statusBar().showMessage(f'Welcome, {user_info.get("full_name", "User")}!')


    def on_logout(self):
        """Called when user logs out"""
        # Remove inventory page
        if hasattr(self, 'inventory_page'):
            self.stacked_widget.removeWidget(self.inventory_page)
            self.inventory_page.deleteLater()

        # Clear login fields
        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        self.login_page.error_label.setText('')
        self.login_page.username_input.setFocus()

        # Switch back to login page
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.current_user = None
        self.statusBar().showMessage('Logged out successfully')

    def get_main_style(self):
        return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }

            /* Login Page Styles */
            #loginContainer {
                background-color: white;
                border-radius: 15px;
            }

            #appTitle {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
            }

            #subtitle {
                font-size: 14px;
                color: #7f8c8d;
            }

            #inputLabel {
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }

            #loginInput {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
            }

            #loginInput:focus {
                border: 2px solid #667eea;
                background-color: white;
            }

            #loginButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                min-height: 50px;
            }

            #loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3, stop:1 #6941a8);
            }

            #errorLabel {
                color: #e74c3c;
                font-size: 13px;
                font-weight: bold;
            }

            #infoLabel {
                color: #95a5a6;
                font-size: 12px;
            }

            /* Inventory Page Styles */
            #mainTitle {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                background-color: #065691;
                color: white;
                border-radius: 8px;
            }

            #userLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px;
            }

            #logoutButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }

            #logoutButton:hover {
                background-color: #c0392b;
            }

            #searchLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
            }

            #searchBox {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }

            QTableWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QTableWidget::item:alternate {
                background-color: #f8f9fa;
            }

            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }

            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                min-width: 150px;
            }

            #addButton {
                background-color: #27ae60;
                color: white;
            }
            #del_col_btn, #add_col_btn{
                padding: 12px 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                min-width: 20px;
                background-color: #F2F4F8;
                color: white;
            }
            #del_col_btn:hover , #add_col_btn:hover {
                background-color: #E4E7EC;
                }
            #addButton:hover {
                background-color: #229954;
            }

            #updateButton {
                background-color: #3498db;
                color: white;
            }

            #updateButton:hover {
                background-color: #2980b9;
            }

            #deleteButton {
                background-color: #e74c3c;
                color: white;
            }

            #deleteButton:hover {
                background-color: #c0392b;
            }

            #refreshButton {
                background-color: #f39c12;
                color: white;
            }

            #refreshButton:hover {
                background-color: #e67e22;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #95a5a6;
            }

            QCheckBox::indicator:checked {
                background-color: #27ae60;
                border: 2px solid #27ae60;
            }
            
        """


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InventoryManagementTool()
    window.show()
    sys.exit(app.exec_())