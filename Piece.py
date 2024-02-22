import pygame
from random import randint
from Conf import X, Y, ssq, width, nextX
from Conf import main_color, magic_color
from Conf import dimx, dimy, x0, y0, prob

colors = []
ncolors = 0

class Piece:
    def __init__(self,screen,level,c):
        global colors, ncolors
        colors = c.colors
        ncolors = c.ncolors
        self.screen = screen
        self.dx = {'L':-1,'R':1}
        self.x =  x0
        self.y = y0
        r1 = randint(0,ncolors-1)
        r2 = randint(0,ncolors-1)
        r3 = randint(0,ncolors-1)
        self.jewels = [r1,r2,r3]
        
        r = randint(0,prob)
        if (r==0)and(level>2):
            self.ismagic = True
        else:
            self.ismagic = False
        
    def change(self):
        self.jewels = [self.jewels[2]]+self.jewels[:2]
        
    def move(self,direction,board):
        self.x += self.dx[direction]
        if (not (self.x in range(0,dimx))):
            self.x -= self.dx[direction]
        elif board.checkCol(self.x,self.y):
            self.x -= self.dx[direction]
        
    def fall(self,board):
        if ((self.y<(dimy-3))):
            self.y += 1
        else:
            return True
            
        if board.checkCol(self.x,self.y):
            self.y -= 1
            return True
        return False
        
    def drawPiece(self,a,b,i):
        r = pygame.Rect((a, b, ssq, ssq))
        if self.ismagic:
            c = magic_color
        else:
            c = colors[self.jewels[i]]
        pygame.draw.rect(self.screen,c,r)
        pygame.draw.rect(self.screen,main_color,r,width)        
        
    def draw(self):
        for i in range(0,len(self.jewels)):
            k=self.y+i
            if k>=0:
                self.drawPiece(X+self.x*ssq, Y+k*ssq,i)
                
    def drawNext(self):
        for i in range(0,len(self.jewels)):
            self.drawPiece(nextX,Y+i*ssq,i)