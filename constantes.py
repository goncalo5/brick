LARGURA = 800
ALTURA = 600

CANVAS_L = 800
CANVAS_A = 550

FPS = 30
DT = 1/FPS

# as diversas fileiras de retangulos
L, C, E = 5, 8, 2  # linhas, colunas e espacamento
B, H, Y0 = (CANVAS_L - (C - 1) * E)/C, 20, 20  # Base, altura e posicao inicial dos retangulos
CORES = ['lightgray', 'white', 'red', 'blue', 'yellow', 'green', 'orange', 'purple']

# PLAYER (RETANGULO)
PLAYER_CONF = {'largura': 80, 'altura': 20, 'cor': 'green',
               'pos': (LARGURA//2 + 100, CANVAS_A - 50),
               'vel': (15, 15), 'tag': 'player'}

# BOLA
RAIO = 15
COR = 'lightgray'
POSX, POSY = 100, 200
VELX, VELY = 15, 15
BOLA_CONF = {'raio': RAIO, 'cor': COR,
             'pos': (POSX, POSY), 'vel': (VELX, VELY)}
