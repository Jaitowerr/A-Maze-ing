class Player():
    def __init__(self, direction: tuple[int,int], img):
        self._x, self._y = direction
        self._img = img

    def render(self, m, win):
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img,self._x,self._y)