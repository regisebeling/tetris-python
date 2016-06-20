import pyglet
import pymunk
from sys import argv
import sys
import math, random, time


ESQ = 0
DIR = 1
CIMA = 2
BAIXO = 3

COLUNAS = 16
LINHAS = 32

matriz = []
listsq = []
stuck = 0



class EventHandler(object):
    def __init__(self, window):
        self.window = window

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            exit()

        if symbol == pyglet.window.key.RIGHT:
            self.window.current_form.moveDireita()

        if symbol == pyglet.window.key.LEFT:
            self.window.current_form.moveEsquerda()

        if symbol == pyglet.window.key.DOWN:
            self.window.current_form.moveBaixo()
						
        if symbol == pyglet.window.key.D:
            self.window.current_form.rotate_dir()

        if symbol == pyglet.window.key.A:
            self.window.current_form.rotate_esq()


        return True


class CarregaTextura(pyglet.sprite.Sprite):
    def __init__(self, image, anchor, x, y, batch, group):
        image = pyglet.image.load(image)

        if(anchor):
            image.anchor_x = image.width/2
            image.anchor_y = image.height/2

        pyglet.sprite.Sprite.__init__(self, image, x, y, batch=batch, group= group)



class Square(CarregaTextura):
    def __init__(self, batch, x, y, t, group):
        CarregaTextura.__init__(self, t, False, x, y, batch, group)

    

class Sqpos(object):
    def __init__(self, x, y):
        self.set_x(x)
        self.set_y(y)
        self.set_active(1)


    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_active(self, a):
        self.active = a

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_active(self):
        return self.active

#Classe abstrata
class Tetra(object):
    def __init__(self, squares, batch, group):
		pass
	
    def set_squares(self, squares):
		pass
		
    def set_batch(self, batch):
		pass

    def set_group(self, group):
		pass

    def get_squares(self):
        pass

    def get_batch(self):
        pass

    def get_group(self):
        pass

    def moveEsquerda(self):
        pass
		
    def moveDireita(self):
        pass
		
    def moveBaixo(self):
        pass
		
    def kill(self, square):
        pass

    def rotate_dir(self):
        pass
		
    def rotate_esq(self):
        pass
		
    def __del__(self):
		pass

#Hernaca nivel 2 - implementa interface Tetra		
class Forma(Tetra):

    def __init__(self, squares, batch, group):
        self.set_squares(squares)
        self.set_batch(batch)
        self.set_group(group)

    def set_squares(self, squares):
        self.squares = squares

    def set_batch(self, batch):
        self.batch = batch

    def set_group(self, group):
        self.group = group

    def get_squares(self):
        return self.squares

    def get_batch(self):
        return self.batch

    def get_group(self):
        return self.group

    def moveEsquerda(self):
        for square in self.squares:
            if square.get_x() /20<= 1 or matriz[square.get_y()/20][square.get_x()/20-1] == 1:
                return

        for square in self.squares:
            square.set_x(square.get_x() - 20)

    def moveDireita(self):
        for square in self.squares:
            if square.get_x() / 20 >= COLUNAS or matriz[square.get_y() / 20][square.get_x() / 20 + 1] == 1:
                return

        for square in self.squares:
            square.set_x(square.get_x() + 20)


    def moveBaixo(self):
        for square in self.squares:
            if (square.get_y()/20 <= 1 or matriz[square.get_y()/20-1][square.get_x()/20] == 1):
                global stuck
                stuck = 1
                return

        for square in self.squares:
            square.set_y(square.get_y() - 20)


    def kill(self, square):
        i=0
        for i in range(0,4):
            if self.squares[i].get_x() == square.get_x() and self.squares[i].get_y() == square.get_y():
                self.squares[i].set_active(0)


    def rotate_dir(self):#D
        px = self.squares[1].get_x()
        py = self.squares[2].get_y()
        newx = []
        newy = []
        count = 0
        for square in self.squares:
            oldx = square.get_x()
            oldy = square.get_y()
            x = (oldy + px - py)
            y = (px + py - oldx)
            newx.append(x)
            newy.append(y)

            if (matriz[y / 20][x / 20] != 1 and x / 20 < COLUNAS and x / 20 > 0 and y / 20 > 0 and y / 20 < LINHAS):
                count += 1

        if count == 4:
            i = 0
            for square in self.squares:
                square.set_x(newx[i])
                square.set_y(newy[i])
                i += 1

    def rotate_esq(self): #A
        px = self.squares[2].get_x()
        py = self.squares[3].get_y()
        newx = []
        newy = []
        count = 0
        for square in self.squares:
            oldx = square.get_x()
            oldy = square.get_y()
            x = (px + py - oldy)
            y = (oldx + py - px)
            newx.append(x)
            newy.append(y)

            if (matriz[y / 20][x / 20] != 1 and x / 20 < COLUNAS and x / 20 > 0 and y / 20 > 0 and y / 20 < LINHAS):
                count += 1
        if count == 4:
            i=0
            for square in self.squares:
                square.set_x(newx[i])
                square.set_y(newy[i])
                i+=1

    def __del__(self):
		print "Desalocando Forma"

		
