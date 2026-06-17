import os
import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Shoot Birds")

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

def cargar_imagen(ruta, ancho, alto, color_fondo=(0, 0, 0)):
    try:
        return pygame.image.load(ruta).convert_alpha()
    except FileNotFoundError:
        superficie = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        superficie.fill(color_fondo)
        return superficie

def cargar_sonido(ruta):
    try:
        return pygame.mixer.Sound(ruta)
    except:
        return None

fondo = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_birds.png"), ANCHO, ALTO, (135, 206, 235))
sonido_disparo = cargar_sonido(os.path.join(ASSETS_DIR, "disparo.wav"))
sonido_golpe = cargar_sonido(os.path.join(ASSETS_DIR, "golpe.wav"))

fuente_grande = pygame.font.SysFont("Arial", 60)
fuente = pygame.font.SysFont("Arial", 30)

class Pajaro:
    def __init__(self):
        self.x = random.randint(100, ANCHO - 100)
        self.y = random.randint(50, ALTO // 2)
        self.vel_x = random.choice([-2, 2])
        self.vel_y = random.choice([-1, 1])
    
    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        
        if self.x < 0 or self.x > ANCHO:
            self.x = random.randint(100, ANCHO - 100)
            self.y = random.randint(50, ALTO // 2)
        if self.y < 0 or self.y > ALTO // 2:
            self.vel_y *= -1
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (50, 50, 50), (int(self.x), int(self.y)), 15)
        pygame.draw.circle(pantalla, (100, 100, 100), (int(self.x) - 8, int(self.y) - 5), 3)

pajaros = [Pajaro() for _ in range(5)]
puntos = 0
municiones = 10
game_over = False
clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN and municiones > 0 and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            municiones -= 1
            
            for pajaro in pajaros[:]:
                distancia = ((pajaro.x - mouse_x) ** 2 + (pajaro.y - mouse_y) ** 2) ** 0.5
                if distancia < 25:
                    pajaros.remove(pajaro)
                    puntos += 10
                    if sonido_golpe:
                        sonido_golpe.play()
            
            if sonido_disparo:
                sonido_disparo.play()
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evento.key == pygame.K_r and game_over:
                municiones = 10
                puntos = 0
                game_over = False
                pajaros = [Pajaro() for _ in range(5)]

    for pajaro in pajaros:
        pajaro.actualizar()

    if municiones <= 0 and len(pajaros) > 0:
        game_over = True

    pantalla.blit(fondo, (0, 0))

    for pajaro in pajaros:
        pajaro.dibujar(pantalla)

    pygame.draw.circle(pantalla, ROJO, pygame.mouse.get_pos(), 5)

    texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    texto_municiones = fuente.render(f"Municiones: {municiones}", True, BLANCO)
    pantalla.blit(texto_puntos, (20, 20))
    pantalla.blit(texto_municiones, (20, 60))

    if game_over:
        texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
        texto_reiniciar = fuente.render("R: Reintentar  ESC: Salir", True, BLANCO)
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))

    pygame.display.update()
    clock.tick(30)
