-- My original lab script (only comments added, and IF EXISTS in the first line).
-- This one is for showing DDL / DML commands. For the website run schema.sql.

drop database if exists ecommerce;
create database ecommerce;
use ecommerce;

-- DDL : CREATE
CREATE TABLE users (
    userid INT PRIMARY KEY,
    username VARCHAR(45) NOT NULL,
    firstname VARCHAR(45) NOT NULL,
    lastname VARCHAR(45) NOT NULL,
    address VARCHAR(120) NOT NULL,
    phone 	BIGINT NOT NULL
);
CREATE TABLE seller (
    sellerid INT PRIMARY KEY,
    sname VARCHAR(45) NOT NULL,
    email VARCHAR(45) NOT NULL,
    rating DECIMAL(2 , 1 ),
    phone BIGINT  NOT NULL
);
CREATE TABLE product (
    productid INT PRIMARY KEY,
    pname VARCHAR(45) NOT NULL,
    price FLOAT NOT NULL,
    qty INT NOT NULL,
    sellerid INT,
    FOREIGN KEY (sellerid)
        REFERENCES seller (sellerid)
);
CREATE TABLE orders (
    orderid INT PRIMARY KEY,
    userid INT NOT NULL,
    orderdate DATETIME,
    total DECIMAL NOT NULL,
    shipping VARCHAR(6) NOT NULL,
    FOREIGN KEY (userid)
        REFERENCES users (userid)
);
CREATE TABLE orderitem (
    orderitemid INT PRIMARY KEY,
    orderid INT NOT NULL,
    productid INT NOT NULL,
    quantity INT NOT NULL,
    unitprice DECIMAL NOT NULL,
    FOREIGN KEY (orderid)
        REFERENCES orders (orderid),
    FOREIGN KEY (productid)
        REFERENCES product (productid)
);
CREATE TABLE payment (
    paymentid INT PRIMARY KEY,
    paymethod VARCHAR(20) NOT NULL,
    paydate DATETIME,
    amount DECIMAL NOT NULL,
    orderid int not null,
    FOREIGN KEY (orderid)
        REFERENCES orders(orderid)
);

-- DML : INSERT
INSERT INTO users VALUES 
(1, 'arjun_raj', 'Arjun', 'Rajput', '45 Malviya Nagar, Jaipur, Rajasthan', 8955999809),
(2, 'priya_s', 'Priya', 'Sharma', '12 MG Road, Bengaluru, Karnataka', 9549363968),
(3, 'amit_k', 'Amit', 'Kumar', 'Andheri West, Mumbai, Maharashtra', 6376734033);

INSERT INTO seller VALUES 
(101, 'Mobile Junction', 'contact@mobilejunction.in', 4.5, 9549710680),
(102, 'Laptop World', 'sales@laptopworld.in', 4.2, 9929988430),
(103, 'Desi Threads', 'cs@desithreads.in', 4.8, 8764321009);

INSERT INTO product VALUES 
(1001, 'Samsung', 75000, 50, 101),
(1002, 'Apple', 80000, 30, 101),
(1003, 'Google', 70000, 25, 101),
(2001, 'HP', 60000, 20, 102),
(2002, 'Lenovo', 55000, 15, 102),
(2003, 'Apple', 95000, 10, 102),
(3001, 'Jeans', 1500, 100, 103),
(3002, 'Shirt', 999, 150, 103),
(3003, 'Tshirt', 599, 200, 103);

INSERT INTO orders VALUES 
(501, 1, '2026-08-12 10:15:00', 81500, 'FREE'),
(502, 2, '2026-08-12 11:30:00', 60000, 'FREE'),
(503, 3, '2026-08-12 12:45:00', 2197, '50');

INSERT INTO orderitem VALUES 
(1, 501, 1002, 1, 80000),
(2, 501, 3001, 1, 1500),
(3, 502, 2001, 1, 60000),
(4, 503, 3002, 1, 999),
(5, 503, 3003, 2, 599);

INSERT INTO payment VALUES 
(9001, 'UPI', '2026-08-12 10:16:00', 81500, 501),
(9002, 'Credit Card', '2026-08-12 11:32:00', 60000, 502),
(9003, 'Net Banking', '2026-08-12 12:46:00', 2197, 503);

-- DML : SELECT
select * from users ;
select * from seller ;
select * from product ;
select * from orders ;
select * from orderitem ;
select * from payment ;

desc payment;

-- DDL : TRUNCATE (deletes all rows but keeps the table)
TRUNCATE TABLE orderitem;

-- DDL : ALTER
ALTER TABLE users 
	ADD COLUMN email VARCHAR(100);

ALTER TABLE users 
	RENAME COLUMN phone TO mobile;
    
-- DML : UPDATE
UPDATE product 
SET 
    price = 77000,
    qty = 45
WHERE
    productid = 1001;
    
UPDATE users SET email = 'arjun.raj@gmail.com' WHERE userid = 1;
UPDATE users SET email = 'priya.sharma@gmail.com' WHERE userid = 2;
UPDATE users SET email = 'amit.kumar@gmail.com' WHERE userid = 3;

select * from users ;
select * from seller ;
select * from product ;
select * from orders ;
select * from orderitem ;
select * from payment ;

-- DDL : RENAME table
ALTER TABLE orderitem 
	RENAME TO cart;

-- JOIN
select * from users,orders where users.userid=orders.userid;