#Classes herdando classe Forma
#Classe FormaO nao tem metodo destrutor (chama da classe Forma) e todas as outras tem. Entao, ela eh a unica que nao esta implementando o destrutor via polimorfismo por inclusao
class FormaO(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2, 30*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 30*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'bluesq.png', group=self.get_group()))

    			
				
class FormaS(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 -20, 30*20))
        squares.append(Sqpos(COLUNAS*20/2, 30*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'orangesq.png', group=self.get_group()))

    def __del__(self):
        print "Desalocando tetra S"
				
				
class FormaZ(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 -20, 31*20))
        squares.append(Sqpos(COLUNAS*20/2, 30*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 30*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'yellowsq.png', group= self.get_group()))

				
    def __del__(self):
        print "Desalocando tetra Z"
				

class FormaT(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 -20, 31*20))
        squares.append(Sqpos(COLUNAS*20/2, 30*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'greensq.png', group = self.get_group()))

    def __del__(self):
        print "Desalocando tetra T"

				
class FormaI(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 + 40, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 - 20, 31*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'redsq.png', group = self.get_group()))

    def __del__(self):
        print "Desalocando tetra I"
				
				
class FormaL(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 -20, 30*20))
        squares.append(Sqpos(COLUNAS*20/2 - 20, 31*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'lbluesq.png', group = self.get_group()))

    def __del__(self):
        print "Desalocando tetra L"

				
class FormaJ(Forma):

    def __init__(self, batch, group):
        squares = []

        squares.append(Sqpos(COLUNAS*20/2 +20, 30*20))
        squares.append(Sqpos(COLUNAS*20/2 - 20, 31*20))
        squares.append(Sqpos(COLUNAS*20/2, 31*20))
        squares.append(Sqpos(COLUNAS*20/2 + 20, 31*20))

        Forma.__init__(self, squares, batch, group)

    def update(self):
        for square in self.squares:
            if square.active == 1:
                listsq.append(Square(batch = self.get_batch(), x = square.get_x(), y = square.get_y(), t = 'purplesq.png', group = self.get_group()))

    def __del__(self):
        print "Desalocando tetra J"



