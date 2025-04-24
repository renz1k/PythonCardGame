# menu.py
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UITextBox
from settings import WIDTH, HEIGHT, BLACK, NEON_BLUE, NEON_PURPLE, load_font, BACKGROUNDS, MUSIC_VOLUME
from cards import RULES_TEXT, ATTACK_CARDS_TEXT, DEFENSE_CARDS_TEXT

def main_menu(manager, screen):
    manager.clear_and_reset()
    title_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 200, 100), (400, 80)),
        text="КиберШторм",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@title_label", object_id="#title")
    )
    
    # Добавляем надпись "Громкость"
    volume_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT - 90), (150, 35)),
        text="Громкость:",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@score_label", object_id="#volume_label")
    )
    
    # Добавляем ползунок громкости
    volume_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, HEIGHT - 55), (200, 30)),
        start_value=pygame.mixer.music.get_volume(),
        value_range=(0.0, 1.0),
        manager=manager
    )
    
    start_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 - 100), (300, 60)),
        text="Начать игру",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#start_button")
    )
    
    rules_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2), (300, 60)),
        text="Правила",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#rules_button")
    )
    
    exit_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 100), (300, 60)),
        text="Выйти",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#exit_button")
    )
    
    result = "menu"
    clock = pygame.time.Clock()

    while result == "menu":
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return "game"
                elif event.ui_element == rules_button:
                    return "rules"
                elif event.ui_element == exit_button:
                    return "exit"
            
            # Обработка изменения громкости
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == volume_slider:
                    pygame.mixer.music.set_volume(event.value)
            
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(BACKGROUNDS["main_menu"], (0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()

def rules_screen(manager, screen):
    manager.clear_and_reset()
    
    # Создаем заголовок с отступом сверху
    title_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 200, 40), (400, 60)),
        text="Правила игры",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@rules_title", object_id="#rules_title")
    )
    
    # Создаем текстовое окно с отступами от краев и заголовка
    rules_text = f"Правила игры:<br>{RULES_TEXT}<br><br>Атакующие карты:<br>{ATTACK_CARDS_TEXT}<br><br>Защитные карты:<br>{DEFENSE_CARDS_TEXT}"
    rules_box = UITextBox(
        html_text=rules_text,
        relative_rect=pygame.Rect((50, 120, WIDTH - 100, HEIGHT - 220)),
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@text_box", object_id="#rules_text")
    )
    
    # Кнопка "Назад" с отступом снизу
    back_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, HEIGHT - 80), (200, 50)),
        text="Назад",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@back_button", object_id="#back_button")
    )
    
    result = "rules"
    clock = pygame.time.Clock()

    while result == "rules":
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    return "menu"
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(BACKGROUNDS["rules"], (0, 0))  # Отображаем фоновое изображение
        manager.draw_ui(screen)
        pygame.display.flip()

def final_screen(manager, screen, player_wins, hacker_wins):
    manager.clear_and_reset()
    
    winner = "Хакер" if hacker_wins > player_wins else "Игрок"
    background_key = "hacker_win" if hacker_wins > player_wins else "player_win"
    
    # Создаем разные стили для победителя хакера и игрока
    if hacker_wins > player_wins:
        winner_style = "@winner_label_hacker"
    else:
        winner_style = "@winner_label_player"
    
    winner_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 250, HEIGHT // 2 - 150), (500, 80)),
        text=f"Победитель: {winner}!",
        manager=manager,
        object_id=winner_style
    )
    
    score_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 200, HEIGHT // 2 - 50), (400, 40)),
        text=f"Счёт: Игрок {player_wins} - {hacker_wins} Хакер",
        manager=manager,
        object_id="@score_label"
    )
    
    replay_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 20), (300, 60)),
        text="Играть снова",
        manager=manager,
        object_id="@menu_button"
    )
    
    menu_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 90), (300, 60)),
        text="Главное меню",
        manager=manager,
        object_id="@menu_button"
    )
    
    exit_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 160), (300, 60)),
        text="Выйти",
        manager=manager,
        object_id="@menu_button"
    )
    result = "final"
    clock = pygame.time.Clock()

    while result == "final":
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == replay_button:
                    return "game"
                elif event.ui_element == menu_button:
                    return "menu"
                elif event.ui_element == exit_button:
                    return "exit"
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(BACKGROUNDS[background_key], (0, 0))  # Отображаем фоновое изображение
        manager.draw_ui(screen)
        pygame.display.flip()

def pause_menu(manager, screen):
    manager.clear_and_reset()
    
    # Создаем заголовок паузы с новым стилем
    pause_label = UILabel(
        relative_rect=pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 150), (200, 50)),
        text="Пауза",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@pause_title", object_id="#pause_title")
    )
    
    continue_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 - 50), (300, 60)),
        text="Продолжить",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#continue_button")
    )
    
    menu_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 20), (300, 60)),
        text="Главное меню",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#menu_button")
    )
    
    # Кнопка музыки
    music_state = "Выкл" if pygame.mixer.music.get_volume() == 0 else "Вкл"
    music_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 90), (300, 60)),
        text=f"Музыка: {music_state}",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#music_button")
    )
    
    exit_button = UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 160), (300, 60)),
        text="Выйти",
        manager=manager,
        object_id=pygame_gui.core.ObjectID(class_id="@menu_button", object_id="#exit_button")
    )
    
    result = "pause"
    clock = pygame.time.Clock()

    while result == "pause":
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == continue_button:
                    return "resume"
                elif event.ui_element == menu_button:
                    return "menu"
                elif event.ui_element == exit_button:
                    return "exit"
                elif event.ui_element == music_button:
                    # Переключаем состояние музыки
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                        music_button.set_text("Музыка: Выкл")
                    else:
                        pygame.mixer.music.set_volume(MUSIC_VOLUME)
                        music_button.set_text("Музыка: Вкл")
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(BACKGROUNDS["pause"], (0, 0))  # Отображаем фоновое изображение
        manager.draw_ui(screen)
        pygame.display.flip()