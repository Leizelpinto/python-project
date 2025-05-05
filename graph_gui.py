import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import re

class SimpleGraphingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Graphing Calculator")

        # Data store for user information
        self.user_data = {}

        # Initial screen with buttons for options
        self.menu_screen()

    def menu_screen(self):
        self.clear_root()

        # Welcome message and instructions
        welcome_label = tk.Label(self.root, text="Welcome to the Graphing Calculator!", font=("Arial", 16))
        welcome_label.pack(pady=20)

        instructions_label = tk.Label(self.root, text="Please choose an option below.", font=("Arial", 12))
        instructions_label.pack(pady=10)

        # Button for Sign In
        signin_button = tk.Button(self.root, text="Sign In", width=20, height=2, command=self.signin_screen)
        signin_button.pack(pady=10)

        # Button for Exit
        exit_button = tk.Button(self.root, text="Exit", width=20, height=2, command=self.root.quit)
        exit_button.pack(pady=10)

    def signin_screen(self):
        self.clear_root()

        tk.Label(self.root, text="Enter your name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Enter your email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=40)
        self.email_entry.pack(pady=5)

        signin_button = tk.Button(self.root, text="Continue", command=self.open_graph_screen)
        signin_button.pack(pady=15)

    def open_graph_screen(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not email:
            messagebox.showwarning("Input Error", "Please enter both name and email.")
            return

        self.user_data["name"] = name
        self.user_data["email"] = email

        self.clear_root()

        welcome_label = tk.Label(self.root, text=f"Welcome, {self.user_data['name']}!", font=("Arial", 14))
        welcome_label.pack(pady=10)

        tk.Label(self.root, text="Enter an equation in terms of x (e.g., x**2 + 2*x - 1):").pack(pady=5)
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=5)

        self.plot_button = tk.Button(self.root, text="Plot Graph", command=self.plot_graph)
        self.plot_button.pack(pady=10)

        # Figure for matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.ax.grid(True)

        # Embed matplotlib figure into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.ball = None
        self.ani = None

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def preprocess_equation(self, equation):
        # Replace mathematical functions with their numpy equivalents
        replacements = {
            r"sin": "np.sin",
            r"cos": "np.cos",
            r"tan": "np.tan",
            r"log": "np.log",
            r"exp": "np.exp",
            r"sqrt": "np.sqrt",
            r"\^": "**"  # Replace ^ with ** for exponentiation
        }
        for pattern, replacement in replacements.items():
            equation = re.sub(pattern, replacement, equation)
        return equation

    def animate_ball(self, x, y):
        if self.ball is not None:
            self.ball.remove()  # Remove the previous ball

        self.ball, = self.ax.plot([x], [y], 'ro', label="Ball")  # Add the ball
        self.canvas.draw()

    def start_animation(self, x_vals, y_vals):
        def update(frame):
            self.animate_ball(x_vals[frame], y_vals[frame])

        if self.ani is not None:
            self.ani.event_source.stop()

        self.ani = animation.FuncAnimation(self.fig, update, frames=len(x_vals), interval=1, repeat=False)  # Faster interval

    def plot_graph(self):
        equation = self.entry.get()
        if not equation:
            messagebox.showerror("Error", "Please enter an equation to plot.")
            return

        try:
            # Preprocess the equation to handle complex expressions
            processed_equation = self.preprocess_equation(equation)

            # Prepare data for the plot
            x = np.linspace(-10, 10, 1000)  # Generate X values
            y = eval(processed_equation, {"x": x, "np": np})  # Safely evaluate the equation

            self.ax.clear()  # Clear previous plots
            self.ax.plot(x, y, label=equation)
            self.ax.set_title(f"{self.user_data['name']}'s Graph of y = " + equation)
            self.ax.legend()
            self.ax.grid(True)

            # Start the ball animation
            self.start_animation(x, y)

            self.canvas.draw()  # Redraw the canvas

        except Exception as e:
            messagebox.showerror("Error", f"Invalid equation: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGraphingCalculator(root)
    root.mainloop()
