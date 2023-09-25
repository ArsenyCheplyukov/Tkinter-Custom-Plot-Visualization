import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Graph Visualizer")

        self.filepath = ""
        self.data = None
        self.filter_mode = 1  # Default filter mode: Remove rows with "nan"

        # create menu
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.load_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)

        # make window resizable
        self.master.geometry("1600x800")
        self.master.resizable(True, True)

        # create buttons to select columns to plot
        self.buttons_x = []
        self.buttons_y = []

        # create a frame for the x-axis buttons and add a label
        self.button_row_x = tk.Frame(master)
        self.button_row_x_label = tk.Label(
            self.button_row_x, text="Select X-Axis:", bd=1, relief="solid", width=150, anchor="c"
        )
        self.button_row_x_label.pack(side="top", pady=(10, 5))
        self.button_row_x.pack(side="top", padx=10, pady=(0, 5))

        # create a frame for the y-axis buttons and add a label
        self.button_row_y = tk.Frame(master)
        self.button_row_y_label = tk.Label(
            self.button_row_y, text="Select Y-Axis:", bd=1, relief="solid", width=150, anchor="c"
        )
        self.button_row_y_label.pack(side="top", pady=(5, 10))
        self.button_row_y.pack(side="top", padx=10, pady=(0, 5))

        # create a frame for the check box
        self.check_box_frame = tk.Frame(master)
        self.check_box_frame.pack(side="top", padx=10, pady=(0, 5))

        # create plot button
        self.plot_button = tk.Button(master, text="Plot", command=self.plot_graph)
        self.plot_button.pack(side="top", pady=(10, 5))

        # create plot area
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

        # call create_buttons to generate the column selection buttons
        self.create_buttons()

    def create_buttons(self):
        # Read columns from data and create buttons to select which to plot
        if self.data is not None:
            columns = list(self.data.columns)
            num_cols = len(columns)

            # Create a canvas for the x-axis buttons
            x_canvas = tk.Canvas(self.button_row_x, height=50)
            x_canvas.pack(side="top", fill="x")
            x_scrollbar = tk.Scrollbar(self.button_row_x, orient="horizontal", command=x_canvas.xview)
            x_scrollbar.pack(side="top", fill="x")
            x_canvas.configure(xscrollcommand=x_scrollbar.set)

            # Create a frame to hold the x-axis buttons
            frame_x = tk.Frame(x_canvas)
            x_canvas.create_window((0, 0), window=frame_x, anchor="nw")

            # Create a canvas for the y-axis buttons
            y_canvas = tk.Canvas(self.button_row_y, height=50)
            y_canvas.pack(side="top", fill="x")
            y_scrollbar = tk.Scrollbar(self.button_row_y, orient="horizontal", command=y_canvas.xview)
            y_scrollbar.pack(side="top", fill="x")
            y_canvas.configure(xscrollcommand=y_scrollbar.set)

            # Create a frame to hold the y-axis buttons
            frame_y = tk.Frame(y_canvas)
            y_canvas.create_window((0, 0), window=frame_y, anchor="nw")

            for i in range(num_cols):
                column = columns[i]
                button_x = tk.Button(
                    frame_x,
                    text=column,
                    command=lambda col=column: self.select_button(col, "x"),
                )

                button_y = tk.Button(
                    frame_y,
                    text=column,
                    command=lambda col=column: self.select_button(col, "y"),
                )
                button_x.pack(side="left")
                button_y.pack(side="left")
                self.buttons_x.append(button_x)
                self.buttons_y.append(button_y)

            frame_x.update_idletasks()  # Update frame_x's dimensions
            frame_y.update_idletasks()  # Update frame_y's dimensions

            # Configure canvas scrolling regions
            x_canvas.configure(scrollregion=x_canvas.bbox("all"))
            y_canvas.configure(scrollregion=y_canvas.bbox("all"))

    def load_file(self):
        # open file dialog to select CSV file
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.filepath:
            # read data from file and update buttons
            self.data = pd.read_csv(
                self.filepath,
                index_col=False,
            )
            # Convert the first column to datetime
            self.data.iloc[:, 0] = pd.to_datetime(self.data.iloc[:, 0], errors="coerce")

            self.data.iloc[:, 1:] = self.data.iloc[:, 1:].apply(lambda x: pd.to_numeric(x, errors="coerce"))

            self.update_buttons()

    def update_buttons(self):
        # destroy old buttons and create new ones
        for button in self.buttons_x:
            button.destroy()
        for button in self.buttons_y:
            button.destroy()
        self.buttons_x = []
        self.buttons_y = []
        self.create_buttons()

    def select_button(self, column, keyword):
        # toggle button state
        if keyword == "x":
            for button in self.buttons_x:
                if button["text"] == column:
                    state = button["relief"]
                    if state == tk.RAISED:
                        button["relief"] = tk.SUNKEN
                        self.selected_x = column
                    else:
                        button["relief"] = tk.RAISED
                        self.selected_x = None
                else:
                    button["relief"] = tk.RAISED

        elif keyword == "y":
            for button in self.buttons_y:
                if button["text"] == column:
                    state = button["relief"]
                    if state == tk.RAISED:
                        button["relief"] = tk.SUNKEN
                        self.selected_y = column
                    else:
                        button["relief"] = tk.RAISED
                        self.selected_y = None
                else:
                    button["relief"] = tk.RAISED

    def plot_graph(self):
        # get selected columns and plot data
        selected_x = [button["text"] for button in self.buttons_x if button["relief"] == tk.SUNKEN]
        selected_y = [button["text"] for button in self.buttons_y if button["relief"] == tk.SUNKEN]

        if selected_x and selected_y:
            # check if selected columns exist in data
            plt.cla()
            self.ax.clear()

            x = self.data[selected_x[0]].values
            y = self.data[selected_y[0]].values

            valid_indices = pd.notnull(x) & pd.notnull(y)
            x = x[valid_indices]
            y = y[valid_indices]

            self.ax.plot(x, y)
            self.ax.set_xlabel(selected_x[0], fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.set_ylabel(selected_y[0], fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.set_title("Selected Columns", fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.grid(True)
            self.ax.tick_params(axis="both", grid_animated=True, which="major", labelsize=14)

            # Set a fixed number of points on the y-axis
            num_points = 10  # Adjust the desired number of points as needed
            self.ax.yaxis.set_major_locator(ticker.MaxNLocator(num_points))

            self.canvas.draw()

        else:
            messagebox.showerror("Error", "Please select at least one X-axis and one Y-axis column.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
