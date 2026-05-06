class Player():
    def __init__(self, direction: tuple[int,int]):
        self._x, self._y = direction
    
    def set_x(self, num):
        self._x += num
    def set_y(self, num):
        self._y += num