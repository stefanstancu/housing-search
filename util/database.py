from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from util.helper import get_db_url

Base = declarative_base()


class DBListing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    price = Column(Float)
    address = Column(Float)
    commute = Column(Float)
    viability = Column(Float)


class Database:
    def __init__(self):
        # Connect to the db
        db_url = get_db_url('credentials/db_credentials.json')
        engine = create_engine(db_url)
        session = sessionmaker()
        session.configure(bind=engine)
        self.s = session()

    def listing_exists(self, listing):
        """
            Checks for the link of the listing
        Args:
            listing: (Listing) A listing object

        Returns:
            bool: whether or not it exists

        """
        exists = self.s.query(DBListing.id).filter(DBListing.url == listing.url).count()
        return bool(exists)

    def save_listing(self, listing, u_of_t_address):
        """
            Writes the listing to the database
        Args:
            u_of_t_address: The destination address
            listing: (Listing) A listing object

        Returns:
            None

        """
        db_listing = DBListing(
            title=listing.get_title(),
            url=listing.url,
            price=listing.get_cost(),
            address=listing.get_address(),
            commute=listing.get_commute_time(u_of_t_address),
            viability=listing.get_viability(u_of_t_address)
        )
        self.s.add(db_listing)
        self.s.commit()
