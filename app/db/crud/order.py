# app/db/crud/order.py

from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product


def create_order(db: Session, user_id: int, shipping_address: str, items: list):
    """Create an order with items"""

    total = 0.0
    order_items = []

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            return None, f"Product {item.product_id} not found"
        if product.quantity < item.quantity:
            return None, f"Not enough stock for {product.name}"

        # snapshot price at time of purchase
        item_total = product.price * item.quantity
        total += item_total

        order_items.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })

        # reduce stock
        product.quantity -= item.quantity
        if product.quantity == 0:
            product.in_stock = False

    # create order
    new_order = Order(
        user_id=user_id,
        shipping_address=shipping_address,
        total_amount=round(total, 2)
    )
    db.add(new_order)
    db.flush()  # get order id without committing

    # create order items
    for item_data in order_items:
        order_item = OrderItem(order_id=new_order.id, **item_data)
        db.add(order_item)

    db.commit()
    db.refresh(new_order)
    return new_order, None


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_all_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: str):
    order = get_order_by_id(db, order_id)
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order