#https://gist.github.com/keeilzhanstd/bca93626647e843d5c1f57601d4093cb

import psycopg2
from datetime import datetime
from pprint import pprint

credentials = {"DBNAME": "functionsdb", "USER":"postgres","PASSWORD":"123","PORT":"5432"}


def executor(method):
	def wrapper(*args, **kwargs):
		args[0].cursor = args[0].connection.cursor()
		rec = method(*args, **kwargs)
		args[0].cursor.close()
		return rec
	return wrapper

class DBConnection:
	def __init__(self):
		try:
			self.connection = psycopg2.connect(dbname=credentials["DBNAME"], user=credentials['USER'], password=credentials['PASSWORD'], port=credentials['PORT'])
			self.connection.autocommit = True
			pprint("Successfully connected")
		except:
			pprint("Cannot connect to database")

	@executor
	def execute(self, command):
		self.cursor.execute(command)
		try:
			res = self.cursor.fetchall()
			return res
		except:
			pass
			#pprint(command)

def showres(array):
	if array:
		for el in array:
			print(el)

if __name__=='__main__':
	db = DBConnection()
	create_customers_table = "CREATE TABLE IF NOT EXISTS customers(id serial primary key, name varchar(50), surname varchar(50), birth_day date, email varchar(50) unique, address varchar(50), spent int)"
	create_products_table = "CREATE TABLE IF NOT EXISTS products(id serial primary key, product_name varchar(100), price int, stock int)"
	create_orders_table = "CREATE TABLE IF NOT EXISTS orders(id serial primary key, customer_id INT REFERENCES customers(id), product_id INT REFERENCES products(id), order_date date)"

	insertintocustomerscmd = """
	INSERT INTO customers(name, surname, birth_day, email, address, spent) VALUES
	('John', 'Snow', '1970-06-23', 'joshsnow@google.ru', 'Russia, 544 Tyapkin St, 43', 0),
	('Elon', 'Musk', '1971-06-28', 'elonreevmusk@tesla.com', 'USA, 420 Weembledown St, 12', 250),
	('Bill', 'Gates', '1955-10-28', 'bgmicro@microsoft.com', 'USA, 233 Melinda St, 2', 320),
	('Jeff', 'Bezos', '1973-02-23', 'bezoss@amazon.com', 'USA, 234 Volotine St, 13', 160),
	('Robert', 'Kasandra', '1988-02-06', 'rbkas@google.com', 'Romania, 544 Hielbeen St, 522', 50),
	('Serj', 'Ivanov', '1985-10-19', 'serjik@google.ru', 'Russia, 322 Stavkina St, 8', 100)
	"""
	insertintoproductscmd = """
	INSERT INTO products(id, product_name, price, stock) VALUES
	(1, 'Handmade IT-Academy logo (3d printed)', 160, 6),
	(2, 'IT-Academy stickers pack', 50, 2),
	(3, 'IT-Academy tea glass', 100, 6)
	"""

	insertintoorderscmd = """
	INSERT INTO orders(customer_id, product_id, order_date) VALUES
	(2, 3, '2019-10-22'),
	(2, 3, '2019-10-23'),
	(2, 2, '2020-10-28'),
	(3, 1, '2020-11-15'),
	(3, 1, '2020-11-22'),
	(4, 1, '2020-11-28'),
	(5, 2, '2020-10-28'),
	(6, 3, '2021-02-23')
	"""

	user_no_confidential_view = """
	CREATE VIEW customers_public AS
	SELECT id, name, surname, birth_day from customers
	"""

	users_orders = """
	CREATE VIEW users_orders AS
	SELECT c.name, c.surname, p.product_name, o.order_date from orders as o
	JOIN customers as c ON c.id = o.customer_id
	JOIN products as p ON p.id = o.product_id
	ORDER BY c.name
	"""

	users_GROUP_BY_name_orders_count = """
	SELECT c.name, count(o.id) as orders_ammount from orders as o
	LEFT JOIN customers as c ON o.customer_id = c.id
	GROUP BY name
	"""

	between_sql_query = """
	SELECT c.name, p.product_name, o.order_date from orders as o
	JOIN customers as c ON c.id = o.customer_id
	JOIN products as p ON p.id = o.product_id
	WHERE o.order_date
	BETWEEN '2019-01-01' AND '2020-12-31'
	ORDER BY o.order_date
	""" 

	search_by_email_ending_with_com = """
	SELECT * from customers
	WHERE email like '%.com'
	"""

	search_by_email_google_com_ending = """
	SELECT * from customers
	WHERE email like '%google.com'
	"""

	search_by_email_different_cntcodes = """
	SELECT * from customers
	WHERE email like '%google.%'
	"""

	search_by_address_case_sensitive = """
	SELECT * from customers
	WHERE address like '%r%'
	"""

	search_by_address_case_senseless = """
	SELECT * from customers
	WHERE address ilike '%r%'
	"""
	#db.execute(create_orders_table)
	#db.execute(create_orders_table)
	#db.execute(create_orders_table)

	#db.execute(insertintocustomerscmd)
	#db.execute(insertintoproductscmd)
	#db.execute(insertintoorderscmd)

	showres(db.execute(/*command*/))