class Game(pyglet.window.Window):
    def __init__(self, space):

        self.space = space

        pyglet.window.Window.__init__(self, width=(COLUNAS*20 + 2*20 + 240), height=(LINHAS*20 + 2*20))

        self.push_handlers(EventHandler(self))
        self.batch_draw = pyglet.graphics.Batch()
        self.scenery = pyglet.graphics.OrderedGroup(0)
        self.pieces = pyglet.graphics.OrderedGroup(1)
        self.foreground = pyglet.graphics.OrderedGroup(2)

        self.formas = []

        self.init_matriz()

        self.draw_game()

        self.current_form = self.random_form()

        self.score = 0

        self.score_label = pyglet.text.Label("Score: %d" % (self.score),
                                  font_name='Times New Roman',
                                  font_size=32,
                                  x=COLUNAS*20 + 140, y=LINHAS*20,
                                  anchor_x='center', anchor_y='center')

        self.inst1 = pyglet.text.Label("Mover: setas",
                                             font_name='Times New Roman',
                                             font_size=24,
                                             x=COLUNAS * 20 + 140, y=(LINHAS/2) * 20 - 80,
                                             anchor_x='center', anchor_y='center')

        self.inst2 = pyglet.text.Label("Girar: A D",
                                             font_name='Times New Roman',
                                             font_size=24,
                                             x=COLUNAS * 20 + 140, y=LINHAS//3 * 20,
                                             anchor_x='center', anchor_y='center')

        self.inst3 = pyglet.text.Label("Sair: Esc",
                                             font_name='Times New Roman',
                                             font_size=24,
                                             x=COLUNAS * 20 + 140, y=LINHAS//4 * 20,
                                             anchor_x='center', anchor_y='center')

        self.logo = CarregaTextura(image='logo.png', anchor=True, x=COLUNAS*20 + 150, y=LINHAS/2 * 20 + 80, batch = self.batch_draw, group = self.scenery)



        pyglet.clock.schedule_interval(self.update, 0.15)

    def init_matriz(self):


        for i in range(0, LINHAS):
            new = []
            for j in range(0, COLUNAS+2):
                new.append(0)
            matriz.append(new)

	#Carrega uma peca random
    def random_form(self):
        i = random.randint(1, 7)

        if i == 1:
            forma = FormaO(self.batch_draw, self.pieces)
        if i == 2:
            forma = FormaJ(self.batch_draw, self.pieces)
        if i == 3:
            forma = FormaL(self.batch_draw, self.pieces)
        if i == 4:
            forma = FormaI(self.batch_draw, self.pieces)
        if i == 5:
            forma = FormaT(self.batch_draw, self.pieces)
        if i == 6:
            forma = FormaS(self.batch_draw, self.pieces)
        if i == 7:
            forma = FormaZ(self.batch_draw, self.pieces)

        return forma


    def draw_game(self):

        self.squares = []

        # Coloca os blocos de limite
        #for i in range(0, COLUNAS + 2):
            #self.squares.append(Square(batch=self.batch_draw, x=(i) * 20, y=(LINHAS + 1) * 20, t = 'wallsq.png'))
        for i in range(0, COLUNAS + 2):
            self.squares.append(Square(batch=self.batch_draw, x=(i) * 20, y=(0) * 20, t = 'wallsq.png', group = self.scenery))
        for j in range(0, LINHAS + 2):
            self.squares.append(Square(batch=self.batch_draw, x=(COLUNAS + 1) * 20, y=(j) * 20, t = 'wallsq.png', group = self.scenery))
        for j in range(0, LINHAS + 2):
            self.squares.append(Square(batch=self.batch_draw, x=(0) * 20, y=(j) * 20, t = 'wallsq.png', group = self.scenery))


    def acha_sq(self, y, x):
        for forma in self.formas:
            for square in forma.squares:
                if square.get_active() == 1 and square.get_x()/20 == x and square.get_y()/20 == y:
                    return square
        return 0


    def linha_completa(self):
        c = 0
        for i in range (0,LINHAS):
            c = 0
            for j in range(0,COLUNAS):
                if matriz[i][j] == 1:
                    c += 1
            if c >= COLUNAS-1:
                return i

        return -1

    def apaga_linha(self, linha):

        for forma in self.formas:
            for square in forma.squares:
                if square.get_y()/20 == linha:
                    forma.kill(square)
                    matriz[square.get_y()/20][square.get_x()/20] = 0

        for i in range(linha, LINHAS):
            for j in range(0, COLUNAS+1):
                sq = self.acha_sq(i,j)
                if sq != 0:
                    sq.set_y(sq.get_y() - 20)
                matriz[i][j] = 0


    def on_draw(self):

        self.score_label = pyglet.text.Label("Score: %d" % (self.score),
                                             font_name='Times New Roman',
                                             font_size=32,
                                             x=COLUNAS * 20 + 140, y=LINHAS * 20,
                                             anchor_x='center', anchor_y='center')

        self.clear()
        self.batch_draw.draw()
        self.score_label.draw()
        self.inst1.draw()
        self.inst2.draw()
        self.inst3.draw()


    def game_over(self):
        self.game_over_logo = CarregaTextura(image='game_over.png', anchor=True, x=COLUNAS * 20 // 2, y=LINHAS * 20 // 2,
                                        batch=self.batch_draw, group=self.foreground)


    def update_matriz(self):
        for forma in self.formas:
            for square in forma.squares:
                if square.get_active() == 1:
                    matriz[square.get_y() / 20][square.get_x() / 20] = 1

    def update(self, dt):

       self.update_matriz()
       global stuck

       if(stuck == 1):
           stuck = 0

           self.formas.append(self.current_form)
           self.update_matriz()

           while(self.linha_completa() != -1):
               print "Linha completa: %d" % (self.linha_completa())
               self.apaga_linha(self.linha_completa())
               self.update_matriz()
               self.score += 100

           self.update_matriz()

           self.current_form = self.random_form()

           if (matriz[self.current_form.squares[0].get_y()/20 -1][self.current_form.squares[0].get_x()/20] == 1 or
               matriz[self.current_form.squares[1].get_y() / 20 - 1][self.current_form.squares[1].get_x() / 20] == 1 or
               matriz[self.current_form.squares[2].get_y() / 20 - 1][self.current_form.squares[2].get_x() / 20] == 1 or
               matriz[self.current_form.squares[3].get_y() / 20 - 1][self.current_form.squares[3].get_x() / 20] == 1):

               self.game_over()

               pyglet.clock.unschedule(self.update)


       else:
            self.current_form.moveBaixo()
            listsq[:] = []
            self.current_form.update()
            for forma in self.formas:
                forma.update()
            self.current_form.__del__()


if __name__ == '__main__':
    space = pymunk.Space()

    window = Game(space=space)


    pyglet.app.run()
