import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.probability_calculator import calculate_total_probability, global_precision
from fractions import Fraction
import numpy as np
from decimal import Decimal, getcontext

getcontext().prec = 100

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

def calculate_and_display_total_probability():
    getcontext().prec = global_precision
    var_values = {var: float(value) for var, value in variables.items()}
    try:
        # Convert variables to Decimal before calculation to maintain precision
        var_values_decimal = {var: Decimal(value) for var, value in var_values.items()}
        P_t = calculate_total_probability(probability_factors, var_values_decimal)
        representation = representation_var.get()

        if P_t.is_infinite() or P_t.is_nan():
            result_var.set("Total Probability P(t): Numerical result out of range")
        else:
            if representation == "Decimal":
                # Format the Decimal to remove scientific notation using the 'f' formatter
                # Adjust the number after '.:' to the desired number of decimal places
                format_string = f"{{:.{global_precision}f}}"
                result_var.set(f"Total Probability P(t): {format_string.format(P_t)}")
            elif representation == "Fraction":
                # Convert the Decimal to a string first to avoid overflow in Fraction
                fraction_result = Fraction(str(P_t))
                result_var.set(f"Total Probability P(t): {fraction_result}")
            elif representation == "Percentage":
                # Format the percentage result to remove scientific notation and trailing zeros
                # and display it with the desired precision
                percentage_result = (P_t * Decimal(100)).quantize(Decimal('1.' + '0' * global_precision))
                # Use 'normalize' to remove trailing zeros
                percentage_result = percentage_result.normalize()
                result_var.set(f"Total Probability P(t): {percentage_result}%")
            else:
                result_var.set("Unknown representation type.")
    except Exception as e:
        result_var.set(f"Error: {e}")


def update_precision(precision_entry,event=None):  # Optional event parameter for the binding.
    global global_precision
    try:
        # Get the new precision value from the entry box.
        new_precision = int(precision_entry.get())
        # Update the global precision if it has changed.
        if new_precision != global_precision:
            global_precision = new_precision
            getcontext().prec = global_precision  # Update the context with the new precision.
            calculate_and_display_total_probability()  # Recalculate the total probability.
    except ValueError:
        # If the new precision value is not an integer, show an error but do not stop the program.
        messagebox.showerror("Error", "Please enter a valid integer for precision.")


def clear_calculator():
    if messagebox.askyesno("Clear", "Are you sure you want to clear?"):
        probability_factors.clear()
        variables.clear()
        factors_listbox.delete(0, tk.END)
        variables_listbox.delete(0, tk.END)
        x_entry.delete(0, tk.END)
        N_entry.delete(0, tk.END)
        variable_name_entry.delete(0, tk.END)
        variable_value_entry.delete(0, tk.END)
        result_var.set("")

def start_gui():
    global probability_factors, variables, x_entry, N_entry, variable_name_entry, variable_value_entry, factors_listbox, variables_listbox, result_var, representation_var
    
    root = tk.Tk()
    root.title("Probability Calculator")
    
    # Configure the root grid to expand the second column and the listboxes' rows
    root.columnconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)
    root.rowconfigure(9, weight=1)

    # Initialize the list of probability factors and variables
    probability_factors = []
    variables = {}

    # Create GUI elements
    x_label = ttk.Label(root, text="x (can be an expression):")
    x_label.grid(column=0, row=0, sticky=(tk.W, tk.E))
    x_entry = ttk.Entry(root)
    x_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    N_label = ttk.Label(root, text="N (can be an expression):")
    N_label.grid(column=0, row=1, sticky=(tk.W, tk.E))
    N_entry = ttk.Entry(root)
    N_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    add_button = ttk.Button(root, text="Add Probability Factor", command=add_probability_factor)
    add_button.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    factors_label = ttk.Label(root, text="Probability Factors:")
    factors_label.grid(column=0, row=3, sticky=(tk.W, tk.E))
    factors_listbox = tk.Listbox(root)
    factors_listbox.grid(column=0, row=4, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    variable_name_label = ttk.Label(root, text="Variable Name:")
    variable_name_label.grid(column=0, row=5, sticky=(tk.W, tk.E))
    variable_name_entry = ttk.Entry(root)
    variable_name_entry.grid(column=1, row=5, sticky=(tk.W, tk.E), padx=5, pady=5)

    variable_value_label = ttk.Label(root, text="Variable Value:")
    variable_value_label.grid(column=0, row=6, sticky=(tk.W, tk.E))
    variable_value_entry = ttk.Entry(root)
    variable_value_entry.grid(column=1, row=6, sticky=(tk.W, tk.E), padx=5, pady=5)

    add_variable_button = ttk.Button(root, text="Add Variable", command=add_variable)
    add_variable_button.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    variables_label = ttk.Label(root, text="Variables:")
    variables_label.grid(column=0, row=8, sticky=(tk.W, tk.E))
    variables_listbox = tk.Listbox(root)
    variables_listbox.grid(column=0, row=9, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

    result_var = tk.StringVar()
    result_label = ttk.Label(root, textvariable=result_var)
    result_label.grid(column=0, row=10, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    # Dropdown for result representation
    representation_var = tk.StringVar()
    representation_combobox = ttk.Combobox(root, textvariable=representation_var, 
                                           values=("Decimal", "Fraction", "Percentage"))
    representation_combobox.grid(column=0, row=11, sticky=(tk.W, tk.E), padx=5, pady=5)
    representation_combobox.set("Percentage")  # Set default value to "Percentage"

    calculate_button = ttk.Button(root, text="Calculate Total Probability", command=calculate_and_display_total_probability)
    calculate_button.grid(column=0, row=12, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    clear_button = ttk.Button(root, text="Clear", command=clear_calculator)
    clear_button.grid(column=0, row=13, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

    # Add a label and entry for precision input
    precision_var = tk.StringVar(value="100")  # Using a StringVar with a default value of "100"
    precision_entry = ttk.Entry(root, textvariable=precision_var)
    precision_label = ttk.Label(root, text="Precision (number of decimals):")
    precision_label.grid(column=0, row=14, sticky=(tk.W, tk.E))
    precision_entry.grid(column=1, row=14, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    # Use trace_add instead of trace to call update_precision with precision_entry as an argument
    def on_precision_change(*args):
        update_precision(precision_entry)
    
    precision_var.trace_add("write", on_precision_change)

    # Start the GUI event loop
    root.mainloop()
