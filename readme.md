# Aggregate-function-sql

Мы продаём Мерч от IT-Academy, наши клиенты люди разных сортов, от обычных рабочих, до высших руководителей компаний.  
Будем вести отчетность о наших клиентах и продажах в базе данных.  

Мы будем использовать три таблицы. customers, products и orders.  
Выглядит примерно так...  
![image](https://user-images.githubusercontent.com/48368029/121824978-bc0afd00-ccd1-11eb-99ca-8edbb4d64e6e.png)

Мы используем таблицу orders чтобы связать клиентов и наш мерч в связи многие-ко-многим, так как у клиентов может быть несколько покупок одного и того же товара, а так у товара могут быть множество покупателей.

```sql 
CREATE TABLE IF NOT EXISTS customers(id serial primary key, name varchar(50), surname varchar(50), birth_day date, email varchar(50) unique, address varchar(50), spent int)
CREATE TABLE IF NOT EXISTS products(id serial primary key, product_name varchar(100), price int, stock int)
CREATE TABLE IF NOT EXISTS orders(id serial primary key, customer_id INT REFERENCES customers(id), product_id INT REFERENCES products(id), order_date date)
```

Учтите что таблица orders добавляется в последнюю очередь, так как она обращается к таблицам customers и products, если таких отношений на стадии создания таблицы orders не окажется, то dbms выдаст вам ошибку.

Заполним наши таблицы изначальными данными.

```sql
INSERT INTO customers(name, surname, birth_day, email, address, spent) VALUES
	('John', 'Snow', '1970-06-23', 'joshsnow@google.ru', 'Russia, 544 Tyapkin St, 43', 0),
	('Elon', 'Musk', '1971-06-28', 'elonreevmusk@tesla.com', 'USA, 420 Weembledown St, 12', 250),
	('Bill', 'Gates', '1955-10-28', 'bgmicro@microsoft.com', 'USA, 233 Melinda St, 2', 320),
	('Jeff', 'Bezos', '1973-02-23', 'bezoss@amazon.com', 'USA, 234 Volotine St, 13', 160),
	('Robert', 'Kasandra', '1988-02-06', 'rbkas@google.com', 'Romania, 544 Hielbeen St, 522', 50),
	('Serj', 'Ivanov', '1985-10-19', 'serjik@google.ru', 'Russia, 322 Stavkina St, 8', 100)

INSERT INTO products(id, product_name, price, stock) VALUES
	(1, 'Handmade IT-Academy logo (3d printed)', 160, 6),
	(2, 'IT-Academy stickers pack', 50, 2),
	(3, 'IT-Academy tea glass', 100, 6)
 
INSERT INTO orders(customer_id, product_id, order_date) VALUES
	(2, 3, '2019-10-22'),
	(2, 3, '2019-10-23'),
	(2, 2, '2020-10-28'),
	(3, 1, '2020-11-15'),
	(3, 1, '2020-11-22'),
	(4, 1, '2020-11-28'),
	(5, 2, '2020-10-28'),
	(6, 3, '2021-02-23')
```
### Customers
![image](https://user-images.githubusercontent.com/48368029/121825125-98948200-ccd2-11eb-9c71-ddba169e7cae.png)
### Products
![image](https://user-images.githubusercontent.com/48368029/121825147-a2b68080-ccd2-11eb-9aff-d0a86c9dafb1.png)
### Orders
![image](https://user-images.githubusercontent.com/48368029/121825165-ac3fe880-ccd2-11eb-848b-607b0216ac51.png)


## Views
Теперь давайте поиграемся с SQL запросами :C  
```sql 
SELECT * from customers
```
Выдаёт нам всю информацию о пользователе. Но мы бы хотели не показывать email адрес, адрес, и день рождения клиента каждому желающему. В таком случае, мы можем сделать следущее.
```sql
SELECT id, name, surname, birth_day from customers
```
![image](https://user-images.githubusercontent.com/48368029/121825276-3f791e00-ccd3-11eb-86eb-3ccd25d20650.png)

Так, в psql есть возможность добавлять view, они значительно облегчают работу, если вам часто приходится писать длинные выборки. С помощью view мы сможем сохранить публичную информацию о клиенте в "якобы" отдельной таблице.

для это создадим нашу view
```sql
CREATE VIEW customers_public AS
SELECT id, name, surname, birth_day from customers
```

теперь мы можем обращаться к нашей view как к отдельной таблице.
```sql
SELECT * from customers public
```
![image](https://user-images.githubusercontent.com/48368029/121825347-a7c7ff80-ccd3-11eb-97eb-d8d5242d157c.png)
Если мы попытаемся узнать конфиденциальную информацию о клиенте через view, то получим следущее  
![image](https://user-images.githubusercontent.com/48368029/121825363-ca5a1880-ccd3-11eb-8ee2-3f99deb0dc6e.png)

## JOINS

Это все хорошо но при запуске `select * from orders` мы получаем таблицу из цифр...  А мы бы хотели видеть имя клиента, и что же он купил и когда.
Давай-те же напишем выборку которая подставит все что нам нужно вместо этих идентификационных номеров.

```sql
SELECT c.name, c.surname, p.product_name, o.order_date from orders as o
	JOIN customers as c ON c.id = o.customer_id
	JOIN products as p ON p.id = o.product_id
	ORDER BY c.name
```
![image](https://user-images.githubusercontent.com/48368029/121825474-6edc5a80-ccd4-11eb-9f9a-42e17b97e8c3.png)  
Теперь разберем что же делает эта выборка.
`JOIN` это аггрегатная фунцкия она используются для того, чтобы совмещать две или более таблицы в зависимости от столбца.  
Бывают разные виды наложения таблиц, ниже предоставлю фотоилюстрацию, которая вполне описывает принцип работы различных JOIN'ов  
![image](https://user-images.githubusercontent.com/48368029/121825551-ead6a280-ccd4-11eb-842a-35b182ed6ba4.png)

>Мы используем JOIN, на самом деле это INNER JOIN но вписывать INNER не всегда обязательно.  
>JOIN по стандарту использует INNER JOIN.  

Так вот, в выборке выше, мы выбираем `c.name, c.surname` из таблицы `customers`. Мы можем обращаться к таблице customers как `c`, так как мы присвоили данной таблице `alias c` путем написания `customers AS c`, возможно это тоже новый концепт для вас, но считайте, что мы просто переименовали таблицу `customers` в `c` в данном случае, а в противном же случае, нам пришлось бы прописывать `customers.name, customers.surname` и так далее.  
С таблицей products и orders мы поступили так же (`p, o` соответственно).   
Путем написания `ON` мы можем передать SQL, информацию о том, в каком случае мы хотим сложить таблицы.  
Мы забираем `c.name, c.surname` из таблицы `customers` только в том случае если `o.customer_id = c.id` (тоесть id клиента равен customer_id заказа)  
Точно так же мы выбираем `p.product_name` из таблицы `products`, если `o.product_id = p.id` (тоесть id товара равен product_id заказа)  
`o.order_date` даёт нам дату когда был сделан заказ.  
`ORDER BY` позволяет нам отсортировать таблицу по определенному столбцу. В примере выше мы сортируем ее по имени клиента. `c.name`  
Если хотите сортировать заказы по дате заказа используйте ```ORDER BY o.order_date```  
так же можно определить в восходящем или нисходящем порядке распределять данные.   
```ORDER BY o.order_date ASC``` для восходящего.    
```ORDER BY o.order_date DESC``` для нисходящего.     
Как итог мы получаем таблицу со столбцами: `name, surname, product_name и order_date`

Теперь закрепим тему о views путем создания view для данной выборки, чтобы в будущем нам не пришлось писать все это по новой, а мы могли получить список заказов одной простой выборкой.

```sql
CREATE VIEW orders_list AS
	SELECT c.name, c.surname, p.product_name, o.order_date from orders as o
	JOIN customers as c ON c.id = o.customer_id
	JOIN products as p ON p.id = o.product_id
	ORDER BY c.name
```

```sql
SELECT * FROM orders_list
```
![image](https://user-images.githubusercontent.com/48368029/121825914-d0052d80-ccd6-11eb-9712-5f49bfcad7a4.png)  

## GROUP BY

Пожалуй расскажу вам про еще кое-какие операторы с помощью которых вы сможете доставать различную информацию из вашей базы данных.  
Первый из них **GROUP BY**  

Оператор **GROUP BY** группирует строки с одинаковыми значениями в итоговые строки, например «найдите количество клиентов в каждой стране» или «найдите количество заказов у каждого из покупателей».  
Оператор **GROUP BY** часто используется с агрегатными функциями (COUNT (), MAX (), MIN (), SUM (), AVG ()) для группировки набора результатов по одному или нескольким столбцам.

Вот пример, как бы вы искали «количество заказов у каждого из покупателей»  
```sql
SELECT c.name as customer_name, count(o.id) as orders_ammount from orders as o
	LEFT JOIN customers as c ON o.customer_id = c.id
	GROUP BY name
	ORDER BY orders_ammount DESC
```
![image](https://user-images.githubusercontent.com/48368029/121826369-2d01e300-ccd9-11eb-8d61-2ae0fec5f5f3.png)  
Так то лучше!  
Сразу видно, что Elon Musk больше всех любит мерч IT-academy ))

`COUNT(o.id) as orders_ammount` посчитал количество заказов для каждого `c.id` и сгрупировал их по `c.name` имени заказчика.  
Только взгляните, мы снова используем alias. На этот раз для столбца COUNT(o.id), это позволило нам отсортировать результат по этому столбцу в ```ORDER BY orders_ammount```  

Но, что не так с данной выборкой?  
Верно, наш клиент John Snow, заказов которого нету в таблице orders не показан в списке результатов.   
Все потому, что мы используем `INNER JOIN`. Тоесть мы берем информацию только о тех кто находится в обеих таблицах.  
Посмотрите на таблицу с JOINами вновь, какое наложение лучше выбрать на этот раз?  
Верно, `RIGHT JOIN` это наш выбор. Таким образом мы возьмём всю таблицу `customers` и часть от `orders`. Что означает, что даже при отсутствии John Snow в нашей таблице `orders`, он будет записан в наш конечный результат.  
```sql
SELECT c.name as customer_name, count(o.id) as orders_ammount from orders as o
	RIGHT JOIN customers as c ON o.customer_id = c.id
	GROUP BY name
	ORDER BY orders_ammount DESC
```
![image](https://user-images.githubusercontent.com/48368029/121826663-b534b800-ccda-11eb-8a44-9081500aa8f4.png)


## BETWEEN
Еще один оператор, который может вам пригодиться это оператор **BETWEEN**
Оператор BETWEEN выбирает значения в заданном диапазоне. Значения могут быть числами, текстом или датами.  

По сути, данный оператор позволит взять данные из таблицы, в которой Значение в определенном столбце, входит в диапазон который мы указываем с помощью `BETWEEN` и `AND`  
Рассмотрим на примере:  
Давайте посмотрим на заказы, которые были сделаны в промежуток между 1 января 2019 года и 31 декабря 2020 года.  

```sql
SELECT * from orders_list
WHERE order_date
	BETWEEN '2019-01-01' AND '2020-12-31'
	ORDER BY order_date
```
![image](https://user-images.githubusercontent.com/48368029/121826824-9aaf0e80-ccdb-11eb-8358-f06f7943e1e2.png)

Вы ведь помните, что мы создавали view с именнем orders_list, используем ее чтобы получить данные о клиенте и совершенном заказе.  
Далее мы используем `WHERE order_date` чтобы указать в каком столбце будет оперировать наш оператор between.  
Затем, сразу после **BETWEEN** указывем начало диапазона, а сразу после **AND** конец диапазона. Это почти как in range(start, end) в нашем любимом Python.  
Ну и конечно же отсортируем все по столбцу order_date, чтобы получить эстетическое удовольствие (наверное)  
Вуаля! получаем заказы сделанные в тот самый промежуток. Однако **BETWEEN** используется не только с датами, вот примеры использованния BETWEEN с числовым типом и строкой.

#### int  
Продукты цена которых находится в промежутке между 100 и 200  
```sql
SELECT * from products
WHERE price
	BETWEEN 100 AND 200
	ORDER BY price ASC
```
![image](https://user-images.githubusercontent.com/48368029/121827049-828bbf00-ccdc-11eb-8919-fda0b82dc08e.png)

#### string  
Клиенты имена которых начинаются с буквы в промежутке между A и G  
```sql
SELECT * from customers_public
WHERE name
	BETWEEN 'A' AND 'G'
```
![image](https://user-images.githubusercontent.com/48368029/121827136-c7175a80-ccdc-11eb-9dad-c717af0cb3ca.png)

## LIKE / ILIKE

```sql
SELECT * from customers
	WHERE email like '%.com'
```
