import os
import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake Game")

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

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

fondo = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_snake.png"), ANCHO, ALTO, (20, 30, 50))
sonido_comer = cargar_sonido(os.path.join(ASSETS_DIR, "comer.wav"))

fuente_grande = pygame.font.SysFont("Arial", 60)
fuente = pygame.font.SysFont("Arial", 30)

tamaño_grid = 20
serpiente = [(ANCHO // 2 // tamaño_grid, ALTO // 2 // tamaño_grid)]
comida = (random.randint(0, ANCHO // tamaño_grid - 1), random.randint(0, ALTO // tamaño_grid - 1))

direccion = (1, 0)
siguiente_direccion = (1, 0)
puntuacion = 0
game_over = False
clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and direccion != (0, 1):
                siguiente_direccion = (0, -1)
            elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                siguiente_direccion = (0, 1)
            elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                siguiente_direccion = (-1, 0)
            elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                siguiente_direccion = (1, 0)
            elif evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif game_over and evento.key == pygame.K_r:
                serpiente = [(ANCHO // 2 // tamaño_grid, ALTO // 2 // tamaño_grid)]
                comida = (random.randint(0, ANCHO // tamaño_grid - 1), random.randint(0, ALTO // tamaño_grid - 1))
                direccion = (1, 0)
                siguiente_direccion = (1, 0)
                puntuacion = 0
                game_over = False

    if not game_over:
        direccion = siguiente_direccion
        nueva_cabeza = (serpiente[0][0] + direccion[0], serpiente[0][1] + direccion[1])
        
        if (nueva_cabeza[0] < 0 or nueva_cabeza[0] >= ANCHO // tamaño_grid or
            nueva_cabeza[1] < 0 or nueva_cabeza[1] >= ALTO // tamaño_grid or
            nueva_cabeza in serpiente):
            game_over = True
        else:
            serpiente.insert(0, nueva_cabeza)
            
            if nueva_cabeza == comida:
                puntuacion += 10
                comida = (random.randint(0, ANCHO // tamaño_grid - 1), random.randint(0, ALTO // tamaño_grid - 1))
                if sonido_comer:
                    sonido_comer.play()
            else:
                serpiente.pop()

    pantalla.blit(fondo, (0, 0))
    
    for segmento in serpiente:
        pygame.draw.rect(pantalla, VERDE, (segmento[0] * tamaño_grid, segmento[1] * tamaño_grid, tamaño_grid - 1, tamaño_grid - 1))
    
    pygame.draw.rect(pantalla, ROJO, (comida[0] * tamaño_grid, comida[1] * tamaño_grid, tamaño_grid - 1, tamaño_grid - 1))
    
    texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto, (20, 20))
    
    if game_over:
        texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
        texto_reiniciar = fuente.render("R: Reintentar  ESC: Salir", True, BLANCO)
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))
    
    pygame.display.update()
    clock.tick(8)
