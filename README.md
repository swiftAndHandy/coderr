# Coderr Backend

REST API backend for the Coderr freelance marketplace platform, built with Django and Django REST Framework.

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.17
- SQLite (development)

## Features

- Token-based authentication (registration & login)
- Business and customer user profiles
- Offer management with basic/standard/premium tiers
- Order system with status tracking
- Review system with rating validation
- Platform statistics endpoint

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/swiftAndHandy/coderr.git
cd backend
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## Authentication

This API uses Token Authentication. After login or registration, include the token in the `Authorization` header of all subsequent requests:

```
Authorization: Token <your_token_here>
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/login/` | Login and receive token | No |

### Profiles

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/profile/{pk}/` | Retrieve a user profile | Yes |
| PATCH | `/api/profile/{pk}/` | Update own profile | Yes (owner only) |
| GET | `/api/profiles/business/` | List all business profiles | Yes |
| GET | `/api/profiles/customer/` | List all customer profiles | Yes |

### Offers

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/offers/` | List all offers (paginated) | No |
| POST | `/api/offers/` | Create an offer | Yes (business only) |
| GET | `/api/offers/{id}/` | Retrieve an offer | Yes |
| PATCH | `/api/offers/{id}/` | Update an offer | Yes (owner only) |
| DELETE | `/api/offers/{id}/` | Delete an offer | Yes (owner only) |
| GET | `/api/offerdetails/{id}/` | Retrieve offer detail | Yes |

### Orders

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List own orders | Yes |
| POST | `/api/orders/` | Create an order | Yes (customer only) |
| PATCH | `/api/orders/{id}/` | Update order status | Yes (business only) |
| DELETE | `/api/orders/{id}/` | Delete an order | Yes (admin only) |
| GET | `/api/order-count/{business_user_id}/` | Get in-progress order count | Yes |
| GET | `/api/completed-order-count/{business_user_id}/` | Get completed order count | Yes |

### Reviews

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/reviews/` | List all reviews | Yes |
| POST | `/api/reviews/` | Create a review | Yes (customer only) |
| PATCH | `/api/reviews/{id}/` | Update a review | Yes (author only) |
| DELETE | `/api/reviews/{id}/` | Delete a review | Yes (author only) |

### Base Information

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/base-info/` | Platform statistics | No |

## Project Structure

```
backend/
├── core/                   # Project settings and main URL configuration
├── auth_app/               # Registration and login
│   └── api/
├── profile_app/            # User profiles (business & customer)
│   └── api/
├── offers_app/             # Offers and offer details
│   └── api/
├── orders_app/             # Orders and order counts
│   └── api/
├── review_app/             # Reviews
│   └── api/
├── base_info_app/          # Platform statistics
│   └── api/
├── media/                  # Uploaded files (excluded from version control)
├── requirements.txt
└── manage.py
```

## Notes

- Media files (profile pictures, offer images) are stored in the `media/` directory
- The database (`db.sqlite3`) is excluded from version control
- CORS is configured to allow all origins in development
