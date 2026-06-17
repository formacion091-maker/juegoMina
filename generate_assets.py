import os
import wave
import struct
import math
import pygame

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')

if not os.path.isdir(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

pygame.init()

# Generar fondo
fondo = pygame.Surface((800, 600))
fondo.fill((100, 180, 240))
for i in range(0, 800, 80):
    pygame.draw.rect(fondo, (80, 120, 70), (i, 520, 80, 80))
for x in range(0, 800, 160):
    pygame.draw.circle(fondo, (255, 255, 255), (x + 80, 120), 40)
pygame.image.save(fondo, os.path.join(ASSETS_DIR, 'fondo.png'))

# Generar personaje mario
mario = pygame.Surface((50, 70), pygame.SRCALPHA)
pygame.draw.rect(mario, (255, 0, 0), (0, 0, 50, 35))
pygame.draw.rect(mario, (0, 0, 255), (0, 35, 50, 35))
pygame.draw.circle(mario, (255, 220, 180), (25, 18), 16)
pygame.draw.rect(mario, (160, 82, 45), (15, 40, 20, 20))
pygame.image.save(mario, os.path.join(ASSETS_DIR, 'mario.png'))

# Generar bloque
bloque = pygame.Surface((100, 20), pygame.SRCALPHA)
pygame.draw.rect(bloque, (170, 120, 70), (0, 0, 100, 20))
for i in range(0, 100, 20):
    pygame.draw.rect(bloque, (200, 160, 100), (i + 2, 2, 16, 16))
pygame.image.save(bloque, os.path.join(ASSETS_DIR, 'bloque.png'))

# Generar sonido salto simple
sample_rate = 44100
duration = 0.25
frequency = 880.0
num_samples = int(sample_rate * duration)
with wave.open(os.path.join(ASSETS_DIR, 'salto.wav'), 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for i in range(num_samples):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate) * (1.0 - i / num_samples))
        wav_file.writeframes(struct.pack('<h', value))

print('Generación completa:', os.listdir(ASSETS_DIR))
