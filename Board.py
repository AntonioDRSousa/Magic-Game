import pygame
from Conf import X, Y, ssq, width
from Conf import main_color, void_color
from Conf import dimx, dimy, x0, y0, num_void

colors = []
ncolors = 0

class Board:
    def __init__(self,screen,c):
        global colors, ncolors
        self.screen = screen
        
        colors = c.colors
        ncolors = c.ncolors
        
        self.board = [[-1 for x in range(dimx)] for y in range(dimy)]
        
    def checkCol(self,x,y):
        def gcolor(z):
            if z>=0:
                return self.board[z][x]
            else:
                return -1
        b1 = gcolor(y)
        b2 = gcolor(y+1)
        b3 = gcolor(y+2)
        return (b1!=num_void)or(b2!=num_void)or(b3!=num_void)
        
    def canPlace(self):
        if (self.board[0][x0]==num_void):
            return True
        return False
        
    def store(self,p):
        if not p.ismagic:
            x , y = p.x , p.y
            self.board[y][x] = p.jewels[0]
            self.board[y+1][x] = p.jewels[1]
            self.board[y+2][x] = p.jewels[2]
        
  
    def hvd(self,x,y,c,direction): 
        dc = {'H':(x,dimx), 'V':(y,dimy), 'D':(0,min(dimy-y,dimx-x)) , 'd':(0,min(y+1,dimx-x))}
        
        cells = [(x,y)]
        
        for i in range(dc[direction][0]+1,dc[direction][1]):
            dcit = {'H':(i,y), 'V':(x,i), 'D':(x+i,y+i) , 'd':(x+i,y-i)}
            t = dcit[direction]
            if self.board[t[1]][t[0]]!=c:
                break
            cells.append(t)
        
        if (len(cells)>=3):
            return cells
        else:
            return []

    def detectMatch(self):
        cells = []
        combo = 0
        for k in ['H','V','D','d']:
            v = []
            for i in range(dimy):
                for j in range(dimx):
                    if self.board[i][j]!=-1:
                        if (j,i) not in v:
                            w = self.hvd(j,i,self.board[i][j],k)
                            if len(w)!=0:
                                v += w
                                combo+=1
            cells += v
        return cells , combo
        
    def eliminateCells(self,cells):
        jw = 0
        for i in range(dimy):
            for j in range(dimx):
                if (j,i) in cells:
                    self.board[i][j] = -1
                    jw += 1
        return jw
        
    def join(self,cells):
        for i in range(dimx):
            v=[]
            for j in range(dimy):
                if self.board[j][i]!=-1:
                    v.append(self.board[j][i])
            v = [-1]*(dimy-len(v))+v
            for j in range(dimy):
                self.board[j][i]=v[j]
                
    def magicMatch(self,p):
        cells = []
        x , y = p.x , (p.y+2)
        if not (y==(dimy-1)):
            c = self.board[y+1][x]
            for i in range(dimy):
                for j in range(dimx):
                    if self.board[i][j]==c:
                        cells.append((j,i))
        return cells , 0
        
    def clear(self,p,level,rate): 
        jwls = 0
        score = 0
        control = True
        while True:
            if (p.ismagic and control):
                cells , combo = self.magicMatch(p)
                control = False
            else:
                cells , combo = self.detectMatch()
            self.delay(cells)
            jw = self.eliminateCells(cells)
            self.join(cells)
            self.draw()
            if jw==0:   
                break
            jwls += jw
            score += (rate)*(10+level+combo)*jw
        return (jwls , score)
            
            
    def delay(self,cells):
        clock = pygame.time.Clock()
        count = 0
        for i in range(1,10):
            for t in cells:
                r = pygame.Rect((X+t[0]*ssq, Y+t[1]*ssq, ssq, ssq))
                pygame.draw.rect(self.screen,main_color,r,width+i)
            pygame.display.update()
            clock.tick(10)

    def draw(self):
        r = pygame.Rect((X, Y, dimx*ssq, dimy*ssq))
        pygame.draw.rect(self.screen,main_color,r,width)
        for i in range(dimy):
            for j in range(dimx):
                r = pygame.Rect((X+j*ssq, Y+i*ssq, ssq, ssq))
                if self.board[i][j]==num_void:
                    c=void_color
                else:
                    c = colors[self.board[i][j]]
                pygame.draw.rect(self.screen,c,r)
                pygame.draw.rect(self.screen,main_color,r,width)