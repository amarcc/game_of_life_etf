from Cell import Cell
import random

class GameController:
    def __init__(self, rows, columns, alive, grid_canvas, curr_year, ovr_year, curr_gen, ovr_gen, end):
        self.rows = rows
        self.columns = columns
        self.alive = alive 
        self.grid_canvas =  grid_canvas

        self.rect_grid = []   
        self.cell_grid = []

        self.end = end

        self.future_alive = []
        self.future_dead = []
        
        self.curr_year = curr_year
        self.ovr_year = ovr_year

        self.curr_gen = curr_gen
        self.ovr_gen = ovr_gen

        self.load_scores()

        self.generation = 0
    
    def setup(self, rect_grid, rows = None, columns = None, alive = None):
        if(rows is not None):
            self.rows = rows

        if(columns is not None):
            self.columns = columns

        if(alive is not None):
            self.alive = alive

        self.rect_grid = rect_grid

        self.cell_grid = [[Cell(i, j) for j in range(columns)] for i in range(rows)]

        flattened = [cell for row in self.cell_grid for cell in row]

        random.shuffle(flattened)

        for cell in flattened[:self.alive]:
            self.change_color_state(cell.x, cell.y, "green", 1)

        
    def change_color_state(self, x, y, color, state):
        self.cell_grid[x][y].set_state(state)
        self.grid_canvas.itemconfig(self.rect_grid[x][y], fill=color)
                
    def automatic_change(self, x, y):
        if self.cell_grid[x][y].get_state() == 1:
            self.cell_grid[x][y].set_state(0)
            self.grid_canvas.itemconfig(self.rect_grid[x][y], fill='black')
        else:
            self.cell_grid[x][y].set_state(1)
            self.grid_canvas.itemconfig(self.rect_grid[x][y], fill='green')

    def check_cell(self, x, y):
        nb = 0

        try:
            check = self.cell_grid[x + 1][y].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x + 1][y - 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x + 1][y + 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x][y - 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x][y + 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x - 1][y].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x - 1][y - 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        try:
            check = self.cell_grid[x - 1][y + 1].get_state()
        except:
            pass
        else:
            if check == 1:
                nb += 1

        cell = self.cell_grid[x][y]

        if cell.get_state() == 1:
            if nb == 2 or nb == 3:
                self.future_alive.append(cell)
            else:
                self.future_dead.append(cell)
        else:
            if nb == 3:
                self.future_alive.append(cell)
            else:
                self.future_dead.append(cell)


    def run(self, w):
        for i in range(self.rows):
            for j in range(self.columns):
                self.check_cell(i, j)

        self.apply_update()

        if(len(self.future_alive) > 0):
            self.generation += 1
            self.curr_gen.set(self.generation)
            if(self.ovr_gen.get() < self.generation):
                self.ovr_gen.set(self.generation)
        else:
            self.generation = 0
            self.curr_gen.set(self.generation)

        self.future_alive = []
        self.future_dead = []
        
        if self.end.get() != 1:
            w.after(500, lambda w=w: self.run(w))
        else:
            self.generation = 0
            self.curr_gen.set(self.generation)
            self.curr_year.set(0)


    def apply_update(self):
        for cell in self.future_alive:
            cell.add_1_year()

            if(self.curr_year.get() < cell.get_year()):
                self.curr_year.set(cell.get_year())

            if(self.ovr_year.get() < cell.get_year()):
                self.ovr_year.set(cell.get_year())

            self.change_color_state(cell.x, cell.y, "green", 1)
        
        for cell in self.future_dead:
            cell.reset_year()
            self.change_color_state(cell.x, cell.y, "black", 0)
    
    def load_scores(self):
        try:
            data = [line.strip() for line in open('./scores.dat')]
        except:
            pass
        else:
            self.ovr_year.set(int(data[0]))
            self.ovr_gen.set(int(data[1]))
            


        

            








