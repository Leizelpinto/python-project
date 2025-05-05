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
        self.root.configure(bg="#f0f8ff")  # Light blue background

        # Data store for user information
        self.user_data = {}

        # Initial menu screen
        self.menu_screen()

    def menu_screen(self):
        self.clear_root()

        # Welcome message and instructions
        tk.Label(self.root, text="Welcome to the Graphing Calculator!", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)
        tk.Label(self.root, text="Please choose an option below.", font=("Arial", 12), bg="#f0f8ff").pack(pady=10)

        # Button for Sign In
        tk.Button(self.root, text="Sign In", width=20, height=2, bg="#4caf50", fg="white", command=self.signin_screen).pack(pady=10)

        # Button for Exit
        tk.Button(self.root, text="Exit", width=20, height=2, bg="#f44336", fg="white", command=self.root.quit).pack(pady=10)

    def signin_screen(self):
        self.clear_root()

        # Motivational message
        tk.Label(self.root, text="Welcome! Let's get started.", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.root, text="Enter your details to explore the beauty of graphs!", font=("Arial", 12), bg="#f0f8ff").pack(pady=10)

        # Name input
        tk.Label(self.root, text="Enter your name:", bg="#f0f8ff").pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        # Email input
        tk.Label(self.root, text="Enter your email:", bg="#f0f8ff").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=40)
        self.email_entry.pack(pady=5)

        # Favorite color input
        tk.Label(self.root, text="What's your favorite color (e.g., 'red', 'blue')?", bg="#f0f8ff").pack(pady=5)
        self.color_entry = tk.Entry(self.root, width=40)
        self.color_entry.pack(pady=5)

        # Continue button
        tk.Button(self.root, text="Continue", bg="#4caf50", fg="white", command=self.open_graph_screen).pack(pady=15)

    def validate_email(self, email):
        """Validate email format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    def open_graph_screen(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        favorite_color = self.color_entry.get().strip()

        if not name or not email or not favorite_color:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address (e.g., example@gmail.com).")
            return

        self.user_data["name"] = name
        self.user_data["email"] = email
        self.user_data["favorite_color"] = favorite_color

        self.clear_root()

        # Display a welcome message in the graph window
        tk.Label(self.root, text=f"Welcome, {self.user_data['name']}!", font=("Arial", 14, "bold"), bg="#f0f8ff", fg=favorite_color).pack(pady=10)
        tk.Label(self.root, text="Enter an equation in terms of x (e.g., x**2 + 2*x - 1):", bg="#f0f8ff").pack(pady=5)

        # Input for the equation
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=5)

        # Buttons for graph actions
        tk.Button(self.root, text="Plot Graph", bg=favorite_color, fg="white", command=self.plot_graph).pack(pady=10)
        tk.Button(self.root, text="Clear Previous Graph", bg="#ff9800", fg="white", command=self.clear_graph).pack(pady=10)

        # Exit button
        tk.Button(self.root, text="Exit", bg="#f44336", fg="white", command=self.root.destroy).pack(pady=10)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.ax.grid(True)

        # Embed the figure into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.ball = None
        self.ani = None

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_graph(self):
        if hasattr(self, 'ax') and self.ax:
            self.ax.clear()  # Clear the graph
            self.ax.grid(True)  # Reset the grid
            self.canvas.draw()  # Redraw the canvas

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
        favorite_color = self.user_data.get("favorite_color", "blue")  # Default to blue if no color

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
            self.ax.plot(x, y, label=equation, color=favorite_color)  # Use favorite color for plot line
            self.ax.set_title(f"{self.user_data['name']}'s Graph of y = " + equation, color=favorite_color)
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
