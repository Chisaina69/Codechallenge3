from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey

engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='restaurant')

    def __repr__(self):
        return f'<Restaurant(name={self.name}, price={self.price})>'

    def reviews(self):
        return [f"Review for {self.name} by {review.customer.first_name} {review.customer.last_name}: {review.star_rating} stars." for review in self.reviews]

    def customers(self):
        return [review.customer for review in self.reviews]


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', back_populates='customer')

    def __repr__(self):
        return f'<Customer(name={self.first_name} {self.last_name})>'

    def reviews(self):
        return [f"Review for {review.restaurant.name} by {self.first_name} {self.last_name}: {review.star_rating} stars." for review in self.reviews]

    def restaurants(self):
        return [review.restaurant for review in self.reviews]


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')

    def __repr__(self):
        return f'<Review(restaurant={self.restaurant.name}, customer={self.customer.first_name} {self.customer.last_name}, rating={self.star_rating})>'
