from mlx import Mlx

def main():
    try:
        m = Mlx()
        mlx = m.mlx_init()
        win = m.mlx_new_window(mlx, 400, 300, "test")
        m.mlx_string_put(mlx, win, 10,10,0xFFFFFF, "Hola")
        m.mlx_loop(mlx)
        print("ok")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()