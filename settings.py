import pygame
import os

# Размеры экрана
WIDTH, HEIGHT = 1460, 700

# Константы для карточек
CARD_WIDTH, CARD_HEIGHT = 130, 200
FPS = 60
TURN_TIME = 60
MARGIN = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (255, 0, 255)
NEON_RED = (255, 50, 50)
HIGHLIGHT_CYAN = (0, 255, 255)
GLOW_CYAN = (0, 255, 255, 128)
NEON_GREEN = (0, 255, 100)
NEON_CYAN = (0, 255, 255)
NEON_ORANGE = (255, 150, 50)



# Пути к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
FONT_DIR = os.path.join(BASE_DIR, "fonts")

# Шрифт (красивый русский шрифт Noto Sans)
FONT_PATH = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except Exception as e:
        print(f"Ошибка загрузки шрифта: {e}")
        return pygame.font.SysFont("Arial", size)
