# settings.py
import pygame
import os

# Размеры экрана
WIDTH, HEIGHT = 1460, 700

# Константы для карточек
CARD_WIDTH, CARD_HEIGHT = 130, 200
FPS = 60
TURN_TIME = 60
MARGIN = 20

# Настройки музыки
MUSIC_VOLUME = 0.15  # Громкость музыки (15% от максимальной)
MUSIC_FADE_TIME = 1000  # Время затухания музыки в миллисекундах

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (255, 0, 255)
NEON_RED = (255, 50, 50)
HIGHLIGHT_CYAN = (0, 255, 255)
GLOW_CYAN = (0, 255, 255, 128)
NEON_GREEN = (0, 255, 255, 100)
NEON_CYAN = (0, 255, 255)
NEON_ORANGE = (255, 150, 50)

# Пути к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
FONT_DIR = os.path.join(BASE_DIR, "fonts")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
FONT_PATH = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

# Путь к фоновой музыке
BACKGROUND_MUSIC = os.path.join(MUSIC_DIR, "background.mp3")

# Словарь путей к шрифтам для pygame_gui
FONT_PATHS = {
    "NotoSans-Regular": FONT_PATH
}

# Пути к фоновым изображениям
BACKGROUND_IMAGES = {
    "main_menu": os.path.join(IMAGE_DIR, "main_menu_background.svg"),
    "rules": os.path.join(IMAGE_DIR, "rules_background.svg"),
    "game": os.path.join(IMAGE_DIR, "game_background.svg"),
    "pause": os.path.join(IMAGE_DIR, "pause_background.svg"),
    "player_win": os.path.join(IMAGE_DIR, "player_win_background.svg"),
    "hacker_win": os.path.join(IMAGE_DIR, "hacker_win_background.svg")
}

# Переменные для хранения загруженных фоновых изображений
BACKGROUNDS = {}

def load_background_images():
#Загружает и масштабирует фоновые изображения под размер экрана
    global BACKGROUNDS
    for key, path in BACKGROUND_IMAGES.items():
        try:
            image = pygame.image.load(path).convert_alpha()
            BACKGROUNDS[key] = pygame.transform.scale(image, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(f"Ошибка загрузки фона {key}: {e}")
            # Создаём заглушку (чёрный фон)
            BACKGROUNDS[key] = pygame.Surface((WIDTH, HEIGHT))
            BACKGROUNDS[key].fill(BLACK)

def load_font(size):
    try:
        return pygame.font.Font(FONT_PATH, size)
    except Exception as e:
        print(f"Ошибка загрузки шрифта: {e}")
        return pygame.font.SysFont("Arial", size)