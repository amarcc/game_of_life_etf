class Cell:
    
    def __init__(self, x, y):
        self.year = 0
        self.state = 0
        self.x = x
        self.y = y

    def get_year(self):
        return self.year
    
    def get_state(self):
        return self.state
    
    def set_cell_year(self, year):
        if isinstance(year, int):
            self.year = year
        else:
            print('year is not instance of int')

    def set_state(self, state):
        if state == 0 or state == 1:
            self.state = state
        else:
            print('state can only be equal to 0 or 1')

    def add_1_year(self):
        self.year += 1

    def reset_year(self):
        self.year = 0
    