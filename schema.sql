-- =====================================================================
--  E-COMMERCE PROJECT : DATABASE FOR THE WEBSITE  (MySQL)
--  Same 6 tables as your ER diagram / lab script.
--  Run this file once before starting the website:
--      mysql -u root -p < schema.sql
--  (or open it in MySQL Workbench and click the lightning bolt)
--  Password of all 3 sample users:  password123
-- =====================================================================

DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE TABLE users (
    userid    INT AUTO_INCREMENT PRIMARY KEY,
    username  VARCHAR(45)  NOT NULL UNIQUE,
    firstname VARCHAR(45)  NOT NULL,
    lastname  VARCHAR(45)  NOT NULL,
    address   VARCHAR(120) NOT NULL,
    mobile    BIGINT       NOT NULL,
    email     VARCHAR(100),
    password  VARCHAR(255) NOT NULL      -- stored as a hash, not the real password
);

CREATE TABLE seller (
    sellerid INT PRIMARY KEY,
    sname    VARCHAR(45) NOT NULL,
    email    VARCHAR(45) NOT NULL,
    rating   DECIMAL(2,1),
    phone    BIGINT      NOT NULL
);

CREATE TABLE product (
    productid INT PRIMARY KEY,
    pname     VARCHAR(45) NOT NULL,
    price     FLOAT       NOT NULL,
    qty       INT         NOT NULL,
    sellerid  INT,
    FOREIGN KEY (sellerid) REFERENCES seller (sellerid)
);

CREATE TABLE orders (
    orderid   INT AUTO_INCREMENT PRIMARY KEY,
    userid    INT NOT NULL,
    orderdate DATETIME,
    total     DECIMAL(10,2) NOT NULL,
    shipping  VARCHAR(6)    NOT NULL,
    FOREIGN KEY (userid) REFERENCES users (userid)
);

CREATE TABLE orderitem (
    orderitemid INT AUTO_INCREMENT PRIMARY KEY,
    orderid     INT NOT NULL,
    productid   INT NOT NULL,
    quantity    INT NOT NULL,
    unitprice   DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (orderid)   REFERENCES orders (orderid),
    FOREIGN KEY (productid) REFERENCES product (productid)
);

CREATE TABLE payment (
    paymentid INT AUTO_INCREMENT PRIMARY KEY,
    paymethod VARCHAR(20)   NOT NULL,
    paydate   DATETIME,
    amount    DECIMAL(10,2) NOT NULL,
    orderid   INT NOT NULL,
    FOREIGN KEY (orderid) REFERENCES orders (orderid)
);

-- ---------------- sample data (same as your script) ----------------
INSERT INTO users (userid, username, firstname, lastname, address, mobile, email, password) VALUES
(1, 'arjun_raj', 'Arjun', 'Rajput', '45 Malviya Nagar, Jaipur, Rajasthan', 8955999809, 'arjun.raj@gmail.com',     'pbkdf2:sha256:1000000$JGKISHF1DCppmumu$47e84aef6991d3386c6064749ebfd571134128dcbeaa5c6d6becd8bf208178a0'),
(2, 'priya_s',   'Priya', 'Sharma', '12 MG Road, Bengaluru, Karnataka',    9549363968, 'priya.sharma@gmail.com', 'pbkdf2:sha256:1000000$JGKISHF1DCppmumu$47e84aef6991d3386c6064749ebfd571134128dcbeaa5c6d6becd8bf208178a0'),
(3, 'amit_k',    'Amit',  'Kumar',  'Andheri West, Mumbai, Maharashtra',   6376734033, 'amit.kumar@gmail.com',   'pbkdf2:sha256:1000000$JGKISHF1DCppmumu$47e84aef6991d3386c6064749ebfd571134128dcbeaa5c6d6becd8bf208178a0');

INSERT INTO seller VALUES
(101, 'Mobile Junction', 'contact@mobilejunction.in', 4.5, 9549710680),
(102, 'Laptop World',    'sales@laptopworld.in',      4.2, 9929988430),
(103, 'Desi Threads',    'cs@desithreads.in',         4.8, 8764321009);

INSERT INTO product VALUES
(1001, 'Samsung', 75000,  50, 101),
(1002, 'Apple',   80000,  30, 101),
(1003, 'Google',  70000,  25, 101),
(2001, 'HP',      60000,  20, 102),
(2002, 'Lenovo',  55000,  15, 102),
(2003, 'Apple',   95000,  10, 102),
(3001, 'Jeans',    1500, 100, 103),
(3002, 'Shirt',     999, 150, 103),
(3003, 'Tshirt',    599, 200, 103);

INSERT INTO orders VALUES
(501, 1, '2026-08-12 10:15:00', 81500, 'FREE'),
(502, 2, '2026-08-12 11:30:00', 60000, 'FREE'),
(503, 3, '2026-08-12 12:45:00',  2197, '50');

INSERT INTO orderitem VALUES
(1, 501, 1002, 1, 80000),
(2, 501, 3001, 1,  1500),
(3, 502, 2001, 1, 60000),
(4, 503, 3002, 1,   999),
(5, 503, 3003, 2,   599);

INSERT INTO payment VALUES
(9001, 'UPI',         '2026-08-12 10:16:00', 81500, 501),
(9002, 'Credit Card', '2026-08-12 11:32:00', 60000, 502),
(9003, 'Net Banking', '2026-08-12 12:46:00',  2197, 503);

SELECT * FROM users;
SELECT * FROM product;
SELECT * FROM orders;
