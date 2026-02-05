import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QTextEdit, QSplitter, QLabel,
                             QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor


class LoggedQTableWidget(QTableWidget):
    """Custom QTableWidget that logs all modifications"""

    def __init__(self, rows, columns, log_callback):
        super().__init__(rows, columns)
        self.log_callback = log_callback

        # Connect signals to log functions
        self.itemChanged.connect(self._on_item_changed)
        self.cellClicked.connect(self._on_cell_clicked)

        # Store previous values for change tracking
        self.previous_values = {}

    def _get_timestamp(self):
        """Get current timestamp"""
        return QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")

    def _on_item_changed(self, item):
        """Log when an item's content changes"""
        row = item.row()
        col = item.column()
        new_value = item.text()
        key = (row, col)

        if key in self.previous_values:
            old_value = self.previous_values[key]
            if old_value != new_value:
                self.log_callback(
                    f"[{self._get_timestamp()}] CELL MODIFIED - Row: {row}, Col: {col}, "
                    f"Old Value: '{old_value}' → New Value: '{new_value}'"
                )
        else:
            self.log_callback(
                f"[{self._get_timestamp()}] CELL SET - Row: {row}, Col: {col}, "
                f"Value: '{new_value}'"
            )

        self.previous_values[key] = new_value

    def _on_cell_clicked(self, row, col):
        """Log when a cell is clicked"""
        item = self.item(row, col)
        value = item.text() if item else ""
        self.log_callback(
            f"[{self._get_timestamp()}] CELL CLICKED - Row: {row}, Col: {col}, "
            f"Value: '{value}'"
        )

    def insertRow(self, row):
        """Override insertRow to log the action"""
        super().insertRow(row)
        self.log_callback(
            f"[{self._get_timestamp()}] ROW INSERTED - Position: {row}, "
            f"Total Rows: {self.rowCount()}"
        )

    def insertColumn(self, column):
        """Override insertColumn to log the action"""
        super().insertColumn(column)
        self.log_callback(
            f"[{self._get_timestamp()}] COLUMN INSERTED - Position: {column}, "
            f"Total Columns: {self.columnCount()}"
        )

    def removeRow(self, row):
        """Override removeRow to log the action"""
        # Log row contents before removal
        row_data = []
        for col in range(self.columnCount()):
            item = self.item(row, col)
            row_data.append(item.text() if item else "")

        super().removeRow(row)
        self.log_callback(
            f"[{self._get_timestamp()}] ROW REMOVED - Position: {row}, "
            f"Data: {row_data}, Total Rows: {self.rowCount()}"
        )

        # Update previous_values dict
        keys_to_remove = [k for k in self.previous_values.keys() if k[0] == row]
        for key in keys_to_remove:
            del self.previous_values[key]

    def removeColumn(self, column):
        """Override removeColumn to log the action"""
        # Log column contents before removal
        col_data = []
        for row in range(self.rowCount()):
            item = self.item(row, column)
            col_data.append(item.text() if item else "")

        super().removeColumn(column)
        self.log_callback(
            f"[{self._get_timestamp()}] COLUMN REMOVED - Position: {column}, "
            f"Data: {col_data}, Total Columns: {self.columnCount()}"
        )

        # Update previous_values dict
        keys_to_remove = [k for k in self.previous_values.keys() if k[1] == column]
        for key in keys_to_remove:
            del self.previous_values[key]

    def setItem(self, row, column, item):
        """Override setItem to track initial values"""
        super().setItem(row, column, item)
        if item:
            self.previous_values[(row, column)] = item.text()

    def clear(self):
        """Override clear to log the action"""
        super().clear()
        self.previous_values.clear()
        self.log_callback(
            f"[{self._get_timestamp()}] TABLE CLEARED - All contents removed"
        )

    def clearContents(self):
        """Override clearContents to log the action"""
        super().clearContents()
        self.previous_values.clear()
        self.log_callback(
            f"[{self._get_timestamp()}] TABLE CONTENTS CLEARED - "
            f"Headers preserved, all cell data removed"
        )

    def sortItems(self, column, order=Qt.AscendingOrder):
        """Override sortItems to log the action"""
        order_text = "Ascending" if order == Qt.AscendingOrder else "Descending"
        super().sortItems(column, order)
        self.log_callback(
            f"[{self._get_timestamp()}] TABLE SORTED - Column: {column}, "
            f"Order: {order_text}"
        )


