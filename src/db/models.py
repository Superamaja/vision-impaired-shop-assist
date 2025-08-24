"""
Database models and management for the Vision-Impaired Shopping Assistant.

This module defines the database schema for storing barcode information
including product names, brands, and allergen information. It uses SQLAlchemy
ORM for database operations and includes comprehensive error handling.
"""

from sqlalchemy import Column, String, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BarcodeExistsError(Exception):
    """Raised when attempting to add a barcode that already exists in the database."""

    pass


class Barcode(Base):
    """
    SQLAlchemy model representing a barcode entry in the database.

    This model stores product information associated with barcodes,
    including allergen information to assist vision-impaired users
    in making informed shopping decisions.

    Attributes:
        barcode (str): Unique barcode identifier (primary key)
        product_name (str): Name of the product
        brand (str): Brand name of the product
        allergies (str): Comma-separated list of allergens, defaults to "none"
    """

    __tablename__ = "barcodes"

    barcode = Column(String, primary_key=True)
    product_name = Column(String)
    brand = Column(String)
    allergies = Column(String, default="none")

    def __repr__(self):
        return f"<Barcode(barcode={self.barcode}, product_name={self.product_name}, brand={self.brand}, allergies={self.allergies})>"


class DatabaseManager:
    """
    Manages database operations for the barcode information system.

    This class provides a high-level interface for all database operations
    including CRUD operations for barcode entries with proper session
    management and error handling.

    Attributes:
        engine: SQLAlchemy database engine
        Session: SQLAlchemy session maker class
    """

    def __init__(self, db_url="sqlite:///database.db"):
        """
        Initialize the database manager with a connection URL.

        Args:
            db_url (str): Database connection URL, defaults to SQLite file
        """
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """
        Initialize the database by creating all tables.

        This method should be called once to set up the database schema.
        """
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Create and return a new database session.

        Returns:
            Session: SQLAlchemy session object
        """
        return self.Session()

    def add_barcode(
        self, barcode: str, product_name: str, brand: str, allergies: str = None
    ) -> dict:
        """
        Add a new barcode entry to the database.

        Args:
            barcode (str): Unique barcode identifier
            product_name (str): Name of the product
            brand (str): Brand name of the product
            allergies (str, optional): Allergen information, defaults to "none"

        Returns:
            dict: Dictionary containing the added barcode information

        Raises:
            BarcodeExistsError: If the barcode already exists in the database
            Exception: For other database-related errors
        """
        session = self.get_session()
        try:
            # If allergies is None or empty, set it to "none"
            if not allergies:
                allergies = "none"

            barcode_entry = Barcode(
                barcode=barcode,
                product_name=product_name,
                brand=brand,
                allergies=allergies,
            )
            session.add(barcode_entry)
            session.commit()
            # Make a detached copy of attributes before closing the session
            result = {
                "barcode": barcode_entry.barcode,
                "product_name": barcode_entry.product_name,
                "brand": barcode_entry.brand,
                "allergies": barcode_entry.allergies,
            }
            return result
        except IntegrityError:
            session.rollback()
            raise BarcodeExistsError(f"Barcode '{barcode}' already exists.")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_barcode(self, barcode: str) -> Barcode:
        """
        Retrieve a barcode entry from the database.

        Args:
            barcode (str): The barcode identifier to search for

        Returns:
            Barcode: The barcode object if found, None otherwise
        """
        session = self.get_session()
        try:
            return session.query(Barcode).filter(Barcode.barcode == barcode).first()
        finally:
            session.close()

    def get_all_barcodes(self) -> list[Barcode]:
        """
        Retrieve all barcode entries from the database.

        Returns:
            list[Barcode]: List of all barcode objects in the database
        """
        session = self.get_session()
        try:
            return session.query(Barcode).all()
        finally:
            session.close()

    def delete_barcode(self, barcode: str) -> bool:
        """
        Delete a barcode entry from the database.

        Args:
            barcode (str): The barcode identifier to delete

        Returns:
            bool: True if the barcode was deleted, False if not found

        Raises:
            Exception: For database-related errors during deletion
        """
        session = self.get_session()
        try:
            result = session.query(Barcode).filter(Barcode.barcode == barcode).delete()
            session.commit()
            return result > 0
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
