dimy = 13
dimx = 7

def diagonal(x,y):
    def it(a,b,s):
        for i in range(a,b):
            t=(x+i,y+s*i)
            cells.append(t)
    cells = [(x,y)]
        
    it(1,min(dimy-y,dimx-x),1)
    it(1,min(y+1,dimx-x),-1)
    return cells

while True:
    print("\n\n\n")
    #self.board = [[-1 for x in range(dimx)] for y in range(dimy)]
    x = int(input("x = "))
    y = int(input("y = "))
    print("\n\n\n")
    v = diagonal(x,y)
    for i in range(dimy):
        for j in range(dimx):
            if (j,i) in v:
                print(" * ",end="")
            else:
                print(" o ",end="")
        print()
