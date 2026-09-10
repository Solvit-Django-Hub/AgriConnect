# AgriConnect

**A Direct Farmer-to-Buyer Produce Marketplace**
Built with Django & PostgreSQL — Machine Learning phase planned next.

---

## About the Project

AgriConnect is a backend-driven marketplace platform that connects smallholder
farmers directly to buyers, removing the middlemen who traditionally control
pricing, timing, and market information in the produce supply chain. Farmers
list their own produce at their own prices; buyers browse, filter, and order
directly from the source.

Every transaction — listing, order, and price — is captured cleanly in the
database, building the dataset a future **Phase 2 Machine Learning** layer
(price prediction, demand forecasting, recommendations) will train on.

The platform is also being designed with **USSD access in mind**, so farmers
and buyers without smartphones can still list produce and place orders using
a basic phone.

## Core Features

- Role-based accounts for **farmers** and **buyers** on a single login system
- Farmers can create, update, and remove produce listings (full CRUD)
- Buyers can search, filter, and order one or more products at once
- Orders are tracked through a status lifecycle: `placed` → `confirmed` → `delivered`
- Referential integrity enforced end-to-end via foreign keys and
  `ON DELETE CASCADE`
- Designed for future USSD-based access for users without smartphones

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Django |
| Database | PostgreSQL (SQLite for local development) |
| Auth | Custom Django `User` model, role-based (`farmer` / `buyer`) |
| Planned | Django REST Framework (API layer), Machine Learning phase |

## Project Structure


agriconnect/
├── agriconnect/          # project settings, root urls
├── accounts/              # custom User model (role, phone_number)
├── farmers/                # Farmer profile + Product model
├── buyers/                # Buyer profile
├── orders/                # Category, Order, OrderItem
├── manage.py
├── requirements.txt
└── .gitignore
```

## Data Model Overview

| App | Models |
|---|---|
| `accounts` | `User` — role (farmer/buyer), phone_number (login key for USSD + web) |
| `farmers` | `Farmer` (profile), `Product` |
| `buyers` | `Buyer` (profile) |
| `orders` | `Category`, `Order`, `OrderItem` |

**Key relationships**
- A farmer creates many products (`Product.farmer` → `User`)
- A category groups many products (`Product.category` → `Category`)
- A buyer places many orders (`Order.buyer` → `User`)
- An order bundles many products through `OrderItem`, which also stores
  `quantity` and `price_at_order` (price is locked in at order time, even if
  the listing price changes later)

## Getting Started

### Prerequisites
- Python 3.10+
- pip
- PostgreSQL (only required for production/staging — local dev can use SQLite)
- Git

### 1. Clone the repository

git clone https://github.com/Solvit-Django-Hub/AgriConnect
cd agriconnect


### 2. Create and activate a virtual environment

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Configure environment variables
Create a `.env` file in the project root (never commit this file):

SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

For production/staging with PostgreSQL, replace `DATABASE_URL` with:

DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME


### 5. Apply migrations

python manage.py makemigrations
python manage.py migrate


### 6. Create a superuser (for Django admin access)

python manage.py createsuperuser


### 7. Run the development server

python manage.py runserver

Visit `http://127.0.0.1:8000/admin/` to access the Django admin panel.

## Dependencies

See `requirements.txt` for the exact pinned versions. Core packages expected
in this project:
- `django`
- `djangorestframework` (API layer)
- `psycopg2-binary` (PostgreSQL driver)
- `python-decouple` or `django-environ` (environment variable management)

> If `requirements.txt` isn't committed yet, generate it from your active
> virtual environment with:
> 
> pip freeze > requirements.txt
> 

## Branching & Workflow

Branches follow the pattern `type/TICKET-KEY-short-description`, e.g.
`feature/AGRI-3-product-model`. Each feature is developed on its own branch
and merged into `main` via pull request.

## Project Status

**In active development.** Core models (`accounts`, `farmers`, `buyers`,
`orders`) are in place. Authentication, views/API, and USSD integration are
in progress.

## Roadmap — Phase 2

- Price prediction from historical order data
- Demand forecasting by crop and season
- Personalized produce recommendations for buyers
- Best-time-to-sell alerts for farmers
- Anomaly detection for fraudulent listings

## License

To be determined.