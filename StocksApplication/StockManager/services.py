"""
This file contains the business logic of the application, acting
as an intermediary between the data access layer (repositories.py)
and higher-level application workflows.

It processes data, enforces business rules, and ensures the integrity of
operations before interacting with the database or returning results.
"""
import sys, os
from dataclasses import dataclass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .repositories import StockGroupRepository, StockRepository

class StockGroupServices:
    def __init__(self):
        self.stock_group_repo = StockGroupRepository()

    def get_all_stock_groups(self):
        all_stock_group = self.stock_group_repo.fetch_all_stock_group()

        all_stock_group_list = list()
        for stock_grp in all_stock_group:
            all_stock_group_list.append((stock_grp.id, stock_grp.group_name, stock_grp.description))
        return all_stock_group_list

    def get_all_stock_group_names(self):
        all_stock_group = self.stock_group_repo.fetch_all_stock_group()

        all_stock_group_list = list()
        for stock_grp in all_stock_group:
            all_stock_group_list.append(f"{stock_grp.group_name} - {stock_grp.id}")
        return all_stock_group_list

    def create_stock_group(self, name: str, desc: str) -> dict:
        create_group = self.stock_group_repo.create_stock_group(name, desc)

        if not create_group:
            return {"message": "Problem with Stock Group Creation Contact Developer", "status": 500}

        return {"message": f"stock group '{name}' successfully created", "status": 200}

    def update_stock_group(self, group_id: int, attr: dict) -> dict:
        update_group = self.stock_group_repo.update_stock_group(group_id, attr)

        if not update_group:
            return {"message": "Problem with Stock Group Update Contact Developer", "status": 500}

        return {"message": f"stock group '{attr['name']}' successfully deleted", "status": 200}

    def delete_stock_group(self, group_id: int) -> dict:
        delete_group = self.stock_group_repo.delete_stock_group(group_id)

        if not delete_group:
            return {"message": "Problem with Stock Group Update Contact Developer", "status": 500}

        return {"message": f"stock group successfully updated", "status": 200}


class StockServices:
    def __init__(self):
        self.stock_repo = StockRepository()

    def get_all_stocks(self, group_id: int) -> list:
        all_stocks = self.stock_repo.fetch_all_stocks(group_id)

        all_stock_list = list()
        for stocks in all_stocks:
            if stocks.minimum_count > stocks.count:
                order_quantity = stocks.minimum_count - stocks.count
            else:
                order_quantity = 0
            all_stock_list.append(
                (
                    stocks.id, stocks.stock_name,
                    stocks.count, stocks.minimum_count,
                    stocks.description, order_quantity,
                    stocks.stock_group_id
                )
            )
        return all_stock_list

    @dataclass
    class StockArgs:
        group_id: int
        stock_name: str
        stock_desc: str
        count: int
        mini_count: int

    def create_stock(self, stock_args: StockArgs) -> dict:
        create_group = self.stock_repo.create_stock(
            stock_name=stock_args.stock_name, group_id=stock_args.group_id,
            stock_desc=stock_args.stock_desc, count=stock_args.count,
            mini_count=stock_args.mini_count
        )

        if not create_group:
            return {"message": "Problem with Stock Creation Contact Developer", "status": 500}

        return {"message": f"Stock '{stock_args.stock_name}' successfully created", "status": 200}

    def get_lower_stock(self, group_id: int = 0) -> list:
        all_stocks = self.stock_repo.fetch_all_stocks(group_id)
        low_stock_list = list()
        for stocks in all_stocks:
            if stocks.minimum_count > stocks.count:
                order_quantity = stocks.minimum_count - stocks.count
                low_stock_list.append(
                    (
                        stocks.id, stocks.stock_name,
                        stocks.count, stocks.minimum_count,
                        stocks.description, order_quantity,
                        stocks.stock_group_id
                    )
                )

        return low_stock_list

    def update_stock(self, stock_id: int, attr: dict):
        edit_stock = self.stock_repo.update_stock(stock_id=stock_id, attr=attr)
        if not edit_stock:
            return {"message": "Problem with Stock Group Update Contact Developer", "status": 500}

        return {"message": f"stock group '{attr['name']}' successfully deleted", "status": 200}

    def delete_stock(self, stock_id: int) -> dict:
        delete_stock = self.stock_repo.delete_stock(stock_id)

        if not delete_stock:
            return {"message": "Problem with Stock Group Update Contact Developer", "status": 500}

        return {"message": f"stock group successfully updated", "status": 200}
