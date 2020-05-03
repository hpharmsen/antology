

class Path():
    NONE_VALUE = 'NONEVALUE'

    def __init__(self, start_coo):
        self.path = {start_coo:self.NONE_VALUE}
        self.last_coo = start_coo
        self.testmode = False

    def add(self, coo):
        if self.path.get(coo):
            to_delete = self.last_coo
            while to_delete != coo:
                to_delete = self.backtrack()
        else:
            self.path[coo] = self.last_coo
        self.last_coo = coo
        if self.testmode:
            print( self )
            print( self.path )

    def __str__(self):
        coo = self.last_coo
        res = str(coo)
        while self.path.get(coo):
            coo = self.path[coo]
            res = str(coo) + ' <-- ' + res
        return res

    def __len__(self):
        return len(self.path.keys())

    def backtrack(self):
        to_delete = self.last_coo
        self.last_coo = self.path[to_delete]

        if len( self.path.keys()) == 1:
            pass
        del self.path[to_delete]
        return self.last_coo


# A <- B <- C <- D <= B
# A <- B

# Dus als path[x] bestaat: path terug lezen

if __name__=='__main__':
    p = Path('A')
    p.testmode = True
    p.add( 'B' )
    p.add( 'C' )
    p.add( 'D' )
    p.add( 'B' )
    p.add( 'E' )
    p.add( 'E' )
    p.add( 'F' )
    p.add( 'A' )
    p.add( 'B' )
    p.add( 'C' )
    p.add( 'D' )
    p.add( 'B' )
    p.add( 'E' )
    p.add( 'E' )
    p.add( 'F' )
