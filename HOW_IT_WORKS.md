# ShopEasy - How it works (for my presentation)

## 1. What is the project?
ShopEasy is a small online shopping website. A user can register, login, search products, add them to a cart, place an order and pay. Everything is saved in a **MySQL database**. The website is made with **Python (Flask)** and **HTML/CSS**.

| Part | What it does | Made with | Folder |
|---|---|---|---|
| Database | stores the data | MySQL | `database/` |
| Backend | decides what happens on each click | Python Flask | `backend/` |
| Frontend | the pages the user sees | HTML + CSS | `frontend/` |

## 2. What happens when I click a button?
Example: click **Add to Cart**.
1. Browser sends a request to Flask (`/add_to_cart/1001`).
2. Flask runs the matching Python function (`add_to_cart`).
3. The function asks MySQL if the product is in stock.
4. Flask saves the item in the cart and sends back a new HTML page.

Words to remember:
- **Route** = a URL linked to a function (`@app.route("/cart")`).
- **GET** = open a page. **POST** = send a filled form.
- **Template** = HTML page with blanks like `{{ p.pname }}` that Flask fills.
- **Session** = small memory of the website for each user (who is logged in, what is in the cart).

## 3. Database (same as my ER diagram)
6 tables: `users`, `seller`, `product`, `orders`, `orderitem`, `payment`.

| Table | Stores | Primary key | Foreign key |
|---|---|---|---|
| users | customer details + password | userid | - |
| seller | seller details + rating | sellerid | - |
| product | name, price, stock | productid | sellerid -> seller |
| orders | order date, total, shipping | orderid | userid -> users |
| orderitem | products inside an order | orderitemid | orderid -> orders, productid -> product |
| payment | how and how much was paid | paymentid | orderid -> orders |

**Relationships (from my ER diagram)**
- User **places** many orders (1 : n)
- Order **contains** many order items (1 : n)
- Product **appears in** many order items (1 : n)
- Seller **lists** many products (1 : n)
- Order is **paid by** one payment (1 : 1)

**Small things I changed from my lab script** (be ready to tell the teacher)
1. `AUTO_INCREMENT` on userid, orderid, orderitemid, paymentid so MySQL gives new ids by itself.
2. `phone` of users is now `mobile` and `email` is added (these are from my own ALTER commands). `password` is in my ER diagram, so it is added in the table.
3. `DECIMAL` became `DECIMAL(10,2)` so paise are not lost.
4. There is **no cart table**. The cart is kept in the session until the order is placed (then it goes to orders + orderitem).

**Files in `database/`**
- `schema.sql` - run this for the website (tables + data).
- `lab_script_original.sql` - my original lab commands (CREATE, INSERT, ALTER, UPDATE, TRUNCATE, RENAME, JOIN). It drops and recreates `ecommerce`, so run `schema.sql` again after showing it.
- `queries.sql` - extra queries (WHERE, ORDER BY, JOIN, GROUP BY, subquery, LEFT JOIN, VIEW).

## 4. Backend files

### config.py
Settings only: MySQL password, secret key, shipping rule (free above Rs.5000, else Rs.50), payment methods. **Change the MySQL password here.**

### db.py
| Function | What it does |
|---|---|
| `get_connection()` | connects to MySQL |
| `fetch_all(sql, params)` | runs SELECT, gives all rows |
| `fetch_one(sql, params)` | runs SELECT, gives one row |
| `execute(sql, params)` | runs INSERT/UPDATE/DELETE and saves with `commit()` |

We write `%s` in the query and give values separately. This is called a *parameterized query* and it stops **SQL injection**.

### app.py - helper functions
| Function | What it does |
|---|---|
| `rupee()` | shows 81500 as Rs. 81,500.00 on pages |
| `is_logged_in()` | checks if `userid` is in the session |
| `calculate_shipping()` | 0 if total >= 5000 else 50 |
| `get_cart_items()` | takes product ids from the session cart and gets their name/price from MySQL |
| `cart_subtotal()` | adds up the cart |
| `inject_cart_count()` | gives the navbar the number of items in cart |

