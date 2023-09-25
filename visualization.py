import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphApp:
    def __init__(self, master):
        self.master = master
        master.title("Graph Visualizer")

        self.filepath = ""
        self.data = None

        # create menu
        menubar = tk.Menu(master, font=("Times New Roman", 14))
        filemenu = tk.Menu(menubar, tearoff=0, font=("Times New Roman", 14))
        filemenu.add_command(
            label="Open",
            command=self.load_file,
            font=("Times New Roman", 14),
        )
        filemenu.add_separator()
        filemenu.add_command(
            label="Exit",
            command=master.quit,
            font=("Times New Roman", 14),
        )
        menubar.add_cascade(label="File", menu=filemenu, font=("Times New Roman", 14))
        master.config(menu=menubar)
        master.config(menu=menubar)

        # make window resizable
        self.master.geometry("1600x600")
        self.master.resizable(True, True)

        # create a frame for the check box
        self.check_box_frame = tk.Frame(master)
        self.check_box_frame.pack(side="top")

        # # create the check button with default value "int"
        # self.first_col_check = tk.StringVar(value="yes")
        # self.check_button = tk.Checkbutton(
        #     self.check_box_frame,
        #     text="First column data type is time:",
        #     font=("Times New Roman", 14),
        #     anchor="c",
        #     variable=self.first_col_check,
        #     onvalue="yes",
        #     offvalue="no",
        # )
        # self.check_button.pack(side="left")

        # create buttons to select columns to plot
        self.buttons_x = []
        self.buttons_y = []
        # create a frame for the x-axis buttons and add a label
        self.button_row_x = tk.Frame(master)
        self.button_row_x_label = tk.Label(
            master,
            text="Select X-Axis:",
            font=("Times New Roman", 14),
            bd=1,
            relief="solid",
            width=20,
            anchor="c",
        )
        self.button_row_x_label.pack(side="top")
        self.button_row_x.pack(side="top")

        # create a frame for the y-axis buttons and add a label
        self.button_row_y = tk.Frame(master)
        self.button_row_y_label = tk.Label(
            master,
            text="Select Y-Axis:",
            font=("Times New Roman", 14),
            bd=1,
            relief="solid",
            width=20,
            anchor="c",
        )
        self.button_row_y_label.pack(side="top")
        self.button_row_y.pack(side="top")

        # create plot button
        self.plot_button = tk.Button(master, text="Plot", font=("Times New Roman", 14), command=self.plot_graph)
        self.plot_button.pack(side="top")

        # create plot area
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)

    def create_buttons(self):
        # read columns from data and create buttons to select which to plot
        if self.data is not None:
            columns = list(self.data.columns)
            num_cols = len(columns)
            row_x = tk.Frame(self.button_row_x)
            row_x.pack(side="left")
            row_y = tk.Frame(self.button_row_y)
            row_y.pack(side="left")
            for i in range(num_cols):
                column = columns[i]
                button_x = tk.Button(
                    row_x,
                    text=column,
                    command=lambda col=column: self.select_button(col, "x"),
                )

                button_y = tk.Button(
                    row_y,
                    text=column,
                    command=lambda col=column: self.select_button(col, "y"),
                )
                button_x.pack(side="left")
                button_y.pack(side="left")
                self.buttons_x.append(button_x)
                self.buttons_y.append(button_y)
            # set button font and alignment
            for button in self.buttons_x + self.buttons_y:
                button.config(font=("Times New Roman", 12), justify="center")

    def load_file(self):
        # open file dialog to select CSV file
        self.filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.filepath:
            # read data from file and update buttons
            self.data = pd.read_csv(self.filepath, index_col=False)
            self.data.iloc[:, 0] = pd.to_datetime(self.data.iloc[:, 0])

            # # calculate the minimum datetime value
            # min_datetime = self.data.iloc[:, 0].min()

            # # subtract the minimum datetime from the entire column and convert to seconds
            # self.data.iloc[:, 0] = (self.data.iloc[:, 0] - min_datetime).astype(
            #     "float64"
            # )
            # print(self.data.iloc[:, 0].values)
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
        # set button font and alignment
        for button in self.buttons_x + self.buttons_y:
            button.config(font=("Times New Roman", 12), justify="center")

    def plot_graph(self):
        # get selected columns and plot data
        selected_x = [button["text"] for button in self.buttons_x if button["relief"] == tk.SUNKEN]
        selected_y = [button["text"] for button in self.buttons_y if button["relief"] == tk.SUNKEN]

        if selected_x and selected_y:
            # check if selected columns exist in data
            plt.cla()
            self.ax.clear()
            self.data.plot(x=selected_x[0], y=selected_y[0], ax=self.ax)
            self.ax.set_xlabel(selected_x[0], fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.set_ylabel(selected_y[0], fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.set_title("Selected Columns", fontname="Times New Roman", fontsize=14, ha="center")
            self.ax.grid(True)
            self.ax.tick_params(axis="both", grid_animated=True, which="major", labelsize=14)

            # NavigationToolbar2Tk(self.ax, self.master)

            self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
