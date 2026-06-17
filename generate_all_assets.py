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

# Generar fondo para Snake (patrón de cuadrícula)
fondo_snake = pygame.Surface((800, 600))
fondo_snake.fill((20, 30, 50))
for x in range(0, 800, 20):
    pygame.draw.line(fondo_snake, (40, 50, 80), (x, 0), (x, 600))
for y in range(0, 600, 20):
    pygame.draw.line(fondo_snake, (40, 50, 80), (0, y), (800, y))
pygame.image.save(fondo_snake, os.path.join(ASSETS_DIR, 'fondo_snake.png'))

# Generar fondo para Shoot Birds (cielo con nubes)
fondo_birds = pygame.Surface((800, 600))
fondo_birds.fill((135, 206, 235))
for i in range(0, 800, 150):
    pygame.draw.ellipse(fondo_birds, (255, 255, 255), (i, 50, 100, 40))
    pygame.draw.ellipse(fondo_birds, (255, 255, 255), (i + 30, 40, 90, 50))
    pygame.draw.ellipse(fondo_birds, (200, 220, 255), (i + 60, 60, 80, 30))
pygame.image.save(fondo_birds, os.path.join(ASSETS_DIR, 'fondo_birds.png'))

# Generar fondo para menú
fondo_menu = pygame.Surface((800, 600))
fondo_menu.fill((30, 30, 60))
for i in range(0, 800, 100):
    pygame.draw.rect(fondo_menu, (50, 100, 150), (i, 0, 50, 600))
    pygame.draw.rect(fondo_menu, (100, 150, 200), (i + 50, 0, 50, 600))
pygame.image.save(fondo_menu, os.path.join(ASSETS_DIR, 'fondo_menu.png'))

# Sonido para comer (Snake)
sample_rate = 44100
duration = 0.1
frequency = 440.0
num_samples = int(sample_rate * duration)
with wave.open(os.path.join(ASSETS_DIR, 'comer.wav'), 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for i in range(num_samples):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate) * (1.0 - i / num_samples))
        wav_file.writeframes(struct.pack('<h', value))

# Sonido para disparo
duration = 0.15
frequencies = [600, 400, 200]
samples_per_freq = int(sample_rate * duration / len(frequencies))
with wave.open(os.path.join(ASSETS_DIR, 'disparo.wav'), 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for freq in frequencies:
        for i in range(samples_per_freq):
            value = int(32767.0 * math.sin(2.0 * math.pi * freq * i / sample_rate) * (1.0 - i / samples_per_freq))
            wav_file.writeframes(struct.pack('<h', value))

# Sonido para golpear pájaro
duration = 0.2
frequency = 300.0
num_samples = int(sample_rate * duration)
with wave.open(os.path.join(ASSETS_DIR, 'golpe.wav'), 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    for i in range(num_samples):
        value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate) * (1.0 - i / num_samples))
        wav_file.writeframes(struct.pack('<h', value))

print('Assets generados:', os.listdir(ASSETS_DIR))
