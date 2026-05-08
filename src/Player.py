class Player():
    def __init__(self, direction: tuple[int,int], img):
        self._x, self._y = direction
        self._img = img

    def render(self, m, win):
        m.mlx_put_image_to_window(m.mlx_ptr, win, self._img,self._x,self._y)
    
    def render_player():

        
        redraw_tile_under_player()

        
        mlx_put_image_to_window(player)

    def redraw_tile(self, x, y):

        TILE = 40

        cell = self.maze.get_cell(x, y)

        key = self.maze.get_tile_key(cell)

        tile = self.tiles[key]

        px = x * TILE
        py = y * TILE

        self.m.mlx_put_image_to_window(
            self.mlx,
            self.win,
            tile,
            px,
            py
        )
    def draw_player(self):

        px = self.player_x * 40
        py = self.player_y * 40

        self.m.mlx_put_image_to_window(
            self.mlx,
            self.win,
            self.player_img,
            px,
            py
        )
    def move_player(self, dx, dy):

        old_x = self.player_x
        old_y = self.player_y

        new_x = old_x + dx
        new_y = old_y + dy

        if not self.can_move(new_x, new_y):
            return

        # RESTAURAR TILE ANTIGUO
        self.redraw_tile(old_x, old_y)

        # mover player
        self.player_x = new_x
        self.player_y = new_y

        # dibujar player nuevo
        self.draw_player()