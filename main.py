# main.py
import pygame
import sys
import pygame_gui
import os
from settings import WIDTH, HEIGHT, load_background_images, BACKGROUND_MUSIC, MUSIC_VOLUME, MUSIC_FADE_TIME
from game import game_screen
from card import load_card_images
from menu import main_menu, rules_screen, final_screen

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройка музыки
pygame.mixer.music.load(BACKGROUND_MUSIC)
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("КиберШторм")

# Определяем базовую директорию и путь к theme.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(BASE_DIR, "theme.json")

# Отладочный вывод
print(f"Текущая рабочая директория: {os.getcwd()}")
print(f"Путь к theme.json: {THEME_PATH}")

# Инициализация pygame_gui
try:
    manager = pygame_gui.UIManager((WIDTH, HEIGHT), THEME_PATH)
    print("theme.json успешно загружен")
except FileNotFoundError:
    print(f"Ошибка: файл theme.json не найден по пути: {THEME_PATH}. Используется тема по умолчанию.")
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Загружаем изображения после инициализации дисплея
load_card_images()
load_background_images()

def main():
    current_screen = "menu"
    player_wins = 0
    hacker_wins = 0

    while True:
        if current_screen == "menu":
            current_screen = main_menu(manager, screen)
        elif current_screen == "rules":
            current_screen = rules_screen(manager, screen)
        elif current_screen == "game":
            current_screen, player_wins, hacker_wins = game_screen(manager, screen)
        elif current_screen == "final":
            current_screen = final_screen(manager, screen, player_wins, hacker_wins)
        elif current_screen == "exit":
            # Плавно останавливаем музыку перед выходом
            pygame.mixer.music.fadeout(MUSIC_FADE_TIME)
            pygame.time.wait(MUSIC_FADE_TIME)
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()