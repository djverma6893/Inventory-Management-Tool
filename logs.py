from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QTextEdit, QSplitter, QLabel,
                             QInputDialog, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QDateTime

class LogsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Logs")
        self.setMinimumSize(800, 600)
        # self.setMinimumWidth(450)
        self.init_ui()
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #create text edit
        self.text_edit = QTextEdit()
        self.text_edit.setText("himayal")
        self.text_edit.setReadOnly(True)
        main_layout.addWidget(self.text_edit)

        #bottom layout
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)

        #export logs
        export_logs_btn= QPushButton("Export logs")
        export_logs_btn.setObjectName("export_logs_btn")
        export_logs_btn.setToolTip("click here Export logs")
        export_logs_btn.clicked.connect(self.export_logs)

        #modify logs
        modify_logs_btn = QPushButton("Modify logs")
        modify_logs_btn.setObjectName("modify_logs_btn")
        modify_logs_btn.setToolTip("click here modify logs")
        modify_logs_btn.clicked.connect(self.modify_logs)

        bottom_layout.addWidget(export_logs_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(modify_logs_btn)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

    def modify_logs(self):
        mes="modify logs clicked"

        self.add_logs(mes)

    def export_logs(self):
        try:
            filename = f"logs_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.txt"
            with open(filename, 'w') as f:
                f.write(self.text_edit.toPlainText())
            QMessageBox.information(self, "Success", f"Logs exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export logs: {str(e)}")

    def add_logs(self, message):
        if self.text_edit is not None:
            self.text_edit.append(message)






