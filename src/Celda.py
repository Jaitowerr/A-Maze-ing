from .Direcccion import Direction


class Cell():
    def __init__(self,
                 west: int,
                 south: int,
                 east: int,
                 north: int,
                 is_42: bool) -> None:
        self.walls = {
            Direction.WEST: west,
            Direction.SOUTH: south,
            Direction.EAST: east,
            Direction.NORTH: north
        }
        self.is_42 = is_42

    def bin_to_hexa(self) -> str:
        """Convert binary wall flags to a single hexadecimal digit.

        Returns:
            A single hex character representing the four wall bits.
        """
        west = int(self.walls[Direction.WEST])
        south = int(self.walls[Direction.SOUTH])
        east = int(self.walls[Direction.EAST])
        north = int(self.walls[Direction.NORTH])

        value = west
        value = (value * 10) + south
        value = (value * 10) + east
        value = (value * 10) + north

        if value == 0:
            return "0"
        if value == 1:
            return "1"
        if value == 10:
            return "2"
        if value == 11:
            return "3"
        if value == 100:
            return "4"
        if value == 101:
            return "5"
        if value == 110:
            return "6"
        if value == 111:
            return "7"
        if value == 1000:
            return "8"
        if value == 1001:
            return "9"
        if value == 1010:
            return "A"
        if value == 1011:
            return "B"
        if value == 1100:
            return "C"
        if value == 1101:
            return "D"
        if value == 1110:
            return "E"
        if value == 1111:
            return "F"
        return "0"
