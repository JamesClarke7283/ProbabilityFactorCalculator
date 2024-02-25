import tkinter as tk
from tkinter import ttk
from src.probability_calculator import calculate_total_probability

# Function to add a probability factor with x and N as expressions
def add_probability_factor():
    x_expr = x_entry.get()  # x is now an expression
    N_expr = N_entry.get()  # N is an expression too
    probability_factors.append((x_expr, N_expr))
    factors_listbox.insert(tk.END, f"x={x_expr}, N={N_expr}")
    x_entry.delete(0, tk.END)
    N_entry.delete(0, tk.END)

# Function to add a variable with its name and value
def add_variable():
    var_name = variable_name_entry.get()
    var_value = variable_value_entry.get()
    variables[var_name] = var_value
    variables_listbox.insert(tk.END, f"{var_name} = {var_value}")
    variable_name_entry.delete(0, tk.END)
    variable_value_entry.delete(0, tk.END)

# Function to calculate and display the total probability
def calculate_and_display_total_probability():
    # Create a dictionary of variables and their values
    var_values = {var: float(value) for var, value in variables.items()}
    try:
        P_t = calculate_total_probability(probability_factors, var_values)
        if percentage_var.get():
            P_t *= 100
            result_var.set(f"Total Probability P(t): {P_t:.4f}%")
        else:
            result_var.set(f"Total Probability P(t): {P_t}")
    except Exception as e:
        result_var.set(f"Error: {e}")

def start_gui():
    # Initialize the main GUI window
    root = tk.Tk()
    root.title("Probability Calculator")

    # Initialize the list of probability factors and variables
    probability_factors = []
    variables = {}

    # Create the GUI layout
    x_label = ttk.Label(root, text="x (can be an expression):")
    x_label.grid(column=0, row=0, sticky=tk.W)
    x_entry = ttk.Entry(root)
    x_entry.grid(column=1, row=0, sticky=tk.EW)

    N_label = ttk.Label(root, text="N (can be an expression):")
    N_label.grid(column=0, row=1, sticky=tk.W)
    N_entry = ttk.Entry(root)
    N_entry.grid(column=1, row=1, sticky=tk.EW)

    add_button = ttk.Button(root, text="Add Probability Factor", command=add_probability_factor)
    add_button.grid(column=0, row=2, columnspan=2, sticky=tk.EW)

    factors_label = ttk.Label(root, text="Probability Factors:")
    factors_label.grid(column=0, row=3, sticky=tk.W)
    factors_listbox = tk.Listbox(root)
    factors_listbox.grid(column=0, row=4, columnspan=2, sticky=tk.EW)

    variable_name_label = ttk.Label(root, text="Variable Name:")
    variable_name_label.grid(column=0, row=5, sticky=tk.W)
    variable_name_entry = ttk.Entry(root)
    variable_name_entry.grid(column=1, row=5, sticky=tk.EW)

    variable_value_label = ttk.Label(root, text="Variable Value:")
    variable_value_label.grid(column=0, row=6, sticky=tk.W)
    variable_value_entry = ttk.Entry(root)
    variable_value_entry.grid(column=1, row=6, sticky=tk.EW)

    add_variable_button = ttk.Button(root, text="Add Variable", command=add_variable)
    add_variable_button.grid(column=0, row=7, columnspan=2, sticky=tk.EW)

    variables_label = ttk.Label(root, text="Variables:")
    variables_label.grid(column=0, row=8, sticky=tk.W)
    variables_listbox = tk.Listbox(root)
    variables_listbox.grid(column=0, row=9, columnspan=2, sticky=tk.EW)

    result_var = tk.StringVar()
    result_label = ttk.Label(root, textvariable=result_var)
    result_label.grid(column=0, row=12, columnspan=2, sticky=tk.EW)

    percentage_var = tk.BooleanVar()
    percentage_check = ttk.Checkbutton(root, text="Display as percentage", variable=percentage_var)
    percentage_check.grid(column=0, row=10, sticky=tk.W)

    calculate_button = ttk.Button(root, text="Calculate Total Probability", command=calculate_and_display_total_probability)
    calculate_button.grid(column=0, row=11, columnspan=2, sticky=tk.EW)

    root.mainloop()
