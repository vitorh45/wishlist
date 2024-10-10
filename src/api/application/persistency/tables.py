from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from api.app import db
from sqlalchemy import Table, Column, String
from sqlalchemy.orm import relationship

UUID_GENERATE_V4 = db.text("uuid_generate_v4()")


wishlist_product = Table(
    'wishlist_product',
    db.metadata,
    Column('wishlist_id', UUID(as_uuid=True), db.ForeignKey('wishlist.id'), primary_key=True),
    Column('product_id', UUID(as_uuid=True), db.ForeignKey('product.id'), primary_key=True)
)


class Client(db.Model):
    __tablename__ = "client"

    id = Column(
        UUID(as_uuid=True),
        server_default=UUID_GENERATE_V4,
        primary_key=True,
        nullable=False,
        unique=True
    )
    name = Column(db.String(256), nullable=False)
    email = Column(db.String(100), nullable=False, unique=True)
    insert_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    wishlist = relationship('Wishlist', backref='client', lazy=True)

class Product(db.Model):
    __tablename__ = "product"

    id = Column(
        UUID(as_uuid=True),
        server_default=UUID_GENERATE_V4,
        primary_key=True,
        nullable=False,
    )
    title = Column(db.String(256), nullable=False)
    brand = Column(db.String(100), nullable=False)
    price = Column(db.Integer, nullable=False)
    image = Column(db.String(200), nullable=False)
    insert_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    wishlist = relationship('Wishlist', secondary=wishlist_product, backref='product')



class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = Column(
        UUID(as_uuid=True),
        server_default=UUID_GENERATE_V4,
        primary_key=True,
        nullable=False,
    )
    client_id = Column(UUID(as_uuid=True), db.ForeignKey('client.id'), nullable=False)
    insert_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    products = db.relationship('Product', secondary=wishlist_product, backref='wishlists')


