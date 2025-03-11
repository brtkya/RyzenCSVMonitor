import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    
    try:
        df = pd.read_csv(file_path)
        update_table(df)
    except Exception as e:
        print(f"Error: {e}")  

def update_table(df):
    table.delete(*table.get_children())  
    table["columns"] = list(df.columns)
    table["show"] = "headings"
    
    for column in df.columns:
        table.heading(column, text=column, command=lambda c=column: show_column_info(c, df))
        table.column(column, width=150)  
    
    for _, row in df.iterrows():
        table.insert("", "end", values=list(row))

def show_column_info(column, df):
    if pd.api.types.is_numeric_dtype(df[column]):
        max_value = df[column].max()
        min_value = df[column].min()
        mean_value = df[column].mean()
        
        create_graph(df, column, max_value, min_value, mean_value)

def create_graph(df, column, max_value, min_value, mean_value):
    graph_window = tk.Toplevel(main_window)
    graph_window.title(f"{column} Graph")

    screen_width = graph_window.winfo_screenwidth()
    screen_height = graph_window.winfo_screenheight()

    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    graph_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    fig, ax = plt.subplots(figsize=(window_width / 80, window_height / 110))  

    ax.plot(df[column], marker='o', linestyle='-', color='b', label=column)
    ax.set_title(f"{column} Graph", fontsize=16)
    ax.set_xlabel("Index", fontsize=14)
    ax.set_ylabel(column, fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    bottom_frame = tk.Frame(graph_window)
    bottom_frame.pack(pady=10, fill="x")

    info_label = tk.Label(bottom_frame, text=f"Max: {max_value}   Min: {min_value}   Mean: {mean_value:.2f}",
                              font=("Arial", 12), pady=5)
    info_label.pack()

main_window = tk.Tk()
main_window.title("CSV Viewer")
main_window.state('zoomed')

upper_frame = tk.Frame(main_window)
upper_frame.pack(pady=10)

load_button = tk.Button(upper_frame, text="Load CSV", command=load_csv)
load_button.pack()

instructions_label = tk.Label(upper_frame, text="Click 'Load CSV' to select a CSV file. Column headers are displayed as table headings. Click a column header to generate a graph.", font=("Arial", 10), pady=5,fg="blue")
instructions_label.pack()

table_frame = tk.Frame(main_window)
table_frame.pack(expand=True, fill="both")

table = ttk.Treeview(table_frame)
table.pack(expand=True, fill="both")

main_window.mainloop()
