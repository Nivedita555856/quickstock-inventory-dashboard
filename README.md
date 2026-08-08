# QuickStock – Inventory Management Dashboard

QuickStock is a deliberately simple inventory dashboard built to teach
**CI/CD concepts using Jenkins**. The application itself is intentionally
minimal — the point of this project is not the app, it's the pipeline that
builds, tests, and redeploys it every time the code changes.

This repository is application-only. Jenkins, Docker, and deployment are
**not** part of this project yet — they get layered on top in a later step.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Bootstrap 5, Jinja2 templates |
| Backend | Python 3.12+, Flask |
| Database | SQLite |
| Testing | pytest |
| Package management | pip, requirements.txt |
| Version control | Git, GitHub |

---

## Project Structure

```text
QuickStock/
├── app.py                     # Flask app: routes + SQLite setup + cart logic
├── requirements.txt           # Python dependencies
├── templates/                 # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── products.html
│   ├── product_detail.html
│   ├── add_product.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   └── about.html
├── static/
│   └── css/
│       └── style.css          # Custom styling on top of Bootstrap 5
├── tests/
│   └── test_app.py            # pytest test cases
├── README.md
└── .gitignore
```

`quickstock.db` is created automatically the first time the app runs — it is
not committed to Git (see `.gitignore`).

---

## Pages

1. **Dashboard** – summary cards (total products, total stock, inventory value) plus a "Featured Products" preview
2. **Product List** – the full catalog, with an "Add to Cart" button on every product
3. **Product Detail** – click any product to see its full info and add it to the cart
4. **Cart** – everything added so far, with quantities, a running total, and a way to remove items
5. **Checkout** – order summary plus a "Pay & Place Order" button (simulated — no real payment gateway)
6. **Order Confirmation** – shown after checkout; the cart is cleared
7. **Add Product** – a simple form that inserts a new product
8. **About** – static info page with app name and version

## Starter Data

On first run, the database is seeded with a 20-item catalog:

| # | Product | Price | Stock |
|---|---|---|---|
| 1 | Dell Inspiron 15 Laptop | ₹55,000 | 20 |
| 2 | HP Pavilion 14 Laptop | ₹48,000 | 15 |
| 3 | Lenovo ThinkPad E14 Laptop | ₹62,000 | 10 |
| 4 | Logitech M185 Wireless Mouse | ₹800 | 50 |
| 5 | Dell Wired Optical Mouse | ₹450 | 60 |
| 6 | HP Wired Keyboard | ₹1,200 | 15 |
| 7 | Logitech K380 Wireless Keyboard | ₹2,500 | 25 |
| 8 | Dell 24-inch Full HD Monitor | ₹9,500 | 12 |
| 9 | Samsung 27-inch LED Monitor | ₹15,500 | 8 |
| 10 | Logitech C270 Webcam | ₹2,200 | 30 |
| 11 | boAt Rockerz Wireless Headphones | ₹1,800 | 40 |
| 12 | JBL Tune 500 Headphones | ₹2,100 | 22 |
| 13 | HP DeskJet Printer | ₹6,500 | 10 |
| 14 | Canon PIXMA Printer | ₹7,200 | 7 |
| 15 | TP-Link Wi-Fi Router | ₹1,800 | 35 |
| 16 | D-Link Wireless Router | ₹1,600 | 28 |
| 17 | SanDisk 32GB Pendrive | ₹450 | 100 |
| 18 | Seagate 1TB External Hard Drive | ₹4,200 | 18 |
| 19 | Anker Power Bank 10000mAh | ₹1,500 | 45 |
| 20 | Logitech Z120 Speakers | ₹900 | 33 |

The Dashboard only previews the first 6 as "Featured Products" to keep it
readable — the Product List page shows all 20.

---

## Running Locally

```bash
# 1. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

The app runs at **http://127.0.0.1:5000** by default.

---

## Running Tests

```bash
pytest
```

This runs the test cases in `tests/test_app.py`, which check that all four
pages load correctly and that the starter products appear in the product
list. These are the same tests a Jenkins "Test" stage will run later.

---

## Designed for CI/CD Demos

This project is structured so that small, single-file UI changes are easy to
make and easy to show flowing through a pipeline later (Git → GitHub →
Jenkins → Build → Test → Deploy). Examples of changes that only touch one or
two files:

1. Add one more product card — edit `templates/dashboard.html`
2. Change the dashboard title — edit `templates/dashboard.html`
3. Add a Category column — edit `templates/products.html` (and `app.py` if
   you also want to store it)
4. Rename the "Add Product" button — edit `templates/add_product.html`
5. Change the Bootstrap button color — edit `static/css/style.css`
6. Add a new dashboard stat card — edit `templates/dashboard.html`

Each of these is small enough to make live during a training session, push
to GitHub, and watch flow through the pipeline once Jenkins is wired up.

---

## What's Intentionally Left Out (for now)

- No authentication or user accounts (the cart uses Flask's session purely
  to remember what one visitor added — there's no login or JWT)
- No REST API layer
- No real payment gateway (checkout simulates a successful payment)
- No frontend framework (React/Angular/Vue)
- No Jenkinsfile, Docker, or deployment config

These are left out on purpose so the focus stays on the CI/CD pipeline
mechanics rather than application complexity. They can be added in a later
phase once the Jenkins pipeline itself is working end-to-end.
