import os
import pygame
import sys
import random

pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Multi Game - Mario Runner | Snake | Shoot Birds")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
MARRON = (139, 69, 19)

# Directorios
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

# Cargar assets
fondo_menu = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_menu.png"), ANCHO, ALTO, (30, 30, 60))
fondo_runner = cargar_imagen(os.path.join(ASSETS_DIR, "fondo.png"), ANCHO, ALTO, (0, 100, 200))
fondo_snake = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_snake.png"), ANCHO, ALTO, (20, 30, 50))
fondo_birds = cargar_imagen(os.path.join(ASSETS_DIR, "fondo_birds.png"), ANCHO, ALTO, (135, 206, 235))

mario_img = cargar_imagen(os.path.join(ASSETS_DIR, "mario.png"), 50, 70, (255, 0, 0))
obstaculo_img = cargar_imagen(os.path.join(ASSETS_DIR, "bloque.png"), 40, 60, (200, 0, 0))

sonido_salto = cargar_sonido(os.path.join(ASSETS_DIR, "salto.wav"))
sonido_comer = cargar_sonido(os.path.join(ASSETS_DIR, "comer.wav"))
sonido_disparo = cargar_sonido(os.path.join(ASSETS_DIR, "disparo.wav"))
sonido_golpe = cargar_sonido(os.path.join(ASSETS_DIR, "golpe.wav"))

fuente_grande = pygame.font.SysFont("Arial", 60)
fuente_media = pygame.font.SysFont("Arial", 40)
fuente = pygame.font.SysFont("Arial", 30)

# ==================== MENU ====================
def menu_principal():
    seleccion = 0
    juegos = ["MARIO RUNNER", "SNAKE", "SHOOT BIRDS"]
    
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
                    return seleccion
        
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

# ==================== JUEGO 1: MARIO RUNNER ====================
def juego_runner():
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
    
    clock = pygame.time.Clock()
    
    def crear_obstaculo():
        return {"x": ANCHO, "y": piso_y + 20, "width": 40, "height": 60}
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if game_over and evento.key == pygame.K_r:
                    return
                elif game_over and evento.key == pygame.K_ESCAPE:
                    return
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
        
        pantalla.blit(fondo_runner, (0, 0))
        pygame.draw.rect(pantalla, MARRON, (0, piso_y + 60, ANCHO, 40))
        pantalla.blit(mario_img, (jugador_x, jugador_y))
        
        for obstaculo in obstaculos:
            pantalla.blit(obstaculo_img, (obstaculo["x"], obstaculo["y"]))
        
        texto = fuente.render(f"Puntuación: {puntuacion}  Nivel: {nivel}  Vidas: {vidas}", True, BLANCO)
        pantalla.blit(texto, (20, 20))
        
        if game_over:
            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
            texto_reiniciar = fuente.render("Presiona R para reintentar o ESC para menú", True, BLANCO)
            pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
            pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))
        
        pygame.display.update()
        clock.tick(30)

# ==================== JUEGO 2: SNAKE ====================
def juego_snake():
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
                    return
        
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
        
        pantalla.blit(fondo_snake, (0, 0))
        
        for segmento in serpiente:
            pygame.draw.rect(pantalla, VERDE, (segmento[0] * tamaño_grid, segmento[1] * tamaño_grid, tamaño_grid - 1, tamaño_grid - 1))
        
        pygame.draw.rect(pantalla, ROJO, (comida[0] * tamaño_grid, comida[1] * tamaño_grid, tamaño_grid - 1, tamaño_grid - 1))
        
        texto = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        pantalla.blit(texto, (20, 20))
        
        if game_over:
            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
            texto_reiniciar = fuente.render("Presiona ESC para volver al menú", True, BLANCO)
            pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
            pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))
        
        pygame.display.update()
        clock.tick(8)

# ==================== JUEGO 3: SHOOT BIRDS ====================
def juego_birds():
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
        
        def dibujar(self):
            pygame.draw.circle(pantalla, (50, 50, 50), (self.x, self.y), 15)
            pygame.draw.circle(pantalla, (100, 100, 100), (self.x - 8, self.y - 5), 3)
    
    pajaros = [Pajaro() for _ in range(5)]
    puntos = 0
    municiones = 10
    tiempo_recarga = 0
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
                    return
                if evento.key == pygame.K_r:
                    municiones = 10
                    puntos = 0
                    game_over = False
                    pajaros = [Pajaro() for _ in range(5)]
        
        for pajaro in pajaros:
            pajaro.actualizar()
        
        if municiones <= 0 and len(pajaros) > 0:
            game_over = True
        
        pantalla.blit(fondo_birds, (0, 0))
        
        for pajaro in pajaros:
            pajaro.dibujar()
        
        pygame.draw.line(pantalla, ROJO, pygame.mouse.get_pos(), pygame.mouse.get_pos(), 2)
        
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        texto_municiones = fuente.render(f"Municiones: {municiones}", True, BLANCO)
        pantalla.blit(texto_puntos, (20, 20))
        pantalla.blit(texto_municiones, (20, 60))
        
        if game_over:
            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
            texto_reiniciar = fuente.render("Presiona R para reintentar o ESC para menú", True, BLANCO)
            pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 60))
            pantalla.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2 + 20))
        
        pygame.display.update()
        clock.tick(30)

# ==================== MAIN ====================
while True:
    seleccion = menu_principal()
    
    if seleccion == 0:
        juego_runner()
    elif seleccion == 1:
        juego_snake()
    elif seleccion == 2:
        juego_birds()
