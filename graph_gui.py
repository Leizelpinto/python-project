import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Data store
user_data = {}

# First Page - Sign In
def open_equation_page():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    
    if not name or not email:
        messagebox.showwarning("Input Error", "Please enter both name and email.")
        return
    
    user_data["name"] = name
    user_data["email"] = email
    
    # Hide sign-in window and open equation window
    signin_window.withdraw()
    open_graph_window()

# Second Page - Equation Input
def open_graph_window():
    def plot():
        equation = equation_entry.get()
        try:
            x = np.linspace(-10, 10, 1000)
            y = eval(equation, {"x": x, "np": np, "__builtins__": {}})
            plt.figure(figsize=(8, 5))
            plt.plot(x, y, label=f"y = {equation}")
            plt.title(f"{user_data['name']}'s Graph of y = {equation}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.legend()
            plt.axhline(0, color='black', linewidth=0.5)
            plt.axvline(0, color='black', linewidth=0.5)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid equation:\n{e}")

    graph_window = tk.Toplevel()
    graph_window.title("Enter Equation")

    welcome_label = tk.Label(graph_window, text=f"Welcome, {user_data['name']}!", font=("Arial", 14))
    welcome_label.pack(pady=10)

    tk.Label(graph_window, text="Enter an equation in terms of x (e.g., x**2 + 2*x - 1):").pack(pady=5)
    equation_entry = tk.Entry(graph_window, width=40)
    equation_entry.pack(pady=5)

    plot_button = tk.Button(graph_window, text="Plot Graph", command=plot)
    plot_button.pack(pady=10)

# Main window
signin_window = tk.Tk()
signin_window.title("Sign In")

tk.Label(signin_window, text="Enter your name:").pack(pady=5)
name_entry = tk.Entry(signin_window, width=40)
name_entry.pack(pady=5)

tk.Label(signin_window, text="Enter your email:").pack(pady=5)
email_entry = tk.Entry(signin_window, width=40)
email_entry.pack(pady=5)

signin_button = tk.Button(signin_window, text="Continue", command=open_equation_page)
signin_button.pack(pady=15)

signin_window.mainloop()
