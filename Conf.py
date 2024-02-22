prob = 20
void_color = "gray"
main_color = "black"
magic_color = "white"
dimx = 7
dimy = 12
num_void = -1
y0 = -2
x0 = 3
X = 50
Y = 50
ssq = 25
width = 1
nextX = 250
nhscores = 10

class Color:
    def __init__(self,qtd):
        self.colors = ["red","green","blue","yellow","orange","cyan","magenta","purple"]
        self.colors = self.colors[:qtd]
        self.ncolors = qtd