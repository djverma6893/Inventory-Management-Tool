from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout
)
from database_mongodb import DatabaseManager
# from inventory_page import InventoryPage
from trio import sleep


class ColumnInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Column")
        self.setMinimumWidth(450)
        # self.database_manager = DatabaseManager()
        self.setStyleSheet(self.get_dialog_style())
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel("Enter column name:")
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("e.g. employee_id")
        label2=QLabel("Column id:")
        self.column_id = QLineEdit()
        self.column_id.setPlaceholderText("e.g. employee_id")

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Add")
        cancel_btn = QPushButton("Cancel")

        ok_btn.clicked.connect(self.accepted)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(label2)
        layout.addWidget(self.column_id)
        layout.addLayout(btn_layout)

    def get_column_name(self):
        return self.line_edit.text().strip()
    def get_column_id(self):
        return self.column_id.text().strip()
    def get_dialog_style(self):
        return """
            QDialog {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """

    def accepted(self):
        if(self.get_column_name()=="" or self.get_column_name()==None):
            print("Please enter column name")
            self.reject()
        else:
            self.database_manager=DatabaseManager()
            self.database_manager.add_new_column(self.get_column_name(),self.get_column_id())
            print("Accepted")
            # InventoryPage(self,None).init_ui()
            self.accept()

        # return self.get_column_name()
    # def reject(self):
    #     print("Rejected")
