-- Extra queries for practice / viva. Run after schema.sql
use ecommerce;

-- 1. WHERE : costly products
select pname, price from product where price > 50000;

-- 2. ORDER BY + LIMIT : best rated seller
select sname, rating from seller order by rating desc limit 1;

-- 3. JOIN (2 tables) : who placed which order
select o.orderid, u.firstname, u.lastname, o.total
from orders o join users u on o.userid = u.userid;

-- 4. JOIN (3 tables) : what is inside each order
select o.orderid, p.pname, oi.quantity, oi.unitprice
from orders o
join orderitem oi on o.orderid = oi.orderid
join product p on oi.productid = p.productid;

-- 5. JOIN : order with payment method
select o.orderid, pay.paymethod, pay.amount
from orders o join payment pay on o.orderid = pay.orderid;

-- 6. GROUP BY + SUM : sales of each seller
select s.sname, sum(oi.quantity * oi.unitprice) as total_sales
from orderitem oi
join product p on oi.productid = p.productid
join seller s on p.sellerid = s.sellerid
group by s.sellerid, s.sname;

-- 7. GROUP BY + COUNT : products of each seller
select s.sname, count(p.productid) as total_products
from seller s left join product p on s.sellerid = p.sellerid
group by s.sellerid, s.sname;

-- 8. Subquery : users who have placed an order
select username from users where userid in (select userid from orders);

-- 9. LEFT JOIN : users with no order
select u.username from users u
left join orders o on u.userid = o.userid
where o.orderid is null;

-- 10. Low stock
select pname, qty from product where qty < 20;

-- 11. VIEW
create or replace view order_summary as
select o.orderid, u.username, o.total, pay.paymethod
from orders o
join users u on o.userid = u.userid
join payment pay on o.orderid = pay.orderid;

select * from order_summary;
