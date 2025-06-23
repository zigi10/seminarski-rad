import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

# Dummy Database class for demonstration; replace with your actual implementation
class Database:
    def __init__(self, db_path):
        pass
    def fetch_customers(self):
        return []
    def fetch_products(self):
        return []
    def fetch_orders(self):
        return []
    def add_customer(self, name, email):
        pass
    def add_product(self, name, price):
        pass
    def update_product(self, product_id, name, price):
        pass
    def delete_product(self, product_id):
        pass
    def add_order(self, customer_id, product_id, quantity, total, date):
        pass

class OnlineStoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = Database("Store.db")

        self.title("Online Store System")
        self.geometry("1200x700")
        self.configure(fg_color="#2c3e50")

        # Varijable
        self.name = ctk.StringVar()
        self.email = ctk.StringVar()
        self.product_name = ctk.StringVar()
        self.price = ctk.StringVar()
        self.quantity = ctk.StringVar()
        self.search_customer = ctk.StringVar()
        self.search_product = ctk.StringVar()

        self.selected_product_id = None

        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        tabview = ctk.CTkTabview(self)
        tabview.pack(expand=True, fill="both", padx=20, pady=20)

        tab_customers = tabview.add("Customers")
        tab_products = tabview.add("Products")
        tab_orders = tabview.add("Orders")

        # --- Customers Tab ---
        ctk.CTkLabel(tab_customers, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(tab_customers, textvariable=self.name).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab_customers, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(tab_customers, textvariable=self.email).grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(tab_customers, text="Add Customer", command=self.add_customer).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Products Tab ---
        ctk.CTkLabel(tab_products, text="Product Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(tab_products, textvariable=self.product_name).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab_products, text="Price ($):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(tab_products, textvariable=self.price).grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(tab_products, text="Add Product", command=self.add_product).grid(row=2, column=0, pady=10)
        ctk.CTkButton(tab_products, text="Update Product", command=self.update_product).grid(row=2, column=1, pady=10)
        ctk.CTkButton(tab_products, text="Delete Product", command=self.delete_product).grid(row=2, column=2, pady=10)

        self.tv_products = ttk.Treeview(tab_products, columns=(1, 2, 3), show="headings", height=10)
        self.tv_products.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)

        self.tv_products.heading(1, text="ID")
        self.tv_products.heading(2, text="Product")
        self.tv_products.heading(3, text="Price")

        self.tv_products.bind("<Double-1>", self.select_product)

        # --- Orders Tab ---
        ctk.CTkLabel(tab_orders, text="Customer:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_customers = ttk.Combobox(tab_orders, state="readonly")
        self.combo_customers.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab_orders, text="Product:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.combo_products = ttk.Combobox(tab_orders, state="readonly")
        self.combo_products.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(tab_orders, text="Quantity:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        ctk.CTkEntry(tab_orders, textvariable=self.quantity).grid(row=2, column=1, padx=10, pady=5)

        ctk.CTkButton(tab_orders, text="Place Order", command=self.add_order).grid(row=3, column=0, columnspan=2, pady=10)

        self.tv_orders = ttk.Treeview(tab_orders, columns=(1, 2, 3, 4, 5, 6, 7, 8), show="headings", height=10)
        self.tv_orders.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=10)

        self.tv_orders.heading(1, text="ID")
        self.tv_orders.heading(2, text="Customer")
        self.tv_orders.heading(3, text="Email")
        self.tv_orders.heading(4, text="Product")
        self.tv_orders.heading(5, text="Price")
        self.tv_orders.heading(6, text="Quantity")
        self.tv_orders.heading(7, text="Total")
        self.tv_orders.heading(8, text="Date")

    def refresh_data(self):
        # Popunjavanje combobox-ova
        self.combo_customers["values"] = [f"{c[0]} - {c[1]} ({c[2]})" for c in self.db.fetch_customers()]
        self.combo_products["values"] = [f"{p[0]} - {p[1]} (${p[2]})" for p in self.db.fetch_products()]

        # Popunjavanje tabele proizvoda
        for i in self.tv_products.get_children():
            self.tv_products.delete(i)
        for row in self.db.fetch_products():
            self.tv_products.insert("", "end", values=row)

        # Popunjavanje tabele porudžbina
        for i in self.tv_orders.get_children():
            self.tv_orders.delete(i)
        for row in self.db.fetch_orders():
            self.tv_orders.insert("", "end", values=row)

    def add_customer(self):
        if self.name.get() and self.email.get():
            try:
                self.db.add_customer(self.name.get(), self.email.get())
                messagebox.showinfo("Success", "Customer added successfully!")
                self.name.set("")
                self.email.set("")
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input error", "Please fill name and email.")

    def add_product(self):
        if self.product_name.get() and self.price.get():
            try:
                price = float(self.price.get())
                self.db.add_product(self.product_name.get(), price)
                messagebox.showinfo("Success", "Product added successfully!")
                self.product_name.set("")
                self.price.set("")
                self.refresh_data()
            except ValueError:
                messagebox.showerror("Input error", "Price must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input error", "Please fill product name and price.")

    def select_product(self, event):
        selected = self.tv_products.focus()
        values = self.tv_products.item(selected, "values")
        if values:
            self.selected_product_id = values[0]
            self.product_name.set(values[1])
            self.price.set(values[2])

    def update_product(self):
        if self.selected_product_id and self.product_name.get() and self.price.get():
            try:
                price = float(self.price.get())
                self.db.update_product(self.selected_product_id, self.product_name.get(), price)
                messagebox.showinfo("Success", "Product updated successfully!")
                self.product_name.set("")
                self.price.set("")
                self.selected_product_id = None
                self.refresh_data()
            except ValueError:
                messagebox.showerror("Input error", "Price must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Selection error", "Please select a product and fill all fields.")

    def delete_product(self):
        selected = self.tv_products.focus()
        values = self.tv_products.item(selected, "values")
        if values:
            try:
                self.db.delete_product(values[0])
                messagebox.showinfo("Success", "Product deleted successfully!")
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Selection error", "Please select a product to delete.")

    def add_order(self):
        try:
            customer_id = int(self.combo_customers.get().split(" - ")[0])
            product_info = self.combo_products.get()
            product_id = int(product_info.split(" - ")[0])
            quantity = int(self.quantity.get())

            # Dohvati cenu proizvoda iz baze ili iz combobox-a
            products = self.db.fetch_products()
            price = 0
            for p in products:
                if p[0] == product_id:
                    price = p[2]
                    break
            total = price * quantity
            date = datetime.now().strftime("%Y-%m-%d")

            self.db.add_order(customer_id, product_id, quantity, total, date)
            messagebox.showinfo("Success", "Order placed successfully!")
            self.quantity.set("")
            self.refresh_data()
        except ValueError:
            messagebox.showerror("Input error", "Please select customer, product and enter valid quantity.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = OnlineStoreApp()
    app.mainloop()