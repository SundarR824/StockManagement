"""
This File only contains models for
database table for connection engines.
"""

from pathlib import Path
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

Base = declarative_base()
db_path = f"sqlite:///{Path(Path.cwd())}/DBModels/stocks.db"
# db_path = "sqlite:////home/sundar/Desktop/StockManagement/StocksApplication/DBModels/stocks.db"
engine = create_engine(db_path, echo=False)

class StockGroup(Base):
    __tablename__ = 'stock_group'

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    description = Column(String)

    # Relationship with Stocks
    stocks = relationship("Stocks", back_populates="stock_group")

    def __repr__(self):
        return f"<StockGroup(id='{self.id}', name='{self.group_name}', description='{self.description}')>"


class Stocks(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    stock_name = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    minimum_count = Column(Integer, nullable=False)
    description = Column(String)

    # Foreign key to StockGroup
    stock_group_id = Column(Integer, ForeignKey('stock_group.id'))

    # Relationship with StockGroup
    stock_group = relationship("StockGroup", back_populates="stocks")

    def __repr__(self):
        return f"<Stocks(id='{self.id}', name='{self.stock_name}', description='{self.description}')>"


if __name__ == '__main__':
    Base.metadata.create_all(engine)
