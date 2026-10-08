# config.py  -  all settings of the project in ONE place.
# Change the password below to YOUR MySQL root password.

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",   # <-- change this
    "database": "ecommerce",
}

SECRET_KEY = "change-this-to-any-random-text"   # Flask needs it for login sessions

FREE_SHIPPING_ABOVE = 5000    # items worth Rs.5000 or more -> free shipping
SHIPPING_CHARGE = 50          # otherwise Rs.50 shipping

PAYMENT_METHODS = ["UPI", "Credit Card", "Net Banking", "Cash on Delivery"]
