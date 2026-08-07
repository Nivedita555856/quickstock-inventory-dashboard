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
├── app.py                 # Flask app: routes + SQLite setup
├── requirements.txt       # Python dependencies
├── templates/             # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── products.html
│   ├── add_product.html
│   └── about.html
├── static/
│   └── css/
│       └── style.css      # Custom styling on top of Bootstrap 5
├── tests/
│   └── test_app.py        # pytest test cases
├── README.md
└── .gitignore
```

`quickstock.db` is created automatically the first time the app runs — it is
not committed to Git (see `.gitignore`).

---

## Pages

1. **Dashboard** – summary cards (total products, total stock, inventory value) plus visible product cards for the current inventory
2. **Product List** – table of all products (name, price, stock)
3. **Add Product** – a simple form that inserts a new product
4. **About** – static info page with app name and version

## Starter Data

On first run, the database is seeded with three products:

| Product | Price | Stock |
|---|---|---|
| Dell Inspiron 15 Laptop | ₹55,000 | 20 |
| Logitech M185 Wireless Mouse | ₹800 | 50 |
| HP Wired Keyboard | ₹1,200 | 15 |

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

- No authentication or user roles
- No JWT or sessions
- No REST API layer
- No frontend framework (React/Angular/Vue)
- No Jenkinsfile, Docker, or deployment config

These are left out on purpose so the focus stays on the CI/CD pipeline
mechanics rather than application complexity. They can be added in a later
phase once the Jenkins pipeline itself is working end-to-end.
