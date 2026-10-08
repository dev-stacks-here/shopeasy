import os

# config.py - all settings of the project in ONE place.
# Reads environment variables (for Vercel / Cloud MySQL) with local fallbacks.

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "your_mysql_password"),
    "database": os.environ.get("DB_NAME", "ecommerce"),
}

# Optional SSL settings for cloud databases (e.g. TiDB Cloud, Aiven)
if os.environ.get("DB_SSL_CA"):
    DB_CONFIG["ssl_ca"] = os.environ.get("DB_SSL_CA")
if os.environ.get("DB_SSL_DISABLED", "").lower() in ("true", "1"):
    DB_CONFIG["ssl_disabled"] = True

SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-to-any-random-text")

FREE_SHIPPING_ABOVE = 5000    # items worth Rs.5000 or more -> free shipping
SHIPPING_CHARGE = 50          # otherwise Rs.50 shipping

PAYMENT_METHODS = ["UPI", "Credit Card", "Net Banking", "Cash on Delivery"]
