"""
This file leverages the connection from the engine to execute
queries for CRUD (Create, Read, Update, Delete) operations,
serving as the data access layer for the application
"""
import sqlite3
import sys, os
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DBModels.DBModels import StockGroup, Stocks, engine

class StockGroupRepository:
    def __init__(self):
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()

    def fetch_stock_group_by_name(self, name: str):
        stock_group = self.session.query(StockGroup).filter(func.lower(StockGroup.group_name) == name.lower()).first()
        self.session.close()
        return stock_group

    def fetch_all_stock_group(self) -> list:
        stock_groups = self.session.query(StockGroup).all()
        self.session.close()
        return stock_groups

    def create_stock_group(self, group_name: str, group_desc: str = "") -> bool:
        try:
            stock_group = StockGroup(group_name=group_name.lower(), description=group_desc)
            self.session.add(stock_group)
            self.session.commit()
            return True
        except sqlite3.IntegrityError as err:
            print(f"Integrity error: {err}")
        except Exception as err:
            print(f"Error: {err}")
        finally:
            self.session.rollback()
            self.session.close()
        return False

    def update_stock_group(self, group_id: int, attr: dict) -> bool:
        stock_group = self.session.query(StockGroup).filter_by(id=group_id).first()
        if not stock_group:
            return False
        stock_group.group_name = attr['name'].lower()
        stock_group.description = attr['desc']
        self.session.commit()
        self.session.close()
        return True

    def delete_stock_group(self, group_id: int) -> bool:
        stock_group = self.session.query(StockGroup).filter_by(id=group_id).first()
        if not stock_group:
            return False
        self.session.delete(stock_group)
        self.session.commit()
        self.session.close()
        return True


class StockRepository:
    def __init__(self):
        session_cls = sessionmaker(bind=engine)
        self.session = session_cls()

    def fetch_all_stocks(self, group_id: int = 0) -> list:
        if group_id != 0:
            stock_list = self.session.query(Stocks).filter_by(stock_group_id=group_id).all()
        else:
            stock_list = self.session.query(Stocks).all()
        self.session.close()
        return stock_list

    def create_stock(self, **kwargs) -> bool:
        try:
            stock_group = Stocks(
                stock_name=kwargs['stock_name'].lower(), description=kwargs['stock_desc'],
                stock_group_id=int(kwargs['group_id']), count=int(kwargs['count']),
                minimum_count=int(kwargs['mini_count'])
            )
            self.session.add(stock_group)
            self.session.commit()
            self.session.close()
            return True
        except Exception as err:
            print(err)
            return False

    def update_stock(self, stock_id: int, attr: dict) -> bool:
        stock = self.session.query(Stocks).filter_by(id=stock_id).first()
        if not stock:
            return False
        stock.stock_name = attr['name'].lower()
        stock.description = attr['desc']
        stock.count = int(attr['count'])
        stock.minimum_count = int(attr['mini_count'])
        stock.stock_group_id = int(attr['group_id'])
        self.session.commit()
        self.session.close()
        return True

    def delete_stock(self, stock_id) -> bool:
        stock = self.session.query(Stocks).filter_by(id=stock_id).first()
        if not stock:
            return False
        self.session.delete(stock)
        self.session.commit()
        self.session.close()
        return True
