import sqlite3
from sqlite3 import Error


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(':memory:')
        print("Connection to SQLite DB successful")
    except Error as e:
        print(e)

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        print(cursor.fetchall())
    except Error as e:
        print(e)


create_users_table = """
    CREATE TABLE IF NOT EXISTS clients (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL
    );
"""

create_products_table = """
CREATE TABLE IF NOT EXISTS products(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL, 
  price DECIMAL(10, 2) NOT NULL
);
"""

create_orders_table = """
CREATE TABLE IF NOT EXISTS orders(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  name TEXT NOT NULL, 
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES clients (id)
);
"""

create_m2m_orders_products = """
CREATE TABLE IF NOT EXISTS m2m_orders_products(
  product_id INTEGER NOT NULL,
  order_id INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products (id) FOREIGN KEY (order_id) REFERENCES orders (id)
);
"""

create_clients = """
INSERT INTO
  clients (name)
VALUES
  ('Иван'),
  ('Константин'),
  ('Дмитрий'),
  ('Александр');
"""

create_products = """
INSERT INTO
  products (name, price)
VALUES
  ('Мяч', 299.99),
  ('Ручка', 18),
  ('Кружка', 159.87),
  ('Монитор', 18000),
  ('Телефон', 9999.9),
  ('Кофе', 159);
"""

create_orders = """
INSERT INTO
  orders (name, user_id)
VALUES
  ('Закупка 1', 2),
  ('Закупка 2', 1),
  ('Закупка 3', 4),
  ('Закупка 4', 3);
"""
create_m2m = """
INSERT INTO
  m2m_orders_products (product_id, order_id)
VALUES
  (2, 1),
  (5, 1),
  (1, 1),
  (1, 2),
  (3, 2),
  (6, 2),
  (2, 2),
  (5, 3),
  (6, 4),
  (3, 4),
  (5, 2);
"""

get_full_price_for_clients = """
SELECT clients.name, SUM(price)
FROM clients, products, orders, m2m_orders_products 
WHERE (orders.user_id = clients.id and m2m_orders_products.order_id = orders.id and m2m_orders_products.product_id = products.id)
GROUP BY
   clients.name;
"""

get_clients_with_phone = """
SELECT
   clients.name
FROM
   clients, products, orders, m2m_orders_products
WHERE (products.name = 'Телефон' and m2m_orders_products.order_id = orders.id and orders.user_id = clients.id and m2m_orders_products.product_id = products.id)
GROUP BY clients.name;
"""

get_products_orders_count = """
SELECT
   name,
   COUNT(order_id)
FROM
   m2m_orders_products
INNER JOIN products ON products.id = m2m_orders_products.product_id
GROUP BY
   name;
"""


if __name__ == '__main__':
    # Создаём базу данных в оперативной памяти, для изменения исправить функцию create_connection()
    conn = create_connection()
    # Создаем отношения и записываем данные
    execute_query(conn, create_users_table)
    execute_query(conn, create_products_table)
    execute_query(conn, create_orders_table)
    execute_query(conn, create_m2m_orders_products)
    execute_query(conn, create_clients)
    execute_query(conn, create_products)
    execute_query(conn, create_orders)
    execute_query(conn, create_m2m)

    # Список клиентов с общей суммой их покупок
    execute_query(conn, get_full_price_for_clients)
    # Список клиентов, которые купили телефон
    execute_query(conn, get_clients_with_phone)
    # Список товаров с количеством их заказов
    execute_query(conn, get_products_orders_count)
