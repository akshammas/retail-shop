"""add performance indexes

Revision ID: f30cf1eb1a1c
Revises: 2f2bab7429ac
Create Date: 2026-06-11 17:23:00.000000

"""
from typing import Union, Sequence
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f30cf1eb1a1c'
down_revision: Union[str, Sequence[str], None] = '2f2bab7429ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_orders_user_id', 'orders', ['user_id'])
    op.create_index('ix_orders_status', 'orders', ['status'])
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'])
    op.create_index('ix_cart_items_user_id', 'cart_items', ['user_id'])
    op.create_index('ix_addresses_user_id', 'addresses', ['user_id'])
    op.create_index('ix_product_images_product_id', 'product_images', ['product_id'])
    op.create_index('ix_products_in_stock', 'products', ['in_stock'])
    op.create_index('ix_products_category_stock', 'products', ['category_id', 'in_stock'])


def downgrade() -> None:
    op.drop_index('ix_orders_user_id', table_name='orders')
    op.drop_index('ix_orders_status', table_name='orders')
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_order_items_product_id', table_name='order_items')
    op.drop_index('ix_cart_items_user_id', table_name='cart_items')
    op.drop_index('ix_addresses_user_id', table_name='addresses')
    op.drop_index('ix_product_images_product_id', table_name='product_images')
    op.drop_index('ix_products_in_stock', table_name='products')
    op.drop_index('ix_products_category_stock', table_name='products')