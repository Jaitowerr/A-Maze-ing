class DSU():
    def __init__(self) -> None:
        self._parent: dict[tuple[int, int], tuple[int, int]] = {}

    def find(self, x: tuple[int, int]) -> tuple[int, int]:
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self._parent[rb] = ra
