# Nyondo General Hardware Management System

A Django-based web application developed to manage inventory, sales transactions, stock records, and customer purchase schemes for Nyondo General Hardware.

## Features

### 1. Inventory Management
- Record and manage stock entries.
- Track suppliers, product categories, and quantities delivered.
- Record unit costs and selling prices.
- Monitor supplier payment status and payment methods.
- Calculate remaining stock quantities and stock value.
- Identify low-stock items.

### 2. Sales Management
- Record customer sales and selected products.
- Validate available stock before processing sales.
- Automatically calculate subtotals and total prices.
- Calculate transport fees based on delivery distance and purchase value.
- Generate sales receipts.
- Edit sales records.
- View sales reports and dashboards.

### 3. Customer Purchase Scheme
- Register and manage scheme customers.
- Record customer payments and generate payment receipts.
- Track goods collected by customers.
- Calculate customer scheme balances.
- Link goods pickups to sales records.

### 4. Dashboards and Reports
- Administrator dashboard.
- Sales dashboard.
- Stock dashboard.
- Sales performance reports.
- Stock reports and low-stock monitoring.

### 5. User Authentication and Access Control
- User registration and login.
- Administrator approval of newly registered accounts.
- Role-based access for administrators, sales managers, and stock managers.

## Technology Stack

- **Backend:** Python, Django
- **Database:** SQLite for local development; PostgreSQL for production deployment
- **Frontend:** HTML, CSS, Django Templates
- **Static Files:** WhiteNoise
- **Production Server:** Gunicorn
- **Deployment:** Render

## Project Structure

```text
Hardware-System-Nyondo/
├── hardware/       # Django project configuration
├── nyondo/         # Inventory and sales management
├── scheme/         # Customer purchase scheme management
├── users/          # Authentication and user management
├── templates/      # HTML templates
├── static/         # CSS, images and other static assets
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/dorcustumulamye/Hardware-System-Nyondo-.git
cd Hardware-System-Nyondo-
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

### 6. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application at:

http://127.0.0.1:8000/

## User Roles

The application supports the following management roles:

- **Administrator:** Access to administrative functions and overall management dashboards.
- **Sales Manager:** Access to sales operations and customer scheme management.
- **Stock Manager:** Access to inventory operations and stock reporting.

The corresponding Django groups must be configured before users can register with these roles.

## Deployment Configuration

The application supports deployment using environment variables.

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DEBUG` | Enables or disables debug mode |
| `ALLOWED_HOSTS` | Permitted application hostnames |
| `DATABASE_URL` | Production database connection |
| `CSRF_TRUSTED_ORIGINS` | Trusted application origins |
| `SECURE_SSL_REDIRECT` | Enforces HTTPS redirects |
| `SESSION_COOKIE_SECURE` | Secures session cookies |
| `CSRF_COOKIE_SECURE` | Secures CSRF cookies |
| `SECURE_HSTS_SECONDS` | Configures HTTP Strict Transport Security |

For production, use a secure secret key, disable debug mode, and configure the appropriate hostnames and HTTPS settings.

## License

This project is maintained as a software project for Nyondo General Hardware.