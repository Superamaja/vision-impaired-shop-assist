from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Barcode(Base):
    __tablename__ = "barcodes"

    barcode = Column(String, primary_key=True)
    product_name = Column(String)
    brand = Column(String)

    def __repr__(self):
        return f"<Barcode(barcode={self.barcode}, product_name={self.product_name}, brand={self.brand})>"


# Create a new database
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)

# Create the table
Base.metadata.create_all(engine)
