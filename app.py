# app.py  -  the BACKEND of our e-commerce website (Flask + MySQL)
#
# Run it with:   python app.py      then open  http://127.0.0.1:5000
#
# Idea: the browser asks for a URL (like /cart). Flask finds the function
# marked with that URL (a "route"), the function talks to MySQL, and then it
# sends back an HTML page (a "template") filled with data.

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import config
from db import get_connection, fetch_all, fetch_one, execute

# Tell Flask where our HTML (frontend) files are kept
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
app.secret_key = config.SECRET_KEY


# =====================================================================
#  HELPER FUNCTIONS  (small tools used by the routes below)
# =====================================================================

@app.template_filter("rupee")
def rupee(value):
    """Show a number like 81500 as  Rs. 81,500.00  inside HTML pages."""
    return "Rs. {:,.2f}".format(float(value))


def is_logged_in():
    """True if a user has logged in (their id is stored in the session)."""
    return "userid" in session


def calculate_shipping(subtotal):
    """Free shipping for big orders, otherwise a fixed charge."""
    if subtotal >= config.FREE_SHIPPING_ABOVE:
        return 0
    return config.SHIPPING_CHARGE


def get_cart_items():
    """The cart is kept in the session as a dictionary: {productid: quantity}.
    This function looks up each product in MySQL and returns full details."""
    cart = session.get("cart", {})
    items = []
    for productid, quantity in cart.items():
        product = fetch_one(
            "SELECT productid, pname, price, qty FROM product WHERE productid = %s",
            (int(productid),),
        )
        if product is not None:
            product["quantity"] = quantity
            product["stock"] = product["qty"]
            product["line_total"] = float(product["price"]) * quantity
            items.append(product)
    return items


def cart_subtotal(items):
    """Add up the line totals of all cart items."""
    total = 0
    for item in items:
        total = total + item["line_total"]
    return total


@app.context_processor
def inject_cart_count():
    """Makes 'cart_count' available in EVERY html page (for the navbar badge)."""
    count = 0
    for quantity in session.get("cart", {}).values():
        count = count + quantity
    return {"cart_count": count}


# =====================================================================
#  1. HOME PAGE : list / search / filter products
# =====================================================================

@app.route("/")
def home():
    # values typed in the search box (they come in the URL, e.g. /?q=apple)
    q = request.args.get("q", "").strip()
    sellerid = request.args.get("sellerid", "")

    # Build the SQL step by step depending on which filters are used
    sql = """
        SELECT p.productid, p.pname, p.price, p.qty, s.sname
        FROM product p
        JOIN seller s ON p.sellerid = s.sellerid
        WHERE 1 = 1
    """
    params = []

    if q != "":
        sql = sql + " AND p.pname LIKE %s"
        params.append("%" + q + "%")
    if sellerid.isdigit():
        sql = sql + " AND p.sellerid = %s"
        params.append(int(sellerid))

    sql = sql + " ORDER BY p.productid"

    products = fetch_all(sql, tuple(params))
    sellers = fetch_all("SELECT sellerid, sname FROM seller ORDER BY sname")

    return render_template(
        "home.html",
        products=products,
        sellers=sellers,
        q=q,
        selected_seller=sellerid,
    )


