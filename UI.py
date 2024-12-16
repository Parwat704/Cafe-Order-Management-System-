import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Menu of the restaurant
menu = {
    'Pizza': {
        'Margherita': 180,
        'Pepperoni': 220,
        'Veggie': 200,
    },
    'Pasta': {
        'Alfredo': 150,
        'Marinara': 120,
        'Pesto': 170,
    },
    'Burger': {
        'Cheese Burger': 300,
        'Chicken Burger': 320,
        'Veggie Burger': 280,
    },
    'Coffee': {
        'Espresso': 60,
        'Cappuccino': 80,
        'Latte': 90,
    },
    'Tea': {
        'Black Tea': 25,
        'Green Tea': 35,
        'Herbal Tea': 45,
    },
}

# Flask server URL
API_URL = "http://127.0.0.1:5000/order"

class RestroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekend Restro")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f0f0")

        # Heading Label
        heading = tk.Label(root, text="Welcome to Weekend Restro", font=("Helvetica", 28, "bold"),
                           bg="#2c3e50", fg="#ecf0f1", relief="raised", bd=5, padx=20, pady=10)
        heading.pack(pady=10)

        # Main Frame
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Frame for Menu 
        menu_frame = tk.Frame(main_frame, bg="#ffffff", relief="groove", bd=5)
        menu_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        menu_label = tk.Label(menu_frame, text="Our Menu", font=("Helvetica", 20, "underline"), bg="#ffffff", fg="#8e44ad")
        menu_label.pack(pady=10)

        # Create boxes for each category
        self.quantities = {}
        self.selections = {}
        for category, items in menu.items():
            item_frame = tk.Frame(menu_frame, bg="#ffffff")
            item_frame.pack(pady=10, padx=10, anchor='w')

            item_label = tk.Label(item_frame, text=category, font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#2c3e50")
            item_label.pack(side=tk.LEFT, padx=10)

            # Dropdown to select specific type
            item_var = tk.StringVar()
            item_combobox = ttk.Combobox(item_frame, values=list(items.keys()), textvariable=item_var, state="readonly", font=("Helvetica", 14))
            item_combobox.pack(side=tk.LEFT, padx=10)
            item_combobox.set("Select Type")

            # Spinbox to select quantity
            quantity = tk.IntVar(value=0)
            self.quantities[category] = quantity
            self.selections[category] = item_var
            quantity_spinbox = tk.Spinbox(item_frame, from_=0, to=10, width=5, font=("Helvetica", 14), textvariable=quantity)
            quantity_spinbox.pack(side=tk.RIGHT)

        # Frame for Order Summary
        summary_frame = tk.Frame(main_frame, bg="#ffffff", relief="groove", bd=5)
        summary_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        summary_label = tk.Label(summary_frame, text="Order Summary", font=("Helvetica", 20, "underline"), bg="#ffffff", fg="#8e44ad")
        summary_label.pack(pady=10)

        self.cart_frame = tk.Frame(summary_frame, bg="#f5f5f5")
        self.cart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Total Label
        self.total_label = tk.Label(root, text="Total Amount: Rs 0", font=("Helvetica", 20), bg="#34495e", fg="#ecf0f1", relief="ridge", padx=10, pady=10)
        self.total_label.pack(pady=10, fill=tk.X)

        # Button Frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        order_button = ttk.Button(button_frame, text="Add to Order", command=self.add_to_cart)
        order_button.grid(row=0, column=0, padx=10)

        finalize_button = ttk.Button(button_frame, text="Finalize Order", command=self.finalize_order)
        finalize_button.grid(row=0, column=1, padx=10)

        clear_button = ttk.Button(button_frame, text="Clear Order", command=self.clear_order)
        clear_button.grid(row=0, column=2, padx=10)

        # Initialize order data
        self.cart = {}
        self.order_total = 0

    def add_to_cart(self):
        # Clear current cart display
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        # Add items to the cart
        self.cart = {}
        for category, quantity in self.quantities.items():
            qty = quantity.get()
            selected_item = self.selections[category].get()
            if qty > 0 and selected_item != "Select Type":
                self.cart[selected_item] = qty

        # Update cart display
        for item, qty in self.cart.items():
            # Find the price from the menu
            for category, items in menu.items():
                if item in items:
                    price = items[item]
                    break
            cart_item = tk.Label(self.cart_frame, text=f"{item} x {qty} = Rs {price * qty}", font=("Helvetica", 14), bg="#f5f5f5", fg="#2c3e50")
            cart_item.pack(anchor='w')

        # Update total
        self.update_total()

    def update_total(self):
        self.order_total = 0
        for item, qty in self.cart.items():
            for category, items in menu.items():
                if item in items:
                    self.order_total += items[item] * qty
                    break
        self.total_label.config(text=f"Total Amount: Rs {self.order_total}")

    def clear_order(self):
        # Reset selections and quantities
        for category in self.quantities:
            self.quantities[category].set(0)
            self.selections[category].set("Select Type")

        # Clear cart and reset total
        self.cart = {}
        self.order_total = 0
        self.total_label.config(text="Total Amount: Rs 0")

        # Clear cart display
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        messagebox.showinfo("Order Cleared", "All items have been removed from the order.")

    def finalize_order(self):
      if not self.cart:
        messagebox.showwarning("No Items Ordered", "You have not ordered any items.")
      else:
        order_data = {
            "items": self.cart,
            "total": self.order_total,
        }
        try:
            # Set headers to specify JSON content
            headers = {'Content-Type': 'application/json'}
            response = requests.post(API_URL, json=order_data, headers=headers)
            
            if response.status_code == 200:
                order_id = response.json().get('order_id', 'N/A')  # Default to 'N/A' if key not found
                messagebox.showinfo("Order Finalized", f"Order placed successfully! Order ID: {order_id}")
            else:
                messagebox.showerror("Error", f"Failed to place the order. Error: {response.text}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to the server.\nError: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = RestroApp(root)
    root.mainloop()
