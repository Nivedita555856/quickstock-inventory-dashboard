"""
Basic pytest test cases for QuickStock.

These are intentionally simple so a Jenkins "Test" stage can run them
(`pytest`) with no extra setup, and so a broken UI/backend change fails
the pipeline before it ever reaches deploy.
"""

import os
import sys

# Make the project root importable when pytest is run from the tests/ folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as test_client:
        yield test_client


def test_dashboard_loads(client):
    """Dashboard page should load and show the app name."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"QuickStock" in response.data


def test_products_page_shows_seed_data(client):
    """Product list should include the full 20-item starter catalog."""
    response = client.get("/products")
    assert response.status_code == 200
    assert b"Laptop" in response.data
    assert b"Mouse" in response.data
    assert b"Keyboard" in response.data
    assert response.data.count(b"Add to Cart") == 20


def test_dashboard_shows_limited_featured_products(client):
    """Dashboard should preview a handful of products, not the full catalog."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Featured Products" in response.data
    assert b"View All Products" in response.data


def test_add_product_page_loads(client):
    """Add Product form page should load with its form fields."""
    response = client.get("/add-product")
    assert response.status_code == 200
    assert b"Add New Product" in response.data


def test_about_page_loads(client):
    """About page should load and show the version badge."""
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Version 1.0" in response.data


def test_product_detail_page_loads(client):
    """Clicking into product 1 should show its detail page."""
    response = client.get("/product/1")
    assert response.status_code == 200
    assert b"Product Details" in response.data


def test_product_detail_invalid_id_redirects(client):
    """Requesting a product that doesn't exist should redirect to the list."""
    response = client.get("/product/9999", follow_redirects=False)
    assert response.status_code == 302


def test_add_to_cart_and_view_cart(client):
    """Adding a product should make it show up on the cart page with a total."""
    client.post("/cart/add/1", follow_redirects=True)
    response = client.get("/cart")
    assert response.status_code == 200
    assert b"Dell Inspiron 15 Laptop" in response.data


def test_checkout_completes_and_clears_cart(client):
    """Paying at checkout should clear the cart and show the confirmation page."""
    client.post("/cart/add/2", follow_redirects=True)
    response = client.post("/checkout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Order Placed Successfully" in response.data

    cart_response = client.get("/cart")
    assert b"Your cart is empty" in cart_response.data
