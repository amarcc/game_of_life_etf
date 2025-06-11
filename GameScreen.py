from tkinter import *
from GameController import GameController

class GameScreen(Frame):
    def __init__(self, parent, rows, columns, alive, to_StartScreen):
        super().__init__(parent)
        
        self.ovr_year = IntVar(value = 0)
        self.curr_year = IntVar(value = 0)
        self.ovr_gen = IntVar(value = 0)
        self.curr_gen = IntVar(value = 0)

        self.rows = rows
        self.columns = columns
        self.alive = alive
        self.end = IntVar(value = 0)

        self.to_StartScreen = to_StartScreen


        self.lab_curr_year = Label(self, text = "Current Oldest Cell:")
        self.lab_curr_year.grid(row = 0, column = 0, sticky = "e", pady=(0, 5))

        self.curr_year_lab = Label(self, text = "0", textvariable = self.curr_year)
        self.curr_year_lab.grid(row = 0, column = 1, sticky = "w" ,pady = (0, 5))

        self.lab_ovr_year = Label(self, text = "Overall Oldest Cell:")
        self.lab_ovr_year.grid(row = 0, column = 2, sticky = "e" , pady = (0, 5))

        self.ovr_year_lab = Label(self, text = "0", textvariable = self.ovr_year)
        self.ovr_year_lab.grid(row = 0, column = 3, sticky="w", pady = (0, 5))

        self.frame_row1 = Frame(self)
        self.frame_row1.grid(row = 1, columnspan = 4, pady = (0, 5))

        self.lab_gen_year = Label(self.frame_row1, text = "Overall Oldest Generation:", anchor='e')
        self.lab_gen_year.grid(row = 0, column = 0)

        self.gen_year_lab = Label(self.frame_row1, text = "0", anchor='w', textvariable = self.ovr_gen)
        self.gen_year_lab.grid(row = 0, column = 1)

        self.frame_canvas = Frame(self)
        self.frame_canvas.grid(row = 2, columnspan = 4, sticky='nswe')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        v_scrollbar = Scrollbar(self.frame_canvas, orient=VERTICAL)
        v_scrollbar.grid(row=0, column=1, sticky='ns')

        h_scrollbar = Scrollbar(self.frame_canvas, orient=HORIZONTAL)
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.grid_canvas = Canvas(self.frame_canvas, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set, bg = "black")
        
        v_scrollbar.config(command=self.grid_canvas.yview)
        h_scrollbar.config(command=self.grid_canvas.xview)

        self.grid_canvas.grid(row = 0, column = 0, sticky='nsew')

        self.frame_row3 = Frame(self)
        self.frame_row3.grid(row = 3, columnspan = 4, pady = (0, 5))

        self.lab_curr_gen = Label(self.frame_row3, text = 'Generation:')
        self.lab_curr_gen.grid(row = 0, column = 0)

        self.curr_gen_lab = Label(self.frame_row3, text = '0', textvariable = self.curr_gen)
        self.curr_gen_lab.grid(row = 0, column = 1)

        self.play_btn = Button(self, text='Play', command=self.play)
        self.play_btn.grid(row = 4, column = 0, columnspan = 2, padx = (0, 5), pady = (0, 5), sticky="e")

        self.back_btn = Button(self, text = "Go back", command = self.back)
        self.back_btn.grid(row = 4, column = 2, columnspan = 2, padx = (5, 0), pady = (0, 5), sticky = "w")

        self.GameController = GameController(self.rows, self.columns, self.alive, self.grid_canvas, self.curr_year, self.ovr_year, self.curr_gen, self.ovr_gen, self.end)

        self.grid_canvas.bind("<MouseWheel>", self.on_zoom)
        self.grid_canvas.bind("<Button-1>", self.on_click)

    def back(self):
        self.end.set(1)
        self.to_StartScreen()

    def set_rows(self, rows):
        self.rows = rows
        return

    def on_zoom(self, event):
        if event.delta > 0:
            factor = 1.1
        elif event.delta < 0:
            factor = 0.9
        else:
            factor = 1

        x = self.grid_canvas.canvasx(event.x)
        y = self.grid_canvas.canvasy(event.y)

        self.grid_canvas.scale("all", x, y, factor, factor)

        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))

    def set_cols(self, columns):
        self.columns = columns
        return
    
    def set_alive(self, alive):
        self.alive = alive
        return
    
    def set_grid(self, rows, columns, alive):
        self.rows = rows
        self.columns = columns
        self.alive = alive

        self.grid_canvas.delete("all")

        self.rectangles = [[None for j in range(columns)] for i in range(rows)]
        
        x_start = 0
        y_start = 0

        CELL_WIDTH = 10

        PADDING = 1

        for i in range(rows):
            x_start = 0
            for j in range(columns):
                self.rectangles[i][j] = self.grid_canvas.create_rectangle(x_start, y_start, x_start + CELL_WIDTH, y_start + CELL_WIDTH, fill="black", width=0)
                x_start += 10 + PADDING
                
            y_start += 10 + PADDING

        end_x_scroll = self.columns * CELL_WIDTH + (self.columns + 1) * PADDING
        end_y_scroll = self.rows * CELL_WIDTH + (self.rows + 1) * PADDING

        self.grid_canvas.config(scrollregion=(0, 0, end_x_scroll, end_y_scroll))

        self.GameController.setup(self.rectangles, self.rows, self.columns, self.alive)

        return
    
    def play(self):
        self.end.set(0)
        self.GameController.run(self)
    
    def on_click(self, event):
        x = self.grid_canvas.canvasx(event.x)
        y = self.grid_canvas.canvasy(event.y)
        clicked_rect = self.grid_canvas.find_closest(x, y)
        if clicked_rect:
            rect = clicked_rect[0]
            coords = [(i, j) for i in range(self.rows) for j in range (self.columns) if self.rectangles[i][j] == rect]
            self.GameController.automatic_change(coords[0][0], coords[0][1])

    def on_closing(self, root):
        f = open('./scores.dat', 'w')
        f.write(f'{self.ovr_year.get()}\n{self.ovr_gen.get()}')
        root.destroy()
                