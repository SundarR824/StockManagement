import sys
from pathlib import Path
from StockManager.services import StockGroupServices, StockServices

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidgetItem, QWidget, QCommandLinkButton, QSpinBox, QDialog,
    QTextEdit
)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_path = f"{Path.cwd()}/ui"

        self.stock_group_services = StockGroupServices()
        self.stock_services = StockServices()

        self.load_main_window()

    def load_main_window(self):
        uic.loadUi(f"{self.project_path}/StockManagement.ui", self)

        stock_operations_button = self.findChild(QCommandLinkButton, "AddStockMenuButton")
        stock_operations_button.clicked.connect(self.add_stock_operations_page)
        self.setWindowTitle("Stock Management")
        self.load_stock_group_data()

    def handle_button_click(self, table_widget, row, stock_indicator):
        """
        This indicator is to get lower stock and all the stocks. 0 = all stocks, 1 = low stocks
        """
        values = []
        for col in range(table_widget.columnCount() - 1):  # Exclude the button column
            item = table_widget.item(row, col)
            values.append(item.text() if item else "")

        stock_group_title = self.findChild(QLabel, "StockIndicatorLabel")
        stock_group_title.setText(f"{values[1]} : {values[2]}")

        self.load_stock_data(row, stock_indicator)

    # Main Window Data Loading (or) Reading Stocks and stock Group Operations
    # -----------------------------------------------------------------------
    def load_stock_group_data(self):  # Load all the Stock Groups
        stock_group_table = self.findChild(QTableWidget, "StockGroupTable")
        stock_group_table.setColumnWidth(0, 130)
        stock_group_table.setColumnWidth(1, 250)
        stock_group_table.setColumnWidth(2, 315)
        stock_group_table.setColumnWidth(3, 130)
        stock_group_table.setColumnWidth(4, 130)
        stock_group_table.setColumnWidth(5, 130)
        stock_group_table.setColumnWidth(6, 130)

        all_low_stocks_button = self.findChild(QPushButton, "LowStocksButton")
        all_low_stocks_button.clicked.connect(lambda _,: self.handle_button_click(stock_group_table, 0, 2))

        # fetching all stocks to display in UI
        # ------------------------------------
        data = self.stock_group_services.get_all_stock_groups()

        stock_group_table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                stock_group_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Add the All Stock button in a new column
            all_stocks_button = QPushButton("Get Stocks")
            all_stocks_button.setFixedSize(100, 30)
            all_stocks_button.clicked.connect(lambda _, r=int(row_data[0]): self.handle_button_click(stock_group_table, r, 0))
            stock_group_table.setCellWidget(row_idx, len(row_data), all_stocks_button)

            # Add the Low Stocks button in another new column
            low_stocks_button = QPushButton("Low Stocks")
            low_stocks_button.setFixedSize(100, 30)
            low_stocks_button.clicked.connect(lambda _, r=int(row_data[0]): self.handle_button_click(stock_group_table, r, 1))
            stock_group_table.setCellWidget(row_idx, len(row_data) + 1, low_stocks_button)

            # Add the Edit Stocks button in another new column
            edit_group_button = QPushButton("Edit Group")
            edit_group_button.setFixedSize(110, 32)
            edit_group_button.clicked.connect(lambda r_data, r=row_data: self.update_stock_group_ui(r))
            stock_group_table.setCellWidget(row_idx, len(row_data) + 2, edit_group_button)

            # Add the Delete Stocks button in another new column
            edit_group_button = QPushButton("Delete Group")
            edit_group_button.setFixedSize(125, 32)
            edit_group_button.clicked.connect(lambda r_data, r=row_data: self.delete_stock_group_ui(r))
            stock_group_table.setCellWidget(row_idx, len(row_data) + 3, edit_group_button)

    def load_stock_data(self, group_id: int, stock_indicator: int):  # Load All the Stocks
        stock_table = self.findChild(QTableWidget, "StockTable")
        stock_table.setColumnWidth(0, 100)
        stock_table.setColumnWidth(1, 150)
        stock_table.setColumnWidth(2, 140)
        stock_table.setColumnWidth(3, 150)
        stock_table.setColumnWidth(4, 200)
        stock_table.setColumnWidth(5, 135)
        stock_table.setColumnWidth(6, 100)
        stock_table.setColumnWidth(7, 148)
        stock_table.setColumnWidth(8, 148)

        if stock_indicator == 1: # Get lower stocks by its group id
            data = self.stock_services.get_lower_stock(group_id)
        elif stock_indicator == 2: # Get all the lower stocks for all stocks
            data = self.stock_services.get_lower_stock(0)
        else:
            data = self.stock_services.get_all_stocks(group_id)

        stock_table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if int(row_data[2]) < int(row_data[3]):
                    item.setBackground(QBrush(QColor(255, 128, 128)))
                stock_table.setItem(row_idx, col_idx, item)

            # Add the Edit Stocks button in another new column
            edit_stock_button = QPushButton("Edit Stock")
            edit_stock_button.setFixedSize(110, 32)
            edit_stock_button.clicked.connect(lambda r_data, r=row_data: self.update_stock_ui(r))
            stock_table.setCellWidget(row_idx, len(row_data), edit_stock_button)

            # Add the Delete Stocks button in another new column
            delete_stock_button = QPushButton("Delete Stock")
            delete_stock_button.setFixedSize(120, 32)
            delete_stock_button.clicked.connect(lambda r_data, r=row_data: self.delete_stock_ui(r))
            stock_table.setCellWidget(row_idx, len(row_data) + 1, delete_stock_button)

    # stocks and stock group operations
    # ---------------------------------
    def add_stock_operations_page(self):
        # Create a QWidget and load the new .ui file
        stock_operations = QWidget()
        uic.loadUi(f"{self.project_path}/StockOperations.ui", stock_operations)

        # Set the new page as the central widget
        self.setCentralWidget(stock_operations)

        create_stock_group_button = self.findChild(QPushButton, "CreateStockGroupButton")
        create_stock_group_button.clicked.connect(self.create_stock_group_ui)

        create_stock_button = self.findChild(QPushButton, "CreateStockButton")
        create_stock_button.clicked.connect(self.create_stock_ui)

        stock_list_page_button = self.findChild(QCommandLinkButton, "BackToStockList")
        stock_list_page_button.clicked.connect(self.load_main_window)

        stock_group_dropdown = self.findChild(QComboBox, "StockGroupBox")
        all_group_names = self.stock_group_services.get_all_stock_group_names()
        stock_group_dropdown.addItems(all_group_names)

    # Create Stock Group
    # ------------------
    def create_stock_group_ui(self):
        group_name = self.findChild(QLineEdit, "GroupNameText").text()
        group_desc = self.findChild(QLineEdit, "GroupDescText").text()

        if not group_name or len(group_name) <= 3:
            warning_text = self.findChild(QLabel, "GroupWarningText")
            warning_text.setText("*Group Name needed 4 or more letters")
            warning_text.setStyleSheet("color: red")
        else:
            warning_text = self.findChild(QLabel, "GroupWarningText")
            created_group = self.stock_group_services.create_stock_group(group_name, group_desc)
            warning_text.setText(created_group['message'])
            warning_text.setStyleSheet("color: Blue")

    # Update Stock Group
    # ------------------
    def update_stock_group_ui(self, row_data):
        edit = QDialog()
        uic.loadUi(f"{self.project_path}/EditStockGroup.ui", edit)
        edit.setWindowTitle("Edit Stock Group")

        name_text = edit.findChild(QLineEdit, "NameText")
        name_text.setText(row_data[1])

        desc_text = edit.findChild(QTextEdit, "DescText")
        desc_text.setText(row_data[2])

        def handle_accept():
            self.stock_group_services.update_stock_group(
                group_id=row_data[0],
                attr={"name": name_text.text(), "desc": desc_text.toPlainText()}
            )
            self.load_stock_group_data()

        edit.accepted.connect(handle_accept)
        edit.setWindowModality(Qt.ApplicationModal)
        edit.exec_()

    # Delete Stock Group
    # ------------------
    def delete_stock_group_ui(self, row_data):
        delete = QDialog()
        uic.loadUi(f"{self.project_path}/DeleteStockGroup.ui", delete)
        delete.setWindowTitle("Delete Stock Group")

        warning_text = delete.findChild(QLabel, "DeleteGroupWarningText")
        warning_text.setText(f"Are you sure to Delete Group belt {row_data[1]}")

        def accept_stock_group_delete():
            data = self.stock_services.get_all_stocks(row_data[0])
            if not data:
                self.stock_group_services.delete_stock_group(row_data[0])
                self.load_stock_group_data()

        delete.accepted.connect(accept_stock_group_delete)
        delete.setWindowModality(Qt.ApplicationModal)
        delete.exec_()

    # Create Stock
    # ------------
    def create_stock_ui(self):
        stock_name = self.findChild(QLineEdit, "StockNameText").text()
        stock_desc = self.findChild(QLineEdit, "StockDescText").text()
        stock_mini_count = self.findChild(QSpinBox, "StockMiniCount").value()
        stock_group_dropdown = self.findChild(QComboBox, "StockGroupBox").currentText()
        stock_group_id = stock_group_dropdown.split('-')[-1]

        if not stock_name or len(stock_name) <= 3:
            warning_text = self.findChild(QLabel, "StockWarningText")
            warning_text.setText("*Stock Name needed 4 or more letters")
            warning_text.setStyleSheet("color: red")
        else:
            warning_text = self.findChild(QLabel, "StockWarningText")
            stock_args = self.stock_services.StockArgs(
                group_id=stock_group_id, stock_name=stock_name, stock_desc=stock_desc,
                mini_count=stock_mini_count, count=0
            )
            created_stock = self.stock_services.create_stock(stock_args)
            warning_text.setText(created_stock['message'])
            warning_text.setStyleSheet("color: Blue")

    # Update Stock
    # ------------
    def update_stock_ui(self, row_data):
        edit = QDialog()
        uic.loadUi(f"{self.project_path}/EditStock.ui", edit)
        edit.setWindowTitle("Edit Stock Group")

        name_text = edit.findChild(QLineEdit, "NameText")
        name_text.setText(row_data[1])

        desc_text = edit.findChild(QTextEdit, "DescText")
        desc_text.setText(row_data[4])

        count_text = edit.findChild(QSpinBox, "CountBox")
        count_text.setValue(row_data[2])

        min_count_text = edit.findChild(QSpinBox, "MiniCountBox")
        min_count_text.setValue(row_data[3])

        def handle_accept():
            self.stock_services.update_stock(
                stock_id=row_data[0],
                attr={
                    "name": name_text.text(),
                    "desc": desc_text.toPlainText(),
                    "count": count_text.value(),
                    "mini_count": min_count_text.value(),
                    "group_id": row_data[-1]
                }
            )
            self.load_stock_data(row_data[-1], 0)

        edit.accepted.connect(handle_accept)
        edit.setWindowModality(Qt.ApplicationModal)
        edit.exec_()

    # Delete Stock
    # ------------
    def delete_stock_ui(self, row_data):
        delete = QDialog()
        uic.loadUi(f"{self.project_path}/DeleteStockGroup.ui", delete)
        delete.setWindowTitle("Delete Stock")

        warning_text = delete.findChild(QLabel, "DeleteGroupWarningText")
        warning_text.setText(f"Are you sure to Delete Stock \n '{row_data[1]}'")

        def accept_stock_delete():
            self.stock_services.delete_stock(row_data[0])
            self.load_stock_data(row_data[6], 0)

        delete.accepted.connect(accept_stock_delete)
        delete.setWindowModality(Qt.ApplicationModal)
        delete.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
