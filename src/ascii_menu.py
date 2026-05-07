def ascii_menu(gen):
    print("\n--- MENÚ ---")
    print("  1. Re-generate a new maze and display it")
    print("  2. Show/Hide shortest path")
    print("  3. Change maze wall colours")
    print("  4. Set colours for the '42' pattern")
    print("  q. Quit")

    while True:
        try:
            opcion = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            return False

        if opcion == 'q':
            print("Saliendo...")
            return False
        elif opcion == '1':
            pass
        elif opcion == '2':
            pass
        elif opcion == '3':
            pass
        elif opcion == '4':
            pass
        else:
            print("Opción no válida. Usa 1, 2, 3, 4 o q.")
