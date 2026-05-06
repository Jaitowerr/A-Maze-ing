class DSU():
    def __init__(self):
        self._parent = {}
    
    def find(self, x):
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]
    
    def union(self,a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self._parent[rb] = ra