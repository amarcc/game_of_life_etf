from tkinter import *
from tkinter import messagebox

class StartScreen(Frame):
    def __init__(self, parent, to_GameScreen, set_values):
        super().__init__(parent)
        
        self.to_GameScreen = to_GameScreen 
        self.set_values = set_values

        self.rows = IntVar()
        self.columns = IntVar()
        self.num_of_alive = IntVar()

        self.lab_rows = Label(self, text = 'Rows:')
        self.lab_rows.grid(row = 1, column = 0, sticky="e")

        self.enr_rows = Entry(self, textvariable = self.rows)
        self.enr_rows.grid(row = 1, column = 1)

        self.lab_columns = Label(self, text = 'Columns:')
        self.lab_columns.grid(row = 2, column = 0, sticky="e")

        self.enr_columns = Entry(self, textvariable = self.columns)
        self.enr_columns.grid(row = 2, column = 1)

        self.lab_num_of_alive = Label(self, text = 'Alive cells:')
        self.lab_num_of_alive.grid(row = 3, column = 0, sticky="e")

        self.enr_num_of_alive = Entry(self, textvariable = self.num_of_alive)
        self.enr_num_of_alive.grid(row = 3, column = 1)

        self.screen_btn = Button(self, text = 'Start')
        self.screen_btn.grid(row = 4, columnspan = 2, pady = (5, 0))
        self.screen_btn.configure(command = self.validate)

        self.rand_btn = Button(self, text = 'Randomize')
        self.rand_btn.grid(row = 5, columnspan = 2)
        self.rand_btn.configure(command = self.to_GameScreen)
        
    def validate(self):
        try:
            rows_number = self.rows.get()
            columns_number = self.columns.get()
            alive_number = self.num_of_alive.get()
        except:
            messagebox.showerror("Invalid input", "Please enter a number")
            return
        else:
            if(rows_number <= 0 or columns_number <= 0 or alive_number <= 0):
                messagebox.showerror("Invalid input", "Numbers of rows, columns and alive need to be bigger then 0")
                return
            elif alive_number >= (rows_number * columns_number):
                messagebox.showerror("Invalid input", "Numbers of alive needs to be less then product of rows and columns")
                return
            else:
                self.rows = rows_number
                self.columns = columns_number
                self.alive = alive_number

                self.set_values(self.rows, self.columns, self.alive)

                self.to_GameScreen()
