"""
QuickStock - Inventory Management Dashboard
--------------------------------------------
A deliberately simple Flask application used to teach CI/CD concepts with
Jenkins. The business logic is kept minimal on purpose - the point of this
project is the pipeline (Git -> GitHub -> Jenkins -> Build -> Test -> Deploy),
not the app itself.

Run locally with:
    pip install -r requirements.txt
    python app.py
"""

import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# A session secret key is required so Flask can store the shopping cart
# in a signed cookie. Fine for this teaching demo; a real app would load
# this from an environment variable instead of hardcoding it.
app.secret_key = "quickstock-dev-secret-key"

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "quickstock.db")


def get_db_connection():
    """Open a new SQLite connection. Rows behave like dictionaries."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the products table and seed it with starter data (once)."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """
    )
    conn.commit()

    # Only seed if the table is empty, so restarting the app never
    # duplicates the starter products.
    row_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if row_count == 0:
        starter_products = [
            ("Dell Inspiron 15 Laptop", 55000.00, 20),
            ("HP Pavilion 14 Laptop", 48000.00, 15),
            ("Lenovo ThinkPad E14 Laptop", 62000.00, 10),
            ("Logitech M185 Wireless Mouse", 800.00, 50),
            ("Dell Wired Optical Mouse", 450.00, 60),
            ("HP Wired Keyboard", 1200.00, 15),
            ("Logitech K380 Wireless Keyboard", 2500.00, 25),
            ("Dell 24-inch Full HD Monitor", 9500.00, 12),
            ("Samsung 27-inch LED Monitor", 15500.00, 8),
            ("Logitech C270 Webcam", 2200.00, 30),
            ("boAt Rockerz Wireless Headphones", 1800.00, 40),
            ("JBL Tune 500 Headphones", 2100.00, 22),
            ("HP DeskJet Printer", 6500.00, 10),
            ("Canon PIXMA Printer", 7200.00, 7),
            ("TP-Link Wi-Fi Router", 1800.00, 35),
            ("D-Link Wireless Router", 1600.00, 28),
            ("SanDisk 32GB Pendrive", 450.00, 100),
            ("Seagate 1TB External Hard Drive", 4200.00, 18),
            ("Anker Power Bank 10000mAh", 1500.00, 45),
            ("Logitech Z120 Speakers", 900.00, 33),
        ]
        conn.executemany(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            starter_products,
        )
        conn.commit()

    conn.close()


def get_cart_items():
    """Look up full product details for everything currently in the cart.

    The cart itself just lives in the session as {product_id: quantity} -
    this turns that into a list the templates can render, plus a grand total.
    """
    cart = session.get("cart", {})
    items = []
    grand_total = 0.0

    if cart:
        conn = get_db_connection()
        for product_id_str, quantity in cart.items():
            product = conn.execute(
                "SELECT * FROM products WHERE id = ?", (int(product_id_str),)
            ).fetchone()
            if product:
                subtotal = product["price"] * quantity
                grand_total += subtotal
                items.append(
                    {
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": quantity,
                        "subtotal": subtotal,
                    }
                )
        conn.close()

    return items, grand_total


@app.context_processor
def inject_cart_count():
    """Make the cart item count available to every template (for the navbar badge)."""
    cart = session.get("cart", {})
    return dict(cart_item_count=sum(cart.values()))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def dashboard():
    """Dashboard - summary cards plus a preview of a few featured products.

    With a full 20-item catalog, showing every product here would be
    cluttered - the Dashboard shows a handful as a preview and links to
    the Product List page, which is the real "browse everything" page.
    """
    conn = get_db_connection()
    all_products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()

    total_products = len(all_products)
    total_stock = sum(p["stock"] for p in all_products)
    total_value = sum(p["price"] * p["stock"] for p in all_products)
    featured_products = all_products[:6]

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stock=total_stock,
        total_value=total_value,
        products=featured_products,
    )


@app.route("/products")
def products():
    """Product List - every product in a simple table."""
    conn = get_db_connection()
    all_products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return render_template("products.html", products=all_products)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    """Product Detail - click into a single product to see its full info."""
    conn = get_db_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    conn.close()

    if product is None:
        return redirect(url_for("products"))

    return render_template("product_detail.html", product=product)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Add one unit of a product to the cart (stored in the session)."""
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart

    flash("Added to cart.", "success")
    return redirect(request.referrer or url_for("products"))


@app.route("/cart")
def view_cart():
    """Cart - everything the shopper has added so far, with a running total."""
    items, grand_total = get_cart_items()
    return render_template("cart.html", items=items, grand_total=grand_total)


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    """Remove a product entirely from the cart."""
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart

    flash("Item removed from cart.", "info")
    return redirect(url_for("view_cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Checkout - review the order, then simulate a payment.

    There's no real payment gateway here - "Pay & Place Order" simply
    clears the cart and shows a confirmation page, which is enough to
    demonstrate the full browse -> cart -> checkout flow.
    """
    items, grand_total = get_cart_items()

    if request.method == "POST":
        session["cart"] = {}
        return redirect(url_for("order_confirmation"))

    if not items:
        return redirect(url_for("view_cart"))

    return render_template("checkout.html", items=items, grand_total=grand_total)


@app.route("/order-confirmation")
def order_confirmation():
    """Order Confirmation - shown after a (simulated) successful payment."""
    return render_template("order_confirmation.html")


@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    """Add Product - a small form that inserts one row into SQLite."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        price = request.form.get("price", "0")
        stock = request.form.get("stock", "0")

        if name:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                (name, float(price), int(stock)),
            )
            conn.commit()
            conn.close()

        return redirect(url_for("products"))

    return render_template("add_product.html")


@app.route("/about")
def about():
    """About - static information page about the app."""
    return render_template("about.html")


# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------
# Initialized at import time so both `python app.py` and pytest (which
# imports this module) always have a ready database to work with.
init_db()

if __name__ == "__main__":
    app.run(debug=True)
