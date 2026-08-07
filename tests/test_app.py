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
    """Product list should include the three starter products."""
    response = client.get("/products")
    assert response.status_code == 200
    assert b"Laptop" in response.data
    assert b"Mouse" in response.data
    assert b"Keyboard" in response.data


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
