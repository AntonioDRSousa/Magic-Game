import pygame
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from Board import *
from Piece import *
from Conf import nhscores
from Conf import Color

fps = 60

class Magic:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600,600))
        pygame.display.set_caption("MAGIC")
        pygame.display.flip()
        
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.start()
        
    def loadHighscore(self):
        fp = open("score/"+str(self.tag)+"/top.num",'r')
        self.highscores=fp.readlines()
        for i in range(nhscores):
            self.highscores[i]=int((self.highscores[i]).split('\n')[0])
        self.top = self.highscores[0]
        fp.close()
        fp = open("score/"+str(self.tag)+"/names.str",'r')
        self.names = fp.readlines()
        fp.close()
        
    def saveHighscore(self):
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:nhscores]
        for i in range(nhscores):
            if ((self.score==self.highscores[i])and(self.score!=0)):
                self.names[i] = self.saveName()+"\n"
        for i in range(nhscores):
            self.highscores[i]=str(self.highscores[i])+"\n"
        fp = open("score/"+str(self.tag)+"/top.num","w")
        fp.writelines(self.highscores)
        fp.close()
        fp = open("score/"+str(self.tag)+"/names.str","w")
        fp.writelines(self.names)
        fp.close()
    
    def saveName(self):
        while True:
            try:
                name = askstring(title='New Highscore', prompt="Name : ",initialvalue="")
                if (len(name)==0):
                    raise
                break
            except:
                showinfo('Error', 'Invalid .....')
        return name
        
    def draw(self):
        self.screen.fill((255,255,255))
        self.board.draw()
        self.piece1.draw()
        self.piece2.drawNext()
        self.drawInf()
        pygame.display.update()
        
    def drawInf(self):
        text_controls = self.font.render("PRESS 'c' for see CONTROLS",True,(0,0,0))
        text_jewels = self.font.render('JEWELS : '+str(self.jewels),True,(0,0,0))
        text_top = self.font.render('TOP     : '+str(self.top),True,(0,0,0))
        text_score = self.font.render('SCORE : '+str(self.score),True,(0,0,0))
        text_level = self.font.render('LEVEL : '+str(self.level),True,(0,0,0))
        text_class = self.font.render('CLASS : '+self.tag,True,(0,0,0))
        
        self.screen.blit(text_controls,(0,350))
        self.screen.blit(text_top, (0,400))
        self.screen.blit(text_score, (0,450))
        self.screen.blit(text_jewels, (0,500))
        self.screen.blit(text_level, (0,550))
        self.screen.blit(text_class, (0,0))
        
    def showHighscores(self):
        s = ""
        for i in range(len(self.highscores)):
            s += f"{(i+1):02d} - {self.highscores[i]} {self.names[i]}"
        showinfo('Highscores',s)
        
    def showControls(self):
        s =  "right -> move piece to right\n"
        s += "left -> move piece to left\n"
        s += "down -> speed fall of piece to max speed\n"
        s += "space -> swap jewels in piece\n"
        s += "p -> pause game\n"
        s += "h -> show highscores\n"
        s += "c -> show controls of game\n"
        s += "n -> new game\n"
        s += "i -> help\n"
        
        showinfo('Controls',s)
        
    def showHelp(self):
        s =  "MAGIC\n\n"
        s += "* Game similar to 'Columns' of SEGA and 'Magic Jewelry' of NES.\n"
        s += "* The objective is earn maximum Points.\n"
        s += "* The game when it's not possible spawn a Piece without ocupie a place not empty in Grid.\n"
        s += "* Grid : 7 X 13 .\n" 
        s += "* The Grid begin empty of Jewels.\n"
        s += "* Each Pieces of game have 3 Jewels chosen randomly.\n"
        s += "* There's 8 possible Jewels, each with a unique color.\n"
        s += "* You begin game with a Piece in ceil.\n"
        s += "* Let be coordenate system (x,y) when x is from 0 to 6 and y is from 0 to 12.\n"
        s += "* All Pieces will be spawn in coordenate (3,-2).\n"
        s += "* Negative y indicates that jewel are above ceil. Observe that the 2 first Jewels in spawned Piece are above Ceil.\n"
        s += "* Jewels above Ceil aren't showed in screen.\n"
        s += "* Out of Grid there's information about the Next Piece that it will be spawn.\n"
        s += "* The Pieces fall until collide with Floor or another with Jewel in Grid."
        s += "* When Piece stops fall, is checked if is possible clear jewels in game.\n"
        s += "* You earn Points by clear Jewels in Grid.\n"
        s += "* You clear Jewels when there's 3 or more Jewels with same color in same Row, Column or Diagonal.\n"
        s += "* Clear Jewels give you points.\n"
        s += "* The remainder Jewels stay in Grid.\n"
        s += "* If there's Jewels that down square isn't Floor or another Jewel, then Jewel will fall until collide with Floor or another Jewel in Grid.\n"
        s += "* The process repeats in loop until there's no more Jewels to clear. Then the Next Piece is spawn.\n"
        s += "* A Combo is the number of sets of Jewels clear at once.\n"
        s += "* For example, you clear 2 rows, 1 column and 3 diagonals you have 6 combos.\n"
        s += "* The game have 60 FPS.\n"
        s += "* The fall's speed of Piece are calculated by Level.\n"
        s += "* Each 1/60 seconds is incremented Count. When Count is 60-level, then Piece fall.\n"
        s += "* You can speed fall of Piece by press down. This made Piece fall each 1/60 seconds until stop the fall.\n"
        s += "* When Jewels cleared in game is more or equals (level+1)*100, then you level up.\n"
        s += "* (rate)*(10+level+combo)*jewels are the score in each clear of jewels.\n"
        s += "* rate is calculate by rate = (60-level) when you speed fall of Piece and level<60.\n"
        s += "* Score, Jewels is acumulative. It's showed by 'Score' and 'Jewels'. Level is showed by 'Level'.\n"
        s += "* The first 10 scores, when game are played, are saved. 'Top' showed the first highscore.\n"
        s += "* If level>2, then there's the random 1/20 chance of Magic Piece. This Piece are showed by color white and don't work how another Pieces.\n"
        s += "* If Magic Piece fall on Jewel, then all Piece of color equals to this Jewel are cleared. The Score is calculate in same way of common Pieces.\n"
        
        showinfo('Help',s)
        
    def close(self):
        self.saveHighscore()
        pygame.quit()
        exit()
        
    def pause(self):
        p = True
        while p:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                    elif event.key == pygame.K_p:
                        p = False
                    elif event.key == pygame.K_h:
                        self.showHighscores()
                    elif event.key == pygame.K_c:
                        self.showControls()
    
    def steps(self):
        if self.piece1.fall(self.board):
            self.board.store(self.piece1)
            b = (self.piece1.y<0)
            
            if ((self.max_count == 1)and(self.level<60)):
                rate = (60-self.level)
            else:
                rate = 1
            t = self.board.clear(self.piece1,self.level,rate)
            self.jewels += t[0]
            self.score += t[1]
            
            self.piece1 = self.piece2
            self.piece2 = Piece(self.screen,self.level,self.color)
            
            if (self.jewels>=((self.level+1)*100)):
                self.level += 1
            
            if self.level<60:
                self.max_count = 60-self.level
            return b
        return False
                
    def showEnd(self):
        s = 'GAME END\n'
        s += 'Score : '+str(self.score)+'\n'
        s += 'Jewels : '+str(self.jewels)+'\n'
        s += 'Level : '+str(self.level)+'\n'
        s += 'Top : '+str(self.top)+'\n'
        showinfo('Game End',s)
        self.saveHighscore()

    def chooseDifficulty(self):
        s =  "DIFFICULTY\n\n"
        s += "[0] - Easy (start in level 0 with 0 points)\n"
        s += "[1] - Medium (start in level 5 with 20000 points)\n"
        s += "[2] - Hard(start in level 10 with 50000 points)\n"
        s += "\nChoose 0,1 or 2 : "
        while True:
            try:
                op = int(askstring(title='Difficulty', prompt=s,initialvalue="0"))
                if ((op<0)or(op>2)):
                    raise
                break
            except:
                showinfo('Error', 'Invalid Option .....')
        if op==0:
            start_level , start_score = 0 , 0
        elif op==1:
            start_level , start_score = 5 , 20000
        else:
            start_level , start_score = 10 , 50000
        return start_level , start_score
        
    def chooseClass(self):
        s =  "CLASS\n\n"
        s += "[0] - Novice (4 colors)\n"
        s += "[1] - Amateur (5 colors)\n"
        s += "[2] - Pro (6 colors)\n"
        s += "[3] - Hardcore (7 colors)\n"
        s += "[4] - God (8 colors)\n"
        s += "\nChoose 0,1,2,3 or 4 : "
        tag = {0:'novice',1:'amateur',2:'pro',3:'hardcore',4:'god'}
        while True:
            try:
                op = int(askstring(title='Class', prompt=s,initialvalue="2"))
                if ((op<0)or(op>4)):
                    raise
                break
            except:
                showinfo('Error', 'Invalid Option .....')
        return op+4 , tag[op]
                
    def newgame(self):
        showinfo('New Game',"Begin")
        clss , self.tag = self.chooseClass()
        self.color = Color(clss)
        self.loadHighscore()
        self.clock = pygame.time.Clock()
        
        self.level , self.score = self.chooseDifficulty()
        self.jewels = 0
        
        self.board = Board(self.screen,self.color)
        self.piece1 = Piece(self.screen,self.level,self.color)
        self.piece2 = Piece(self.screen,self.level,self.color)
        
        self.max_count = 60-self.level
        
    def start(self):
        self.newgame()
        
        count = 0
        while True:
            if count == (self.max_count):
                b=self.steps()
                if (not self.board.canPlace())or(b):
                    self.showEnd()
                    break
            self.draw()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                    elif event.key == pygame.K_p:
                        self.pause()
                    elif event.key == pygame.K_h:
                        self.showHighscores()
                    elif event.key == pygame.K_c:
                        self.showControls()
                    elif event.key == pygame.K_n:
                        count = 0
                        self.showEnd()
                        self.newgame()
                    elif event.key == pygame.K_i:
                        self.showHelp()
                    elif event.key == pygame.K_SPACE:
                        self.piece1.change()
                    elif event.key == pygame.K_LEFT:
                        self.piece1.move('L',self.board)
                    elif event.key == pygame.K_RIGHT:
                        self.piece1.move('R',self.board)
                    elif event.key == pygame.K_DOWN:
                        self.max_count=1
                        count = 0
            self.clock.tick(fps)
            count = (count+1)%(self.max_count+1)