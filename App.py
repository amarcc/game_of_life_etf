from tkinter import *
from StartScreen import StartScreen
from GameScreen import GameScreen
import random

from PIL import Image as PILImage, ImageTk

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title('Conway game of life')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.rows = random.randint(100, 150)
        self.columns = random.randint(100, 150)
        self.alive = random.randint(1, self.rows * self.columns - 1)

        file = PILImage.open("./boat.png")
        image = ImageTk.PhotoImage(file)
        self.root.iconphoto(True, image)

        self.StartScreen = StartScreen(self.root, self.to_GameScreen, self.set_values)

        self.GameScreen = GameScreen(self.root, self.rows, self.columns, self.alive, self.to_StartScreen)

        self.root.protocol("WM_DELETE_WINDOW", lambda root=self.root: self.GameScreen.on_closing(root)) 

    def set_values(self, rows, columns, alive):
        self.rows = rows
        self.columns = columns
        self.alive = alive     

    def run(self):
        self.StartScreen.grid(row = 0, column = 0, padx = 20, pady = 20)
        self.root.mainloop()

    def to_GameScreen(self):
        self.StartScreen.grid_forget()
        self.GameScreen.set_grid(self.rows, self.columns, self.alive)
        self.GameScreen.grid(row = 0, column = 0, padx = 20, pady = 20)

    def to_StartScreen(self):
        self.GameScreen.grid_forget()

        self.rows = random.randint(100, 150)
        self.columns = random.randint(100, 150)
        self.alive = random.randint(1, self.rows * self.columns - 1)

        self.StartScreen.rows.set(0)
        self.StartScreen.columns.set(0)
        self.StartScreen.num_of_alive.set(0)
        self.StartScreen.grid(row = 0, column = 0, padx = 20, pady = 20)

        