class TableLogApp(QMainWindow):
    """Main application window with table and log viewer"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("QTable Modification Logger")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize log_text first (before creating table)
        self.log_text = None

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create splitter for table and log
        splitter = QSplitter(Qt.Horizontal)

        # Left side - Table and controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Table label
        table_label = QLabel("Editable Table (Click cells to edit)")
        table_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        left_layout.addWidget(table_label)

        # Create logged table (log_text will be created before sample data is added)
        self.table = LoggedQTableWidget(5, 4, self.add_log)
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'City', 'Email'])

        left_layout.addWidget(self.table)

        # Control buttons
        button_layout = QHBoxLayout()

        add_row_btn = QPushButton("Add Row")
        add_row_btn.clicked.connect(self.add_row)
        button_layout.addWidget(add_row_btn)

        remove_row_btn = QPushButton("Remove Selected Row")
        remove_row_btn.clicked.connect(self.remove_row)
        button_layout.addWidget(remove_row_btn)

        add_col_btn = QPushButton("Add Column")
        add_col_btn.clicked.connect(self.add_column)
        button_layout.addWidget(add_col_btn)

        remove_col_btn = QPushButton("Remove Selected Column")
        remove_col_btn.clicked.connect(self.remove_column)
        button_layout.addWidget(remove_col_btn)

        sort_btn = QPushButton("Sort by Column 0")
        sort_btn.clicked.connect(lambda: self.table.sortItems(0))
        button_layout.addWidget(sort_btn)

        clear_contents_btn = QPushButton("Clear Contents")
        clear_contents_btn.clicked.connect(self.table.clearContents)
        button_layout.addWidget(clear_contents_btn)

        left_layout.addLayout(button_layout)

        # Right side - Log viewer
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Log label
        log_label = QLabel("Modification Log")
        log_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        right_layout.addWidget(log_label)

        # Log text area - CREATE THIS BEFORE ADDING SAMPLE DATA
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                font-family: 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
        right_layout.addWidget(self.log_text)

        # Log control buttons
        log_button_layout = QHBoxLayout()

        clear_log_btn = QPushButton("Clear Log")
        clear_log_btn.clicked.connect(self.clear_log)
        log_button_layout.addWidget(clear_log_btn)

        export_log_btn = QPushButton("Export Log")
        export_log_btn.clicked.connect(self.export_log)
        log_button_layout.addWidget(export_log_btn)

        right_layout.addLayout(log_button_layout)

        # Add widgets to splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter)

        # NOW add sample data after log_text is created
        sample_data = [
            ['John Doe', '30', 'New York', 'john@email.com'],
            ['Jane Smith', '25', 'Los Angeles', 'jane@email.com'],
            ['Bob Johnson', '35', 'Chicago', 'bob@email.com'],
            ['Alice Brown', '28', 'Houston', 'alice@email.com'],
            ['Charlie Wilson', '32', 'Phoenix', 'charlie@email.com']
        ]

        for row, row_data in enumerate(sample_data):
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(value))

        # Initial log message
        self.add_log(f"[{QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}] "
                     f"Application started - Table initialized with {self.table.rowCount()} rows "
                     f"and {self.table.columnCount()} columns")

    def add_log(self, message):
        """Add a message to the log"""
        # Check if log_text is initialized
        if self.log_text is not None:
            self.log_text.append(message)
            # Auto-scroll to bottom
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def add_row(self):
        """Add a new row to the table"""
        self.table.insertRow(self.table.rowCount())

    def remove_row(self):
        """Remove the currently selected row"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to remove")

    def add_column(self):
        """Add a new column to the table"""
        col_name, ok = QInputDialog.getText(self, "Add Column", "Enter column name:")
        if ok and col_name:
            col_count = self.table.columnCount()
            self.table.insertColumn(col_count)
            self.table.setHorizontalHeaderItem(col_count, QTableWidgetItem(col_name))

    def remove_column(self):
        """Remove the currently selected column"""
        current_col = self.table.currentColumn()
        if current_col >= 0:
            self.table.removeColumn(current_col)
        else:
            QMessageBox.warning(self, "Warning", "Please select a column to remove")

    def clear_log(self):
        """Clear the log text area"""
        self.log_text.clear()
        self.add_log(f"[{QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}] "
                     f"Log cleared")

    def export_log(self):
        """Export log to a text file"""
        try:
            filename = f"table_log_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.txt"
            with open(filename, 'w') as f:
                f.write(self.log_text.toPlainText())
            QMessageBox.information(self, "Success", f"Log exported to {filename}")
            self.add_log(f"[{QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}] "
                         f"Log exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export log: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TableLogApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()