import pygame
import pygame.mixer
import sys
import random
import sqlite3

# Инициализация Pygame
pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DD!Space")

white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

pygame.mixer.init()

# Загрузка музыки для главного экрана
menu_music = pygame.mixer.Sound("data/menu_music.mp3")

# Загрузка музыки для игрового процесса
game_music = pygame.mixer.Sound("data/mainmenu.mp3")

shoot_sound = pygame.mixer.Sound("data/shoot2.wav")

explosion_sound = pygame.mixer.Sound("data/boom.wav")
explosion_sound.set_volume(1.0)

# Определение громкости музыки (от 0.0 до 1.0)
menu_music.set_volume(0.5)
game_music.set_volume(0)
shoot_sound.set_volume(1.0)

conn = sqlite3.connect("highscores.db")
cursor = conn.cursor()
# Создание таблицы для хранения рекордов, если ее еще нет
cursor.execute('''CREATE TABLE IF NOT EXISTS highscores
                  (player_name TEXT, score INTEGER)''')
conn.commit()
conn.close()
