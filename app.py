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

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
            ("Logitech M185 Wireless Mouse", 800.00, 50),
            ("HP Wired Keyboard", 1200.00, 15),
        ]
        conn.executemany(
            "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
            starter_products,
        )
        conn.commit()

    conn.close()


# ---------------------------------------------------------------------------
# Routes (only 4 pages, as required)
# ---------------------------------------------------------------------------
@app.route("/")
def dashboard():
    """Dashboard - summary cards plus a visible list of current products."""
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()

    total_products = len(products)
    total_stock = sum(p["stock"] for p in products)
    total_value = sum(p["price"] * p["stock"] for p in products)

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_stock=total_stock,
        total_value=total_value,
        products=products,
    )


@app.route("/products")
def products():
    """Product List - every product in a simple table."""
    conn = get_db_connection()
    all_products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return render_template("products.html", products=all_products)


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
