from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtGui import QFont
from database_mongodb import DatabaseManager

class AddEditDialog(QDialog):
    def __init__(self, parent=None, mode='add', data=None):
        super().__init__(parent)
        self.mode = mode
        self.data = data
        print(self.data)
        self.setWindowTitle('Add New Record' if mode == 'add' else 'Edit Record')
        self.setMinimumWidth(450)
        self.setStyleSheet(self.get_dialog_style())
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create input fields
        # col_name=self.parent().header_name()
        self.col_nm= DatabaseManager().get_header_id()
        print(self.col_nm)
        self.col_name=[f+'_input' for f in self.col_nm]

        print(self.col_name,"hanji")
        # Style inputs
        input_style = """
                    QLineEdit, QComboBox {
                        padding: 8px;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        font-size: 13px;
                    }
                    QLineEdit:focus, QComboBox:focus {
                        border: 2px solid #4CAF50;
                    }
                """
        for i, input in enumerate(self.col_name):
            if(input=="hcl_laptop_input"):
                col=QComboBox()
                col.addItems(['YES', 'NO'])
                col.setStyleSheet(input_style)
                # self.col_name[i]=QComboBox()
                # self.col_name[i].addItem(['YES', 'NO'])
                # self.col_name[i].setStyleSheet(input_style)
                self.col_name[i]=col
            else:
                col=QLineEdit()
                col.setStyleSheet(input_style)
                self.col_name[i]=col

        # self.team_member_input = QLineEdit()
        # self.laptop1_sn_input = QLineEdit()
        # self.laptop2_sn_input = QLineEdit()
        # self.intern_phone_input = QLineEdit()
        # self.test_phone1_input = QLineEdit()
        # self.test_phone2_input = QLineEdit()
        # self.hcl_laptop_input = QComboBox()
        # self.hcl_laptop_input.addItems(['YES', 'NO'])
        # self.serial_no_input = QLineEdit()


        # for widget in [self.team_member_input, self.laptop1_sn_input, self.laptop2_sn_input,
        #                self.intern_phone_input, self.test_phone1_input, self.test_phone2_input,
        #                self.hcl_laptop_input, self.serial_no_input]:
        #     widget.setStyleSheet(input_style)

        # If editing, populate fields
        if self.data:
            self.data.pop('id')
        if self.mode == 'edit' and self.data:
            # print(self.data, "dialogs.py")
            # self.col_head=[self.team_member_input,self.laptop1_sn_input,self.laptop2_sn_input,self.intern_phone_input,self.test_phone1_input,self.test_phone2_input,self.hcl_laptop_input,self.serial_no_input]

            # self.team_member_input.setText(str(self.data[1]))
            # self.laptop1_sn_input.setText(str(self.data[2]) if self.data[2] else '')
            # self.laptop2_sn_input.setText(str(self.data[3]) if self.data[3] else '')
            # self.intern_phone_input.setText(str(self.data[4]) if self.data[4] else '')
            # self.test_phone1_input.setText(str(self.data[5]) if self.data[5] else '')
            # self.test_phone2_input.setText(str(self.data[6]) if self.data[6] else '')
            # self.hcl_laptop_input.setCurrentText(str(self.data[7]))
            # self.serial_no_input.setText(str(self.data[8]) if self.data[8] else '')
            for i, dd in enumerate(self.data):
                # print(self.data[dd])
                if(dd=="hcl_laptop"):
                    self.col_name[i].setCurrentText(self.data[dd])
                else:
                    self.col_name[i].setText(str(self.data[dd]) if self.data[dd] else '')


        # Create labels with bold font
        label_font = QFont()
        label_font.setBold(True)

        # labels = ['Team Member:', 'Laptop1 SN:', 'Laptop2 SN:', 'Intern Phone:',
        #           'Test Phone1:', 'Test Phone2:', 'HCL Laptop:', 'Serial NO:']
        labels = DatabaseManager().get_header_name()

        # inputs = [self.team_member_input, self.laptop1_sn_input, self.laptop2_sn_input,
        #           self.intern_phone_input, self.test_phone1_input, self.test_phone2_input,
        #           self.hcl_laptop_input, self.serial_no_input]

        for label_text, input_widget in zip(labels, self.col_name):
            label = QLabel(label_text)
            label.setFont(label_font)
            layout.addRow(label, input_widget)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        save_btn = QPushButton('Save')
        cancel_btn = QPushButton('Cancel')

        save_btn.setMinimumHeight(40)
        cancel_btn.setMinimumHeight(40)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def get_data(self):
        input_data={}
        for i,name,dd in enumerate(zip(self.col_nm,self.col_name)):
            input_data.append(name,self.col_name[i].text())
        print(input_data)
        return input_data
        return {
            'team_member': self.team_member_input.text(),
            'laptop1_sn': self.laptop1_sn_input.text() or None,
            'laptop2_sn': self.laptop2_sn_input.text() or None,
            'intern_phone': self.intern_phone_input.text() or None,
            'test_phone1': self.test_phone1_input.text() or None,
            'test_phone2': self.test_phone2_input.text() or None,
            'hcl_laptop': self.hcl_laptop_input.currentText(),
            'serial_no': self.serial_no_input.text() or None
        }

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