### app.py - pages (routes)
| Function | URL | What it does |
|---|---|---|
| `home()` | `/` | shows products; search by name and filter by seller using `LIKE` and `WHERE` |
| `register()` | `/register` | checks the form, hashes password, INSERT into users |
| `login()` | `/login` | finds the user, compares password with hash, saves userid in session |
| `logout()` | `/logout` | clears the session |
| `add_to_cart()` | `/add_to_cart/<id>` | adds product to the session cart (checks stock) |
| `cart()` | `/cart` | shows cart, total and shipping |
| `update_cart()` | `/cart/update/<id>` | changes quantity (0 removes) |
| `remove_from_cart()` | `/cart/remove/<id>` | removes an item |
| `checkout()` | `/checkout` | shows summary; on POST it places the order |
| `orders()` | `/orders` | my order history |
| `order_detail()` | `/order/<id>` | one order in detail (only my own) |
| `sellers()` | `/sellers` | sellers + number of products (COUNT, GROUP BY) |
| `report()` | `/report` | total users/orders/revenue, sales per seller, low stock |

### What `checkout()` does (most important)
When I press **Place Order**:
1. INSERT a row in `orders`.
2. For every cart item: reduce `qty` in `product` and INSERT a row in `orderitem`.
3. INSERT a row in `payment`.
4. `commit()` to save all. If anything fails, `rollback()` undoes everything.

This is a **transaction** (all or nothing - the A of ACID). Then the cart is emptied.

*Note:* `orders.total` = price of the items only (same as my sample data). Shipping is shown separately as FREE or 50.

## 5. Frontend files (`frontend/templates/`)
| File | Page |
|---|---|
| `base.html` | navbar + messages + footer. All other pages use `{% extends "base.html" %}` |
| `home.html` | search box + product cards |
| `register.html`, `login.html` | forms |
| `cart.html` | cart table |
| `checkout.html` | summary + payment method |
| `orders.html`, `order_detail.html` | order history / details |
| `sellers.html`, `report.html` | seller list / report |
| `static/style.css` | colours and layout |

Jinja2 basics: `{{ value }}` prints, `{% for %}` loops, `{% if %}` conditions, `url_for('cart')` gives the URL of function `cart`.

## 6. Safety things I used
1. Password is stored as a **hash**, not plain text.
2. **Parameterized queries** against SQL injection.
3. Cart / checkout / orders need login, and a user can see only his own orders.
4. Input checks (10-digit mobile, password length, stock limit).

## 7. Demo steps (5 minutes)
1. Run `schema.sql` in Workbench and show `SELECT * FROM product;`.
2. Open website -> search "apple", filter by seller.
3. Register a new user and login.
4. Add products to cart, change quantity. Small order = Rs.50 shipping, big order = FREE.
5. Checkout with UPI -> show the order page.
6. In Workbench: `SELECT * FROM orders; SELECT * FROM orderitem; SELECT * FROM payment; SELECT pname, qty FROM product;` -> new rows and reduced stock.
7. Open Report page and explain JOIN / GROUP BY. Run 2-3 queries from `queries.sql`.

## 8. Viva questions
1. **Primary key / foreign key?** Primary key identifies a row uniquely. Foreign key refers to the primary key of another table.
2. **Why `orders` and `orderitem` separately?** One order has many products; we cannot put a list in one cell (1NF), so each product gets its own row in orderitem.
3. **Why `unitprice` in orderitem?** Product price may change later; old orders must keep the old price.
4. **What is a JOIN?** Combining rows of two tables using a common column. I used INNER JOIN and LEFT JOIN.
5. **Transaction? Where used?** Group of queries that run fully or not at all. In `checkout()` with commit/rollback.
6. **ACID?** Atomicity, Consistency, Isolation, Durability.
7. **SQL injection?** Typing SQL code in input boxes to attack. Stopped with `%s` parameters.
8. **Why hash the password?** If the database leaks, real passwords are safe.
9. **GET vs POST?** GET opens a page, POST sends form data to change something.
10. **What is a session?** Memory kept for each user (login + cart).
11. **DELETE vs TRUNCATE vs DROP?** DELETE removes chosen rows, TRUNCATE removes all rows, DROP removes the table.
12. **DDL vs DML?** DDL changes structure (CREATE, ALTER, DROP, TRUNCATE). DML changes data (INSERT, UPDATE, DELETE, SELECT).
13. **How is stock reduced safely?** `UPDATE product SET qty = qty - n WHERE qty >= n`; if nothing changes, order is rolled back.
14. **What is Flask?** A small Python framework that links URLs to functions.
15. **Why no cart table?** Cart is temporary, so it stays in the session; only the final order goes to the database.

## 9. What is missing (future work)
- Real payment gateway (payment is only recorded).
- Admin login (Report page is open to all).
- Product images, reviews, order cancellation.
