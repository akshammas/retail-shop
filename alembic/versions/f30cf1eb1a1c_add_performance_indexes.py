# alembic/versions/xxxx_add_performance_indexes.py

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # orders — fast lookup by user
    op.create_index('ix_orders_user_id', 'orders', ['user_id'])

    # orders — fast filter by status
    op.create_index('ix_orders_status', 'orders', ['status'])

    # order_items — fast lookup by order
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])

    # order_items — fast lookup by product
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'])

    # cart_items — fast lookup by user
    op.create_index('ix_cart_items_user_id', 'cart_items', ['user_id'])

    # addresses — fast lookup by user
    op.create_index('ix_addresses_user_id', 'addresses', ['user_id'])

    # product_images — fast lookup by product
    op.create_index('ix_product_images_product_id', 'product_images', ['product_id'])

    # products — fast filter by in_stock
    op.create_index('ix_products_in_stock', 'products', ['in_stock'])

    # composite index — category + in_stock filter together
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