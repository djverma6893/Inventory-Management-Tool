from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import csv


class MenuBarManager:
    """Manages menu bar and its functions for the inventory page"""

    def __init__(self, parent_widget, db_manager, user_info):
        """
        Initialize menu bar manager

        Args:
            parent_widget: The parent widget (InventoryPage)
            db_manager: Database manager instance
            user_info: Current user information dictionary
        """
        self.parent = parent_widget
        self.db_manager = db_manager
        self.user_info = user_info

    def create_menu_bar(self):
        """Create and return the menu bar with all menus and actions"""
        menubar = QMenuBar()
        menubar.setStyleSheet(self._get_menu_style())

        # Create File Menu
        self._create_file_menu(menubar)

        # Create Help Menu
        self._create_help_menu(menubar)

        return menubar

    def _create_file_menu(self, menubar):
        """Create File menu with Import, Export, and Exit actions"""
        file_menu = menubar.addMenu('📁 File')

        # Import Action
        import_action = QAction('📥 Import from CSV', self.parent)
        import_action.setShortcut('Ctrl+I')
        import_action.setStatusTip('Import data from CSV file')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        # Export Action
        export_action = QAction('📤 Export to CSV', self.parent)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Export data to CSV file')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Exit Action
        exit_action = QAction('🚪 Exit', self.parent)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.exit_application)
        file_menu.addAction(exit_action)

    def _create_help_menu(self, menubar):
        """Create Help menu with Help and About actions"""
        help_menu = menubar.addMenu('❓ Help')

        # Help Action
        help_action = QAction('📖 Help', self.parent)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Show help information')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        help_menu.addSeparator()

        # About Action
        about_action = QAction('ℹ️ About', self.parent)
        about_action.setStatusTip('About this application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def import_data(self):
        """Import data from CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 'Import CSV File', '', 'CSV Files (*.csv);;All Files (*)'
        )

        if not file_path:
            return

        try:
            imported_count = 0
            skipped_count = 0
            error_details = []

            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)

                # Check if required columns exist
                required_columns = ['team_member']
                if not all(col in csv_reader.fieldnames for col in required_columns):
                    QMessageBox.warning(
                        self.parent,
                        'Invalid CSV Format',
                        'CSV file must contain at least the "team_member" column.'
                    )
                    return

                for row_num, row in enumerate(csv_reader, start=2):  # start=2 for row number (header is row 1)
                    try:
                        data = {
                            'team_member': row.get('team_member', '').strip(),
                            'laptop1_sn': row.get('laptop1_sn', '').strip(),
                            'laptop2_sn': row.get('laptop2_sn', '').strip(),
                            'intern_phone': row.get('intern_phone', '').strip(),
                            'test_phone1': row.get('test_phone1', '').strip(),
                            'test_phone2': row.get('test_phone2', '').strip(),
                            'hcl_laptop': row.get('hcl_laptop', 'NO').strip().upper(),
                            'serial_no': row.get('serial_no', '').strip()
                        }

                        # Validate team_member is not empty
                        if not data['team_member']:
                            error_details.append(f"Row {row_num}: team_member is required")
                            skipped_count += 1
                            continue

                        # Ensure hcl_laptop is YES or NO
                        if data['hcl_laptop'] not in ['YES', 'NO']:
                            data['hcl_laptop'] = 'NO'

                        if self.db_manager.add_record(data):
                            imported_count += 1
                        else:
                            error_details.append(f"Row {row_num}: Database insertion failed")
                            skipped_count += 1

                    except Exception as e:
                        error_details.append(f"Row {row_num}: {str(e)}")
                        skipped_count += 1

            # Refresh the table in parent
            if hasattr(self.parent, 'load_data'):
                self.parent.load_data()

            # Show result message
            message = f'✅ Successfully imported {imported_count} record(s)!'
            if skipped_count > 0:
                message += f'\n⚠️ {skipped_count} record(s) were skipped due to errors.'
                if error_details:
                    message += '\n\nError details:\n' + '\n'.join(error_details[:5])  # Show first 5 errors
                    if len(error_details) > 5:
                        message += f'\n... and {len(error_details) - 5} more errors'

            QMessageBox.information(self.parent, 'Import Complete', message)

        except Exception as e:
            QMessageBox.critical(
                self.parent,
                'Import Error',
                f'Failed to import data:\n{str(e)}'
            )

    def export_data(self):
        """Export data to CSV file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            'Export CSV File',
            'equipment_export.csv',
            'CSV Files (*.csv);;All Files (*)'
        )

        if not file_path:
            return

        try:
            rows = self.db_manager.fetch_all_records()

            if not rows:
                QMessageBox.warning(self.parent, 'No Data', 'No data available to export!')
                return

            # Define CSV headers
            headers = ['id', 'team_member', 'laptop1_sn', 'laptop2_sn',
                       'intern_phone', 'test_phone1', 'test_phone2',
                       'hcl_laptop', 'serial_no']

            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.DictWriter(file, fieldnames=headers)
                csv_writer.writeheader()

                for row in rows:
                    # Create a new dict with only the headers we want
                    export_row = {}
                    for header in headers:
                        export_row[header] = row.get(header, '')
                    csv_writer.writerow(export_row)

            QMessageBox.information(
                self.parent,
                'Export Successful',
                f'✅ Successfully exported {len(rows)} record(s) to:\n{file_path}'
            )

        except Exception as e:
            QMessageBox.critical(
                self.parent,
                'Export Error',
                f'Failed to export data:\n{str(e)}'
            )

    def show_help(self):
        """Show help information dialog"""
        help_text = """
        <h2>📚 Equipment Inventory Management - Help</h2>

        <h3>📋 Basic Operations:</h3>
        <ul>
            <li><b>Add Record:</b> Click the "➕ Add Record" button to add new equipment</li>
            <li><b>Edit Record:</b> Double-click on any row to edit the record</li>
            <li><b>Delete Records:</b> Select records using checkboxes and click "🗑️ Delete Selected"</li>
            <li><b>Search:</b> Use the search box to filter records by team member or serial number</li>
            <li><b>Refresh:</b> Click "🔄 Refresh" to reload all data from the database</li>
        </ul>

        <h3>📁 File Operations:</h3>
        <ul>
            <li><b>Import (Ctrl+I):</b> Import equipment records from a CSV file</li>
            <li><b>Export (Ctrl+E):</b> Export all records to a CSV file for backup or sharing</li>
        </ul>

        <h3>📊 CSV Format for Import:</h3>
        <p>When importing, your CSV file should have these columns (header row required):</p>
        <ul>
            <li><b>team_member</b> - Required, name of the team member</li>
            <li><b>laptop1_sn</b> - Optional, first laptop serial number</li>
            <li><b>laptop2_sn</b> - Optional, second laptop serial number</li>
            <li><b>intern_phone</b> - Optional, intern phone number</li>
            <li><b>test_phone1</b> - Optional, first test phone</li>
            <li><b>test_phone2</b> - Optional, second test phone</li>
            <li><b>hcl_laptop</b> - Optional, YES or NO (default: NO)</li>
            <li><b>serial_no</b> - Optional, serial number</li>
        </ul>

        <h3>⌨️ Keyboard Shortcuts:</h3>
        <ul>
            <li><b>Ctrl+I:</b> Import data from CSV</li>
            <li><b>Ctrl+E:</b> Export data to CSV</li>
            <li><b>Ctrl+Q:</b> Exit application</li>
            <li><b>F1:</b> Show this help dialog</li>
        </ul>

        <h3>💡 Tips:</h3>
        <ul>
            <li>Use the search function to quickly find specific equipment or team members</li>
            <li>Export your data regularly to create backups</li>
            <li>Double-check your CSV format before importing to avoid errors</li>
            <li>You can select multiple records for bulk deletion</li>
        </ul>

        <p style='margin-top: 20px; color: #7f8c8d;'>
        <i>For technical support, contact your system administrator.</i>
        </p>
        """

        msg = QMessageBox(self.parent)
        msg.setWindowTitle('Help - Equipment Inventory')
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_about(self):
        """Show about dialog with application information"""
        about_text = """
        <h2>🏢 Equipment Inventory Management System</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p><b>Release Date:</b> January 2026</p>
        <p><b>Database:</b> MongoDB</p>

        <hr>

        <h3>📝 Description:</h3>
        <p>A comprehensive inventory management system designed for tracking team equipment 
        including laptops, phones, and other electronic devices. This system provides 
        an intuitive interface for managing equipment assignments and maintaining 
        accurate inventory records.</p>

        <h3>✨ Key Features:</h3>
        <ul>
            <li>✅ User authentication with role-based access control</li>
            <li>✅ Create, read, update, and delete equipment records</li>
            <li>✅ Advanced search and filter functionality</li>
            <li>✅ Import/Export data via CSV format</li>
            <li>✅ Secure password hashing (SHA-256)</li>
            <li>✅ Real-time data synchronization with MongoDB</li>
            <li>✅ User-friendly graphical interface</li>
            <li>✅ Keyboard shortcuts for productivity</li>
        </ul>

        <h3>🛠️ Technology Stack:</h3>
        <ul>
            <li><b>Programming Language:</b> Python 3.x</li>
            <li><b>GUI Framework:</b> PyQt5</li>
            <li><b>Database:</b> MongoDB</li>
            <li><b>Security:</b> SHA-256 Password Hashing</li>
        </ul>

        <hr>

        <h3>👤 Current Session:</h3>
        <p><b>User:</b> {}</p>
        <p><b>Role:</b> {}</p>
        <p><b>Full Name:</b> {}</p>

        <hr>

        <p style='margin-top: 20px; text-align: center; color: #7f8c8d;'>
        <i>© 2026 Equipment Inventory Management System<br>
        All rights reserved.<br><br>
        Developed with ❤️ using Python and PyQt5</i>
        </p>
        """.format(
            self.user_info.get('username', 'Unknown'),
            self.user_info.get('role', 'user').upper(),
            self.user_info.get('full_name', 'Unknown User')
        )

        msg = QMessageBox(self.parent)
        msg.setWindowTitle('About - Equipment Inventory')
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def exit_application(self):
        """Exit the application with confirmation"""
        reply = QMessageBox.question(
            self.parent,
            'Exit Application',
            'Are you sure you want to exit the application?\n\nAny unsaved changes will be lost.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Try to close the parent window (main application)
            if self.parent.parent_window:
                self.parent.parent_window.close()
            else:
                # Fallback: close the current widget
                self.parent.close()

    def _get_menu_style(self):
        """Return the stylesheet for the menu bar"""
        return """
            QMenuBar {
                background-color: #34495e;
                color: white;
                font-size: 14px;
                font-weight: 500;
                padding: 5px;
                border-bottom: 3px solid #2c3e50;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 15px;
                margin: 2px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #2c3e50;
            }
            QMenuBar::item:pressed {
                background-color: #1a252f;
            }
            QMenu {
                background-color: white;
                border: 2px solid #34495e;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 10px 30px;
                color: #2c3e50;
                border-radius: 3px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #bdc3c7;
                margin: 5px 10px;
            }
        """