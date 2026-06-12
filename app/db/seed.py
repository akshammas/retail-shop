# app/db/seed.py

import random
import time
from faker import Faker
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models import User, Product, Order, OrderItem, CartItem, Category, Address
from app.core.security import hash_password

fake = Faker("en_IN")  # Indian locale for realistic data
Faker.seed(42)  # reproducible results


def seed_categories(db: Session):
    print("Seeding categories...")
    categories = [
        Category(name="clothing", description="All clothing items"),
        Category(name="footwear", description="Shoes and sandals"),
        Category(name="accessories", description="Bags, belts, and more"),
        Category(name="outerwear", description="Jackets and coats"),
        Category(name="sportswear", description="Sports and gym wear"),
        Category(name="ethnic", description="Traditional Indian wear"),
        Category(name="formal", description="Office and formal wear"),
        Category(name="casual", description="Everyday casual wear"),
    ]
    # only add if not already there
    existing = db.query(Category).count()
    if existing == 0:
        db.add_all(categories)
        db.commit()
        print(f"✅ {len(categories)} categories seeded")
    else:
        print(f"Categories already exist — skipping")
    return db.query(Category).all()


def seed_users(db: Session, count: int = 10000):
    print(f"Seeding {count} users...")
    start = time.time()

    hashed = hash_password("password123")

    # get all existing emails from db to avoid duplicates
    existing_emails = set(
        email for (email,) in db.query(User.email).all()
    )
    print(f"  → {len(existing_emails)} existing emails found")

    users = []
    inserted = 0

    while inserted < count:
        email = fake.unique.email()

        # skip if already in db
        if email in existing_emails:
            continue

        existing_emails.add(email)
        users.append(User(
            name=fake.name(),
            email=email,
            password=hashed,
            role="customer",
            is_active=True,
            phone_number=fake.phone_number()[:15]
        ))
        inserted += 1

        # batch insert every 500
        if len(users) % 500 == 0:
            db.bulk_save_objects(users)
            db.commit()
            users = []
            print(f"  → {inserted} users inserted...")

    # insert remaining
    if users:
        db.bulk_save_objects(users)
        db.commit()

    total = time.time() - start
    print(f"✅ {count} users seeded in {total:.1f}s")

def seed_products(db: Session, categories: list, count: int = 50000):
    existing = db.query(Product).count()
    if existing >= count:
        print(f"Products already seeded ({existing} rows) — skipping")
        return

    print(f"Seeding {count} products...")
    start = time.time()

    category_ids = [c.id for c in categories]
    products = []

    for i in range(count):
        products.append(Product(
            name=f"{fake.word().capitalize()} {random.choice(['Shirt', 'Pant', 'Jacket', 'Shoes', 'Bag', 'Cap', 'Kurta', 'Saree'])}",
            price=round(random.uniform(99, 9999), 2),
            description=fake.sentence(),
            in_stock=random.choice([True, True, True, False]),  # 75% in stock
            quantity=random.randint(0, 200),
            category_id=random.choice(category_ids)
        ))

        if len(products) % 1000 == 0:
            db.bulk_save_objects(products)
            db.commit()
            products = []
            print(f"  → {i+1} products inserted...")

    if products:
        db.bulk_save_objects(products)
        db.commit()

    total = time.time() - start
    print(f"✅ {count} products seeded in {total:.1f}s")


def seed_orders(db: Session, count: int = 100000):
    existing = db.query(Order).count()
    if existing >= count:
        print(f"Orders already seeded ({existing} rows) — skipping")
        return

    print(f"Seeding {count} orders...")
    start = time.time()

    # get all user and product ids
    user_ids = [u.id for u in db.query(User.id).all()]
    product_ids = [p.id for p in db.query(Product.id).all()]

    if not user_ids or not product_ids:
        print("❌ No users or products found — skipping orders")
        return

    statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    orders = []
    order_items = []

    for i in range(count):
        user_id = random.choice(user_ids)
        num_items = random.randint(1, 4)
        total = 0.0

        order = Order(
            user_id=user_id,
            status=random.choice(statuses),
            shipping_address=fake.address().replace("\n", ", "),
            total_amount=0.0  # will update below
        )
        orders.append(order)

        # batch insert orders every 1000
        if len(orders) % 1000 == 0:
            db.bulk_save_objects(orders)
            db.flush()
            orders = []
            print(f"  → {i+1} orders inserted...")

    # commit remaining orders
    if orders:
        db.bulk_save_objects(orders)
    db.commit()

    total_time = time.time() - start
    print(f"✅ {count} orders seeded in {total_time:.1f}s")


def run_seed():
    db = SessionLocal()
    try:
        print("\n🌱 Starting database seed...\n")
        start = time.time()

        categories = seed_categories(db)
        seed_users(db, count=10000)
        seed_products(db, categories, count=50000)
        seed_orders(db, count=100000)

        total = time.time() - start
        print(f"\n✅ Seed complete in {total:.1f}s")
        print(f"   Users:    {db.query(User).count():,}")
        print(f"   Products: {db.query(Product).count():,}")
        print(f"   Orders:   {db.query(Order).count():,}")

    except Exception as e:
        print(f"❌ Seed failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()