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

shuttle_img = pygame.image.load("data/shattle.png")
shuttle_size = 50
shuttle_img = pygame.transform.scale(shuttle_img, (shuttle_size, shuttle_size))


enemy_img = pygame.image.load("data/enemy.png")
enemy_size = 50
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))


enemy2_img = pygame.image.load("data/enemy2.png")
enemy2_size = 50
enemy2_img = pygame.transform.scale(enemy2_img, (enemy2_size, enemy2_size))

bullet_img = pygame.image.load("data/bullet.png")
bullet_size = 30
bullet_img = pygame.transform.scale(bullet_img, (bullet_size, bullet_size))

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

shuttle_x = width // 2 - shuttle_size // 2
shuttle_y = height - 2 * shuttle_size
shuttle_speed = 8
shuttle_lives = 3
random_point = random.randint(0, 1)

bullet_size = 8
bullet_speed = 15
bullets = []

enemy_speed = 5
enemies = []

score = 0

menu_bg = pygame.image.load("data/bg2.jpg")
menu_bg = pygame.transform.scale(menu_bg, (width, height))

font_pixel = pygame.font.Font("data/pixelfont.ttf", 100)

def set_new_highscore(player_name, score):
    conn = sqlite3.connect("highscores.db")
    cursor = conn.cursor()

    # Проверка, есть ли уже запись для этого игрока в базе данных
    cursor.execute("SELECT * FROM highscores WHERE player_name=?", (player_name,))
    existing_record = cursor.fetchone()
    if existing_record:
        # Если запись существует, обновляем ее, если текущий счет больше предыдущего
        if score > existing_record[1]:
            cursor.execute("UPDATE highscores SET score=? WHERE player_name=?", (score, player_name))
    else:
        # Если записи нет, добавляем новую запись
        cursor.execute("INSERT INTO highscores (player_name, score) VALUES (?, ?)", ("Player", score))
    conn.commit()
    conn.close()

# Функция для получения самого высокого рекорда из базы данных
def get_highest_score():
    conn = sqlite3.connect("highscores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(score) FROM highscores")
    highest_score = cursor.fetchone()[0]
    conn.close()
    return highest_score if highest_score is not None else 0
def draw_shuttle(x, y):
    win.blit(shuttle_img, (x, y))

def draw_enemy(x, y):
    if random_point == 0:
        win.blit(enemy_img, (x, y))
    else:
        win.blit(enemy2_img, (x, y))
def draw_bullets(bullets):
    for bullet in bullets:
        win.blit(bullet_img, (bullet[0], bullet[1]))
