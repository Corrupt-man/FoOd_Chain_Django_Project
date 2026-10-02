# FoOd Chain® — Django food ordering demo

A local educational project inspired by common food-delivery ordering flows. It includes registration/login/logout, a food menu, session-based cart, checkout, itemized billing, order history, and Django admin.

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create/activate a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Initialize database: `python manage.py migrate`
6. Create admin: `python manage.py createsuperuser`
7. Load sample menu: `python manage.py seed_menu`
8. Start: `python manage.py runserver`
9. Visit http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Demo scope
- Currency shown as PKR.
- Checkout creates an order and bill; it does not process real payments.
- No delivery partner tracking, restaurant marketplace, email/SMS, or payment gateway.
- For production: configure a secret key and DEBUG=False, use PostgreSQL, HTTPS, secure cookies, payment-provider integration, and deployment settings.
