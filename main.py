import pygame

# Инициализация pygame и создание дисплея
pygame.init()
pygame.mixer.init()  # Инициализируем звуковую систему
pygame.mixer.music.load("music/background.mp3")  # Загружаем фоновую музыку
pygame.mixer.music.set_volume(0.3)  # Устанавливаем громкость (0.0 - 1.0)
pygame.mixer.music.play(-1)  # Включаем музыку в бесконечный цикл
from settings import WIDTH, HEIGHT
pygame.display.set_mode((WIDTH, HEIGHT))

# После этого импортируем остальные модули,
# в которых происходит загрузка изображений (например, card.py)
from menu import main_menu, rules_screen, final_screen, pause_menu
from game import game_screen

def main():
    state = "menu"
    running = True
    while running:
        if state == "menu":
            state = main_menu()
        elif state == "game":
            state = game_screen()
        elif state == "rules":
            state = rules_screen()
        elif state == "pause":
            state = pause_menu()
        elif state == "exit":
            running = False
    pygame.quit()

if __name__ == "__main__":
    main()
