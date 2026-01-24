from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QTableWidget, QTableWidgetItem, QPushButton, QCheckBox,
                             QMessageBox, QHeaderView, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
# from database_manager import DatabaseManager
from database_mongodb import DatabaseManager
from dialogs import AddEditDialog


class InventoryPageUser(QWidget):
    def __init__(self, parent=None, user_info=None):
        super().__init__(parent)
        self.parent_window = parent
        self.user_info = user_info
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header section with user info
        header_layout = QHBoxLayout()

        title = QLabel('EQUIPMENT INVENTORY MANAGEMENT')
        title.setObjectName('mainTitle')

        user_info_layout = QVBoxLayout()
        user_label = QLabel(f"👤 {self.user_info.get('full_name', 'User')}")
        user_label.setObjectName('userLabel')

        logout_btn = QPushButton('🚪 Logout')
        logout_btn.setObjectName('logoutButton')
        logout_btn.setMaximumWidth(100)
        logout_btn.clicked.connect(self.handle_logout)

        user_info_layout.addWidget(user_label)
        user_info_layout.addWidget(logout_btn)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(user_info_layout)

        main_layout.addLayout(header_layout)

        # Search section
        search_layout = QHBoxLayout()
        search_label = QLabel('🔍 Search:')
        search_label.setObjectName('searchLabel')

        self.search_box = QLineEdit()
        self.search_box.setObjectName('searchBox')
        self.search_box.setPlaceholderText('Search by Team Member or Serial Number...')
        self.search_box.textChanged.connect(self.search_records)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        # self.table.doubleClicked.connect(self.on_row_double_click)

        # Set column widths
        self.table.setColumnWidth(0, 50)  # Checkbox column

        main_layout.addWidget(self.table)

        # Buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        # self.add_btn = QPushButton('➕ Add Record')
        # # self.update_btn = QPushButton('✏️ Update Record')
        # self.delete_btn = QPushButton('🗑️ Delete Selected')
        self.refresh_btn = QPushButton('🔄 Refresh')

        # self.add_btn.setObjectName('addButton')
        # # self.update_btn.setObjectName('updateButton')
        # self.delete_btn.setObjectName('deleteButton')
        self.refresh_btn.setObjectName('refreshButton')

        # self.add_btn.clicked.connect(self.add_record)
        # # self.update_btn.clicked.connect(self.update_record)
        # self.delete_btn.clicked.connect(self.delete_records)
        self.refresh_btn.clicked.connect(self.load_data)

        # button_layout.addWidget(self.add_btn)
        # # button_layout.addWidget(self.update_btn)
        # button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def handle_logout(self):
        reply = QMessageBox.question(
            self, 'Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.parent_window:
                self.parent_window.on_logout()

    def load_data(self, search_query=None):
        try:
            if search_query:
                print("hey_")
                rows = self.db_manager.search_records(search_query)
            else:
                print("hello")
                rows = self.db_manager.fetch_all_records()

            # Add header row + data rows
            self.table.setRowCount(len(rows) + 1)

            # Create header row (row 0) with bold text
            headers = ['Select', 'Team Member', 'Laptop1 SN', 'Laptop2 SN',
                       'Intern Phone', 'Test Phone1', 'Test Phone2', 'HCL Laptop', 'Serial NO']

            for col_idx, header in enumerate(headers):
                if col_idx == 0:
                    # Checkbox header
                    header_widget = QWidget()
                    header_layout = QHBoxLayout(header_widget)
                    header_layout.setAlignment(Qt.AlignCenter)
                    header_layout.setContentsMargins(0, 0, 0, 0)
                    header_label = QLabel('☑️')
                    header_label.setStyleSheet("font-weight: bold; font-size: 14px;")
                    header_layout.addWidget(header_label)
                    self.table.setCellWidget(0, col_idx, header_widget)
                else:
                    item = QTableWidgetItem(header)
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(10)
                    item.setFont(font)
                    item.setBackground(Qt.lightGray)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(0, col_idx, item)

            # Populate data rows (starting from row 1)
            for row_idx, row_data in enumerate(rows, start=1):
                # Add checkbox in first column
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)

                checkbox = QCheckBox()
                checkbox.setProperty('record_id', row_data.get('id'))  # Store the ID
                checkbox_layout.addWidget(checkbox)

                self.table.setCellWidget(row_idx, 0, checkbox_widget)
                for index,(key, value) in enumerate(row_data.items()):
                    # print(key,value)
                    if key != 'id':
                        item = QTableWidgetItem(str(value))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(row_idx, index+1, item)
                # Add data to remaining columns
                # for col_idx in range(1, 9):
                #     item = QTableWidgetItem(str(row_data[col_idx]) if row_data[col_idx] else '')
                #     item.setTextAlignment(Qt.AlignCenter)
                #     self.table.setItem(row_idx, col_idx, item)

            # Adjust column widths
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.setColumnWidth(0, 70)

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load data: {str(e)}')

    def search_records(self):
        search_text = self.search_box.text()
        if search_text:
            self.load_data(search_text)
        else:
            self.load_data()

    def on_row_double_click(self, index):
        row = index.row()
        if row == 0:  # Skip header row
            return

        # Get record ID from checkbox
        checkbox_widget = self.table.cellWidget(row, 0)
        if checkbox_widget:
            checkbox = checkbox_widget.findChild(QCheckBox)
            record_id = checkbox.property('record_id')

            # Fetch record data
            record_data = self.db_manager.get_record_by_id(record_id)
            if record_data:
                self.open_edit_dialog(record_data)

    def add_record(self):
        dialog = AddEditDialog(self, mode='add')
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if self.db_manager.add_record(data):
                self.load_data()
                QMessageBox.information(self, 'Success', 'Record added successfully!')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to add record!')

    # def update_record(self):
    #     # Get selected rows via checkboxes
    #     selected_ids = self.get_selected_record_ids()
    #
    #     if not selected_ids:
    #         QMessageBox.warning(self, 'Warning', 'Please select a record to update!')
    #         return
    #
    #     if len(selected_ids) > 1:
    #         QMessageBox.warning(self, 'Warning', 'Please select only one record to update!')
    #         return
    #
    #     record_data = self.db_manager.get_record_by_id(selected_ids[0])
    #     if record_data:
    #         self.open_edit_dialog(record_data)

    def open_edit_dialog(self, record_data):
        dialog = AddEditDialog(self, mode='edit', data=record_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            if self.db_manager.update_record(record_data[0], data):
                self.load_data()
                QMessageBox.information(self, 'Success', 'Record updated successfully!')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to update record!')

    def get_selected_record_ids(self):
        selected_ids = []
        for row in range(1, self.table.rowCount()):  # Skip header row
            checkbox_widget = self.table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    selected_ids.append(checkbox.property('record_id'))
        return selected_ids

    def delete_records(self):
        selected_ids = self.get_selected_record_ids()

        if not selected_ids:
            QMessageBox.warning(self, 'Warning', 'Please select at least one record to delete!')
            return

        # Create confirmation message with selected records
        confirmation_text = f"You are about to delete {len(selected_ids)} record(s):\n\n"

        for record_id in selected_ids:
            record_data = self.db_manager.get_record_by_id(record_id)
            if record_data:
                confirmation_text += f"• {record_data[1]} (Serial: {record_data[8]})\n"

        confirmation_text += "\nAre you sure you want to delete these records?"

        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            confirmation_text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db_manager.delete_records(selected_ids):
                self.load_data()
                QMessageBox.information(self, 'Success', f'{len(selected_ids)} record(s) deleted successfully!')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to delete records!')

