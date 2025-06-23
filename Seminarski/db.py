import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

# --- Database class ---
class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            total REAL,
            date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")

        self.con.commit()

    def add_customer(self, name, email):
        self.cur.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        self.con.commit()

    def add_product(self, name, price):
        self.cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.con.commit()

    def add_order(self, customer_id, product_id, quantity, total, date):
        self.cur.execute("INSERT INTO orders (customer_id, product_id, quantity, total, date) VALUES (?, ?, ?, ?, ?)",
                         (customer_id, product_id, quantity, total, date))
        self.con.commit()

    def fetch_customers(self):
        self.cur.execute("SELECT * FROM customers")
        return self.cur.fetchall()

    def fetch_products(self):
        self.cur.execute("SELECT * FROM products")
        return self.cur.fetchall()

    def fetch_orders(self):
        self.cur.execute("""
        SELECT orders.id, customers.name, customers.email, products.name, products.price, orders.quantity, orders.total, orders.date
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN products ON orders.product_id = products.id
        """)
        return self.cur.fetchall()

    def update_product(self, product_id, name, price):
        self.cur.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (name, price, product_id))
        self.con.commit()

    def delete_product(self, product_id):
        self.cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.con.commit()

    def delete_order(self, order_id):
        self.cur.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.con.commit()