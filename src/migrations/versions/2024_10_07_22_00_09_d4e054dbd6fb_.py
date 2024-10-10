"""empty message

Revision ID: 9cbb83af6a14
Revises: f95bdbdc9a3f
Create Date: 2024-10-07 14:26:13.776465

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'd4e054dbd6fb'
down_revision = '294079b5e1fe'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        sa.table('product',
                 sa.column('brand'),
                 sa.column('title'),
                 sa.column('price'),
                 sa.column('image'),
                 sa.column('update_at'),
                 sa.column('insert_at')),
        [
            {
                "brand": "Gibson",
                "title": "Les Paul 69 cherry sunburst",
                "price": 1500000,
                "image": "products/list/gibson_01.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Gibson",
                "title": "Les Paul 67 goldtop",
                "price": 1700000,
                "image": "products/list/gibson_02.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Gibson",
                "title": "Les Paul 69 lemon drop",
                "price": 2500000,
                "image": "products/list/gibson_03.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Gibson",
                "title": "Les Paul 69 jow perry",
                "price": 3500000,
                "image": "products/list/gibson_04.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Marshall",
                "title": "JCM 800",
                "price": 1500000,
                "image": "products/list/marshall_01.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Marshall",
                "title": "Jubilee",
                "price": 1600000,
                "image": "products/list/marshall_02.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Marshall",
                "title": "AFD 100",
                "price": 1800000,
                "image": "products/list/marshall_03.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "EMB",
                "title": "Rack wah",
                "price": 2500000,
                "image": "products/list/emb_01.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Dunlop",
                "title": "Crybaby Slash",
                "price": 500000,
                "image": "products/list/pedal_01.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            },
            {
                "brand": "Marshall",
                "title": "Gabinete 4x12",
                "price": 1000000,
                "image": "products/list/marshall_04.jpg",
                'update_at': datetime.utcnow(),
                'insert_at': datetime.utcnow()
            }
        ]
    )


def downgrade():
    pass
