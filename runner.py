import os
import pygame
import sys

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mario Runner")

BLANCO = (255, 255, 255)
MARRON = (139, 69, 19)

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

fondo = cargar_imagen(os.path.join(ASSETS_DIR, "fondo.png"), ANCHO, ALTO, (0, 100, 200))
mario_img = cargar_imagen(os.path.join(ASSETS_DIR, "mario.png"), 50, 70, (255, 0, 0))
obstaculo_img = cargar_imagen(os.path.join(ASSETS_DIR, "bloque.png"), 40, 60, (200, 0, 0))

sonido_salto = cargar_sonido(os.path.join(ASSETS_DIR, "salto.wav"))

fuente_grande = pygame.font.SysFont("Arial", 60)
fuente = pygame.font.SysFont("Arial", 30)

piso_y = ALTO - 100
jugador_x = 50
jugador_y = piso_y
jugador_ancho = 50
jugador_alto = 70
velocidad_y = 0
gravedad = 0.6
en_suelo = True

obstaculos = []
velocidad_obstaculos = 5

puntuacion = 0
nivel = 1
vidas = 3
game_over = False
tiempo_spawn = 0
spawn_delay = 100

def crear_obstaculo():
    return {"x": ANCHO, "y": piso_y + 20, "width": 40, "height": 60}

clock = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if game_over and evento.key == pygame.K_r:
                puntuacion = 0
                nivel = 1
                vidas = 3
                jugador_y = piso_y
                velocidad_y = 0
                en_suelo = True
                game_over = False
                obstaculos = []
                tiempo_spawn = 0
                spawn_delay = 100
            elif game_over and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif not game_over and evento.key == pygame.K_SPACE and en_suelo:
                velocidad_y = -15
                en_suelo = False
                if sonido_salto:
                    sonido_salto.play()

    if not game_over:
        jugador_y += velocidad_y
        velocidad_y += gravedad
        
        if jugador_y >= piso_y:
            jugador_y = piso_y
            velocidad_y = 0
            en_suelo = True
        
        tiempo_spawn += 1
        if tiempo_spawn >= spawn_delay:
            obstaculos.append(crear_obstaculo())
            tiempo_spawn = 0
            spawn_delay = max(50, 100 - nivel * 5)
        
        for obstaculo in obstaculos[:]:
            obstaculo["x"] -= velocidad_obstaculos + nivel
            
            rect_jugador = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)
            rect_obstaculo = pygame.Rect(obstaculo["x"], obstaculo["y"], obstaculo["width"], obstaculo["height"])
            
            if rect_jugador.colliderect(rect_obstaculo):
                vidas -= 1
                if vidas <= 0:
                    game_over = True
                else:
                    obstaculos.remove(obstaculo)
            
            if obstaculo["x"] < -50:
                obstaculos.remove(obstaculo)
                puntuacion += 1
                if puntuacion >= nivel * 5:
                    nivel += 1

    pantalla.blit(fondo, (0, 0))
    pygame.draw.rect(pantalla, MARRON, (0, piso_y + 60, ANCHO, 40))
    pantalla.blit(mario_img, (jugador_x, jugador_y))
    
    for obstaculo in obstaculos:
        pantalla.blit(obstaculo_img, (obstaculo["x"], obstaculo["y"]))
    
    texto = fuente.render(f"Puntuación: {puntuacion}  Nivel: {nivel}  Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (20, 20))
    
    if game_over:
        texto_game_over = fuente_grande.render("GAME OVER", True, (255, 50, 50))
        texto_reiniciar = fuente.render("R: Reintentar  ESC: Salir", True, BLANCO)
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))
    
    pygame.display.update()
    clock.tick(30)
