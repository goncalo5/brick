from Tkinter import *
from constantes import *

from retangulo import Retangulo
from bola import Bola
import random

# Considera
# 1) Imagens separadas vs unicas
# 2) Tamanho do spritesheet (.png, .jpg, .ppm, .gif, .) footprint (256, 256, 256)
# 3) Overflow de memoria
# 4) Processamento
# 5) Formato da imagem
# 6) Controle da animacao FPS = frames per seconds = 100 (30 ou 60)


class Jogo(object):
    """
    Classe que organiza os elementos do jogo
    """
    def __init__(self):
        # Criamos o conteiner principal do jogo
        self.root = Tk()
        self.root.geometry('%ix%i' % (LARGURA, ALTURA))
        self.root.resizable(False, False)
        self.root.title('Joguinho Besta')

        # E uma frame para conter o canvas
        self.frame = Frame(bg="black")
        self.frame.pack()
        
        # Criamos a tela do jogo
        self.canvas = Canvas(self.frame, bg="black", width=CANVAS_L, height=CANVAS_A)
        self.canvas.pack()

        # E colocamos um botao para comecar o jogo
        self.comecar = Button(self.root, text='START', command=self.comeca)
        self.comecar.focus_force()
        self.comecar.pack()

        # Bind com a tecla enter
        # self.comecar.bind('<Return>', self.comeca)

        self.spritesheet = []
        self.number_of_sprite = 0
        self.limite = self.bola = self.player = self.r = self.jogando = self.msg = None

        # Carrega o spritesheet
        self.carrega_imagens()

        self.novo_jogo()

        self.root.mainloop()

    def carrega_imagens(self):
        """
        Carrega as imagens de animacao no fundo
        """
        for i in range(1, 91):
            # gif, pgm, ppm, pbx --> PIL == Pillow (png, jpeg...)
            try:
                self.spritesheet.append(PhotoImage(file="psico_bg/psico_%.2i.gif" % i))
            except:
                pass
        self.limite = len(self.spritesheet) - 1

    def novo_jogo(self):  # Cria os elementos necessario para um novo jogo
        # Criamos a bola que ira se movimentar
        self.bola = Bola(**BOLA_CONF)

        # E o player tambem
        self.player = Retangulo(**PLAYER_CONF)
        self.player.desenhar(self.canvas)

        # E adicionamos o evento de movimentacao com o uso do teclado para o player
        self.canvas.bind('<Motion>', self.move_player)

        # Lista dos retangulos
        self.r = []

        # E por fim as diversas fileiras de retangulos
        l, c, e = L, C, E  # linhas, colunas e espacamento
        b, h, y0 = B, H, Y0  # Base, altura e posicao inicial dos retangulos
        for i in range(l):
            cor = random.choice(CORES)
            for j in range(c):
                r = Retangulo(b, h, cor, (b*j+(j+1)*e, i*h+(i+1)*e + y0), (0, 0), 'rect')
                self.r.append(r)

        # Mantemos uma variavel para mostrar que ainda esta rolando um jogo
        self.jogando = True

    def comeca(self):
        """
        Inicia o jogo
        """
        self.jogar()

    def jogar(self):
        """
        Deve ser executado enquanto o jogo estiver rodando
        """
        if self.jogando:
            self.update()
            self.desenhar()

            if len(self.r) == 0:
                self.jogando = False
                self.msg = 'VENCEU'
            if self.bola.y > CANVAS_A:
                self.jogando = False
                self.msg = 'PERDEU'
            
            self.root.after(10, self.jogar)
        else:
            self.acabou(self.msg)

    def move_player(self, event):
        """
        Move o player na tela de acordo com o movimento do mouse
        """
        if 0 < event.x < CANVAS_L - self.player.b:
            self.player.x = event.x

    def update(self):  # Updatamos as condicoes do jogo
        self.bola.update(self)

        self.number_of_sprite += 1
        if self.number_of_sprite > self.limite:
            self.number_of_sprite = 0

        # Depois de mover a bola e preciso procurar por coliscoes
        # self.VerificaColisao()

    def desenhar(self):  # Metodo para redesenhar a tela do jogo
        # primeiro apagamos tudo que ha no canvas
        self.canvas.delete(ALL)

        # Desenhamos o background
        try:
            self.canvas.create_image((CANVAS_L/2, CANVAS_A/2), image=self.spritesheet[self.number_of_sprite])
        except:
            pass
        # e o player
        self.player.desenhar(self.canvas)

        # E por fim todos os retangulos
        for r in self.r:
            r.desenhar(self.canvas)

        # depois desenhamos a bola
        self.bola.desenhar(self.canvas)

    def recomeca(self):  # Recomeca o jogo
        self.novo_jogo()
        self.comecar['text'] = 'START'
        self.jogar()

    def acabou(self, msg):
        """
        Aparece a msg na tela informando o player se ele ganhou ou perdeu
        """
        self.canvas.delete(ALL)
        self.canvas.create_text(CANVAS_L/2, CANVAS_A/2, text=msg, fill='white')
        self.comecar['text'] = 'RESTART'
        self.comecar['command'] = self.recomeca

    def verifica_colisao(self):
        """
        Verifica se houve alguma colisao entre elementos do jogo
        """
        # Primeiro criamos uma bounding box para a bola
        coord = self.canvas.bbox('bola')
        # x1, y1, x2, y2

        # Depois pegamos a id de todos os objetos que colidem com a bola
        colisoes = self.canvas.find_overlapping(*coord)

        # Se o numero de colisoes for diferente de zero
        if len(colisoes) != 0:
            # verificamos se o id do objeto e diferente do player
            if colisoes[0] != self.player:
                # Vamos checar a colisao com o objeto mais proximo do topo
                # esquerdo da bola
                m_p = self.canvas.find_closest(coord[0], coord[1])
                
                # Depois temos que olhar para cada um dos retangulos para identificar
                # com quem a bola colidiu
                for r in self.r:
                    # tendo encontrado o retangulo
                    if r == m_p[0]:
                        # deletamos ele do jogo
                        self.r.remove(r)
                        self.canvas.delete(r)

                        # E invertemos o sentido da velocidade da bola
                        self.b_vy *= -1

                        # Por fim saimos da funcao
                        return

if __name__ == '__main__':
    Jogo()
