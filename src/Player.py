class Player():
    def __init__(self, direction: tuple[int,int], img):
        self._x, self._y = direction
        self._img = img

    def render(self, m, win):
        px = self._x * 40 + 14
        py = self._y * 40 + 14
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img,px,py)
    