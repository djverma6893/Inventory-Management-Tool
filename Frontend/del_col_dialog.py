from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QCheckBox, QMessageBox, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt


class DeleteColumnDialog(QDialog):
    def __init__(self, column_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Columns")
        self.setMinimumWidth(450)
        self.column_names = column_names  # list of column names
        self.checkboxes = []

        self.setStyleSheet(self.get_dialog_style())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel("Select columns to delete:")
        layout.addWidget(label)

        # Scroll area for many columns
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        scroll_layout = QVBoxLayout(container)

        for col in self.column_names:
            checkbox = QCheckBox(col)
            self.checkboxes.append(checkbox)
            scroll_layout.addWidget(checkbox)

        scroll_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Buttons
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete")
        cancel_btn = QPushButton("Cancel")

        delete_btn.clicked.connect(self.confirm_delete)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def confirm_delete(self):
        selected = self.get_selected_columns()

        if not selected:
            QMessageBox.warning(
                self, "No Selection", "Please select at least one column."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the following columns?\n\n"
            + "\n".join(selected),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.accept()

    def get_selected_columns(self):
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]

    def get_dialog_style(self):
        return """
            QDialog {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #e53935;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c62828;
            }
        """
