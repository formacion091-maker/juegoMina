import os
import pygame
import sys
import subprocess

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("MULTI GAME MENU")

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

fondo_menu = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_menu.png"), ANCHO, ALTO, (30, 30, 60))

fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_media = pygame.font.SysFont("Arial", 40)
fuente = pygame.font.SysFont("Arial", 30)

seleccion = 0
juegos = ["MARIO RUNNER", "SNAKE", "SHOOT BIRDS"]
archivos = ["runner.py", "snake.py", "birds.py"]

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                seleccion = (seleccion - 1) % len(juegos)
            elif evento.key == pygame.K_DOWN:
                seleccion = (seleccion + 1) % len(juegos)
            elif evento.key == pygame.K_RETURN:
                archivo = os.path.join(SCRIPT_DIR, archivos[seleccion])
                subprocess.run([sys.executable, archivo])

    pantalla.blit(fondo_menu, (0, 0))

    titulo = fuente_grande.render("MULTI GAME", True, BLANCO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

    for i, juego in enumerate(juegos):
        if i == seleccion:
            texto = fuente_media.render(f"> {juego} <", True, ROJO)
        else:
            texto = fuente_media.render(juego, True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 200 + i * 80))

    instrucciones = fuente.render("Usa UP/DOWN para navegar, ENTER para seleccionar", True, (200, 200, 200))
    pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 60))

    pygame.display.update()
    pygame.time.Clock().tick(30)