# =====================================================================
#  2. REGISTER / LOGIN / LOGOUT
# =====================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    # GET  = the user just opened the page  -> show the empty form
    # POST = the user pressed the Register button -> process the form
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    firstname = request.form.get("firstname", "").strip()
    lastname = request.form.get("lastname", "").strip()
    email = request.form.get("email", "").strip()
    mobile = request.form.get("mobile", "").strip()
    address = request.form.get("address", "").strip()
    password = request.form.get("password", "")

    # ----- validation (check the input before saving) -----
    if not (username and firstname and lastname and mobile and address and password):
        flash("Please fill all the fields.", "error")
        return redirect(url_for("register"))
    if not (mobile.isdigit() and len(mobile) == 10):
        flash("Mobile number must be exactly 10 digits.", "error")
        return redirect(url_for("register"))
    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("register"))

    existing = fetch_one("SELECT userid FROM users WHERE username = %s", (username,))
    if existing is not None:
        flash("That username is already taken. Try another one.", "error")
        return redirect(url_for("register"))

    # never store the real password - store its hash
    password_hash = generate_password_hash(password)

    execute(
        """INSERT INTO users (username, firstname, lastname, address, mobile, email, password)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (username, firstname, lastname, address, int(mobile), email, password_hash),
    )
    flash("Registration successful! Please login.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))

    # check_password_hash compares the typed password with the stored hash
    if user is None or not check_password_hash(user["password"], password):
        flash("Wrong username or password.", "error")
        return redirect(url_for("login"))

    # remember the user in the session (a small cookie-based memory)
    session["userid"] = user["userid"]
    session["username"] = user["username"]
    flash("Welcome back, " + user["firstname"] + "!", "success")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# =====================================================================
#  3. CART : add, view, change quantity, remove
#     (the cart lives in the session, so there is no cart table)
# =====================================================================

@app.route("/add_to_cart/<int:productid>", methods=["POST"])
def add_to_cart(productid):
    if not is_logged_in():
        flash("Please login to add items to your cart.", "error")
        return redirect(url_for("login"))

    product = fetch_one("SELECT productid, pname, qty FROM product WHERE productid = %s", (productid,))
    if product is None:
        flash("Product not found.", "error")
        return redirect(url_for("home"))

    cart = session.get("cart", {})
    key = str(productid)                    # session keys must be text
    already = cart.get(key, 0)

    if already + 1 > product["qty"]:
        flash("Only " + str(product["qty"]) + " piece(s) of " + product["pname"] + " in stock.", "error")
    else:
        cart[key] = already + 1
        session["cart"] = cart              # save the cart back in the session
        flash(product["pname"] + " added to cart.", "success")

    return redirect(request.referrer or url_for("home"))


@app.route("/cart")
def cart():
    if not is_logged_in():
        flash("Please login to see your cart.", "error")
        return redirect(url_for("login"))

    items = get_cart_items()
    subtotal = cart_subtotal(items)
    shipping = calculate_shipping(subtotal) if items else 0
    return render_template("cart.html", items=items, subtotal=subtotal, shipping=shipping)


@app.route("/cart/update/<int:productid>", methods=["POST"])
def update_cart(productid):
    if not is_logged_in():
        return redirect(url_for("login"))

    quantity = request.form.get("quantity", "")
    if not quantity.isdigit():
        flash("Enter a valid quantity.", "error")
        return redirect(url_for("cart"))
    quantity = int(quantity)

    product = fetch_one("SELECT pname, qty FROM product WHERE productid = %s", (productid,))
    cart = session.get("cart", {})
    key = str(productid)

    if product is None or key not in cart:
        flash("Cart item not found.", "error")
    elif quantity == 0:
        del cart[key]
        session["cart"] = cart
        flash("Item removed from cart.", "success")
    elif quantity > product["qty"]:
        flash("Only " + str(product["qty"]) + " piece(s) of " + product["pname"] + " in stock.", "error")
    else:
        cart[key] = quantity
        session["cart"] = cart
        flash("Cart updated.", "success")
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:productid>", methods=["POST"])
def remove_from_cart(productid):
    if not is_logged_in():
        return redirect(url_for("login"))
    cart = session.get("cart", {})
    cart.pop(str(productid), None)
    session["cart"] = cart
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))


# =====================================================================
#  4. CHECKOUT : turn the cart into an order + payment
# =====================================================================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not is_logged_in():
        flash("Please login to checkout.", "error")
        return redirect(url_for("login"))

    userid = session["userid"]
    items = get_cart_items()
    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("cart"))

    # total = price of the items (same as the sample data); shipping is shown separately
    total = round(cart_subtotal(items), 2)
    shipping = calculate_shipping(total)

    # ---- show the checkout page ----
    if request.method == "GET":
        user = fetch_one("SELECT firstname, lastname, address FROM users WHERE userid = %s", (userid,))
        return render_template(
            "checkout.html", items=items, total=total, shipping=shipping,
            user=user, methods=config.PAYMENT_METHODS,
        )

    # ---- the user pressed "Place Order" ----
    paymethod = request.form.get("paymethod", "")
    if paymethod not in config.PAYMENT_METHODS:
        flash("Please choose a payment method.", "error")
        return redirect(url_for("checkout"))

    # We change 3 tables (orders, orderitem, product) + payment.
    # Either ALL changes happen or NONE (a "transaction").
    conn = get_connection()
    cursor = conn.cursor()
    try:
        now = datetime.now()
        shipping_text = "FREE" if shipping == 0 else str(shipping)

        # 1) create the order
        cursor.execute(
            "INSERT INTO orders (userid, orderdate, total, shipping) VALUES (%s, %s, %s, %s)",
            (userid, now, total, shipping_text),
        )
        orderid = cursor.lastrowid

        # 2) for each cart item: reduce stock and add an order item
        for item in items:
            cursor.execute(
                "UPDATE product SET qty = qty - %s WHERE productid = %s AND qty >= %s",
                (item["quantity"], item["productid"], item["quantity"]),
            )
            if cursor.rowcount == 0:
                raise ValueError("Not enough stock for " + item["pname"])

            cursor.execute(
                "INSERT INTO orderitem (orderid, productid, quantity, unitprice) VALUES (%s, %s, %s, %s)",
                (orderid, item["productid"], item["quantity"], item["price"]),
            )

        # 3) record the payment
        cursor.execute(
            "INSERT INTO payment (paymethod, paydate, amount, orderid) VALUES (%s, %s, %s, %s)",
            (paymethod, now, total, orderid),
        )

        conn.commit()      # everything worked -> save all changes
    except Exception as error:
        conn.rollback()    # something failed -> undo everything
        flash("Order failed: " + str(error), "error")
        return redirect(url_for("cart"))
    finally:
        cursor.close()
        conn.close()

    session["cart"] = {}   # empty the cart
    flash("Order placed successfully! Your order number is " + str(orderid) + ".", "success")
    return redirect(url_for("order_detail", orderid=orderid))


# =====================================================================
#  5. ORDERS : history and details of one order
# =====================================================================

@app.route("/orders")
def orders():
    if not is_logged_in():
        flash("Please login to see your orders.", "error")
        return redirect(url_for("login"))

    rows = fetch_all(
        """SELECT o.orderid, o.orderdate, o.total, o.shipping, pay.paymethod
           FROM orders o
           LEFT JOIN payment pay ON o.orderid = pay.orderid
           WHERE o.userid = %s
           ORDER BY o.orderid DESC""",
        (session["userid"],),
    )
    return render_template("orders.html", orders=rows)


@app.route("/order/<int:orderid>")
def order_detail(orderid):
    if not is_logged_in():
        flash("Please login first.", "error")
        return redirect(url_for("login"))

    # userid in WHERE -> a user can only open HIS OWN orders
    order = fetch_one(
        """SELECT o.orderid, o.orderdate, o.total, o.shipping,
                  u.firstname, u.lastname, u.address,
                  pay.paymethod, pay.amount, pay.paydate
           FROM orders o
           JOIN users u ON o.userid = u.userid
           LEFT JOIN payment pay ON o.orderid = pay.orderid
           WHERE o.orderid = %s AND o.userid = %s""",
        (orderid, session["userid"]),
    )
    if order is None:
        flash("Order not found.", "error")
        return redirect(url_for("orders"))

    items = fetch_all(
        """SELECT p.pname, oi.quantity, oi.unitprice,
                  (oi.quantity * oi.unitprice) AS line_total
           FROM orderitem oi
           JOIN product p ON oi.productid = p.productid
           WHERE oi.orderid = %s""",
        (orderid,),
    )
    return render_template("order_detail.html", order=order, items=items)


# =====================================================================
#  6. SELLERS PAGE and 7. REPORT PAGE
# =====================================================================

@app.route("/sellers")
def sellers():
    rows = fetch_all(
        """SELECT s.sellerid, s.sname, s.email, s.rating, s.phone,
                  COUNT(p.productid) AS total_products
           FROM seller s
           LEFT JOIN product p ON s.sellerid = p.sellerid
           GROUP BY s.sellerid, s.sname, s.email, s.rating, s.phone
           ORDER BY s.rating DESC"""
    )
    return render_template("sellers.html", sellers=rows)


@app.route("/report")
def report():
    # This page shows how JOIN, GROUP BY and SUM work on our data.
    # (In a real website only an admin would be allowed to see it.)
    all_orders = fetch_all(
        """SELECT o.orderid, u.username, o.orderdate, o.total, pay.paymethod
           FROM orders o
           JOIN users u ON o.userid = u.userid
           LEFT JOIN payment pay ON o.orderid = pay.orderid
           ORDER BY o.orderid DESC"""
    )
    sales_by_seller = fetch_all(
        """SELECT s.sname, SUM(oi.quantity * oi.unitprice) AS sales
           FROM orderitem oi
           JOIN product p ON oi.productid = p.productid
           JOIN seller s ON p.sellerid = s.sellerid
           GROUP BY s.sellerid, s.sname
           ORDER BY sales DESC"""
    )
    low_stock = fetch_all("SELECT pname, qty FROM product WHERE qty < 20 ORDER BY qty")
    summary = fetch_one(
        """SELECT (SELECT COUNT(*) FROM users)   AS total_users,
                  (SELECT COUNT(*) FROM orders)  AS total_orders,
                  (SELECT COALESCE(SUM(amount), 0) FROM payment) AS total_revenue"""
    )
    return render_template(
        "report.html",
        all_orders=all_orders, sales_by_seller=sales_by_seller,
        low_stock=low_stock, summary=summary,
    )


# =====================================================================
#  START THE SERVER
# =====================================================================
if __name__ == "__main__":
    app.run(debug=True)    # debug=True: auto-restart + error details (only for learning)
