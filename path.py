class Path:
    NONE_VALUE = "NONEVALUE"

    def __init__(self, start_coo):
        self.path = {start_coo: self.NONE_VALUE}
        self.start_coo = start_coo
        self.last_coo = start_coo
        self.testmode = False

    def add(self, coo):
        # assert self.is_valid()
        if self.path.get(coo):
            to_delete = self.last_coo
            while to_delete != coo:
                to_delete = self.backtrack()
        else:
            self.path[coo] = self.last_coo
        self.last_coo = coo
        if self.testmode:
            print(self)
            print(self.path)
        # assert self.path.get(self.last_coo)
        # assert self.path.get(self.start_coo)
        # assert self.is_valid()

    def backtrack(self):
        to_delete = self.last_coo
        if self.path[to_delete] == self.NONE_VALUE:
            return self.NONE_VALUE
        self.last_coo = self.path[to_delete]
        # assert self.last_coo != self.NONE_VALUE
        if not self.path.get(self.last_coo):
            return self.NONE_VALUE
        del self.path[to_delete]
        # assert self.path.get(self.last_coo)
        # assert self.path.get(self.start_coo)
        # assert self.is_valid()
        return self.last_coo

    def follow(self):
        self.last_coo = self.path[self.last_coo]
        # assert self.last_coo != self.NONE_VALUE
        # assert self.path.get(self.last_coo)
        # assert self.path.get(self.start_coo)
        return self.last_coo

    def reverse(self):
        # assert self.is_valid()
        reverse_path = Path(self.last_coo)
        reverse_path.path = {
            val: key for key, val in self.path.items() if not val == self.NONE_VALUE
        }
        reverse_path.last_coo = self.start_coo
        # assert reverse_path.last_coo != self.NONE_VALUE
        if self.testmode:
            print(reverse_path)
            print(reverse_path.path)
        reverse_path.path[self.last_coo] = self.NONE_VALUE
        # assert reverse_path.path.get(self.last_coo)
        # if not reverse_path.path.get(self.start_coo):
        #    assert False
        # assert reverse_path.path.get(self.start_coo)
        # if reverse_path.start_coo != self.last_coo:
        #    assert False
        # if reverse_path.last_coo != self.start_coo:
        #    assert False
        # assert reverse_path.is_valid()
        return reverse_path

    def __str__(self):
        coo = self.last_coo
        res = str(coo)
        while self.path.get(coo):
            coo = self.path[coo]
            res = str(coo) + " <-- " + res
        return res

    def __len__(self):
        return len(self.path.keys())

    # def is_valid(self):
    #     if not self.last_coo or self.last_coo==self.NONE_VALUE:
    #         return False
    #     if not self.start_coo or self.start_coo==self.NONE_VALUE:
    #         return False
    #     p = self.path
    #     v = p[self.last_coo]
    #     counter = 1
    #     while v != self.NONE_VALUE:
    #         counter +=1
    #         v = p.get(v)
    #         if not v:
    #             return False
    #     if counter != len( p ):
    #         return False
    #     return True


if __name__ == "__main__":
    # Tests
    p = Path("A")
    p.testmode = True
    p.add("B")
    p.add("C")
    p.add("D")
    p.add("B")
    p.add("E")
    p.add("E")
    p.add("F")
    p.add("A")
    p.add("B")
    p.add("C")
    p.add("D")
    p.add("B")
    p.add("E")
    p.add("E")
    p.add("F")
    q = p.reverse()
    assert q.reverse().path == p.path
    assert q.reverse().start_coo == p.start_coo
    assert q.reverse().last_coo == p.last_coo
