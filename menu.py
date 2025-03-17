import pygame
from buttons import Button
from cards import RULES_TEXT, ATTACK_CARDS_TEXT, DEFENSE_CARDS_TEXT  # Импортируем текст правил и карт
from settings import WIDTH, HEIGHT, MARGIN, NEON_BLUE, NEON_PURPLE, NEON_RED, BLACK, load_font, FPS, WHITE, NEON_GREEN, \
    NEON_CYAN, NEON_ORANGE


def main_menu():
    button_width, button_height = 400, 70  # Увеличили высоту кнопок
    start_button = Button("Начать игру", WIDTH // 2 - button_width // 2, HEIGHT // 2 - 120, button_width, button_height, NEON_BLUE, NEON_PURPLE)
    rules_button = Button("Правила", WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height, NEON_GREEN, NEON_CYAN)
    exit_button = Button("Выйти", WIDTH // 2 - button_width // 2, HEIGHT // 2 + 120, button_width, button_height, NEON_RED, NEON_ORANGE)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if start_button.is_clicked(event):
                return "game"
            if rules_button.is_clicked(event):
                return "rules"
            if exit_button.is_clicked(event):
                return "exit"

        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        title_font = load_font(60)
        title = title_font.render("КиберШторм", True, NEON_BLUE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Отрисовка кнопок
        start_button.draw(screen)
        rules_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


from cards import RULES_TEXT, ATTACK_CARDS_TEXT, DEFENSE_CARDS_TEXT
from settings import WHITE, NEON_RED, NEON_GREEN, NEON_PURPLE


def rules_screen():
    back_button = Button("Назад", WIDTH - 150 - MARGIN, HEIGHT - 70 - MARGIN, 120, 50, NEON_RED, NEON_RED)
    font = load_font(36)
    text_font = load_font(20)

    # Разбиваем текст атакующих и защитных карт на строки
    formatted_attack_text = "\n\n".join(ATTACK_CARDS_TEXT.split("\n"))
    formatted_defense_text = "\n\n".join(DEFENSE_CARDS_TEXT.split("\n"))

    # Создаём список строк с цветом для каждого раздела
    sections = [
        (RULES_TEXT, WHITE),  # Белый текст для правил
        ("\n", NEON_RED),  # Красный заголовок
        (formatted_attack_text, NEON_RED),  # Красный текст атакующих карт
        ("\n", NEON_GREEN),  # Зелёный заголовок
        (formatted_defense_text, NEON_GREEN)  # Зелёный текст защитных карт
    ]

    # Максимальная ширина текста
    max_width = WIDTH - 2 * MARGIN

    lines = []
    for section_text, color in sections:
        section_lines = section_text.split("\n")
        for idx, line in enumerate(section_lines):
            # Разбиваем строку на несколько частей, если она слишком длинная
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if text_font.size(test_line)[0] < max_width:  # Проверяем ширину строки
                    current_line = test_line
                else:
                    lines.append((current_line, color))  # Сохраняем строку с цветом
                    current_line = word  # Начинаем новую строку
            if current_line:
                lines.append((current_line, color))  # Добавляем последнюю строку

            # Добавляем отступ между строками в каждой секции
            if idx < len(section_lines) - 1:  # Не добавляем отступ после последней строки секции
                lines.append(("", WHITE))  # Пустая строка для отступа

        # Добавляем отступ после каждой секции
        lines.append(("", WHITE))  # Пустая строка для отступа между секциями

    clock = pygame.time.Clock()
    scroll_y = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if back_button.is_clicked(event):
                return "menu"
            if event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, scroll_y - event.y * 20)

        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        title = font.render("Правила игры", True, NEON_PURPLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, MARGIN))

        y_offset = MARGIN + 60 - scroll_y
        for line, color in lines:
            text_surface = text_font.render(line, True, color)
            screen.blit(text_surface, (MARGIN, y_offset))
            y_offset += text_surface.get_height() + 5  # Отступ между строками

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def final_screen(player_wins, hacker_wins):
    button_width, button_height = 400, 70
    replay_button = Button("Сыграть ещё раз", WIDTH // 2 - button_width // 2, HEIGHT - 300, button_width, button_height, NEON_BLUE, NEON_PURPLE)
    menu_button = Button("В главное меню", WIDTH // 2 - button_width // 2, HEIGHT - 200, button_width, button_height, NEON_GREEN, NEON_CYAN)
    exit_button = Button("Выйти", WIDTH // 2 - button_width // 2, HEIGHT - 100, button_width, button_height, NEON_RED, NEON_ORANGE)

    winner_text = "Победа Игрока!" if player_wins > hacker_wins else "Победа Хакера!"
    winner_color = NEON_GREEN if player_wins > hacker_wins else NEON_RED
    score_text = f"Игрок {player_wins} - {hacker_wins} Хакер" 
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if replay_button.is_clicked(event):
                return "game"
            if menu_button.is_clicked(event):
                return "menu"
            if exit_button.is_clicked(event):
                return "exit"

        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        font = load_font(60)
        winner_surface = font.render(winner_text, True, winner_color)
        score_surface = font.render(score_text, True, WHITE)  # Рендерим счёт

        screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, 100))  # Текст победителя
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 180))    # Счёт ниже

        replay_button.draw(screen)
        menu_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)



def pause_menu():
    button_width, button_height = 350, 70
    continue_button = Button("Продолжить", WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height, NEON_GREEN, NEON_CYAN)
    menu_button = Button("Главное меню", WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height, NEON_RED, NEON_ORANGE)

    clock = pygame.time.Clock()
    paused = True
    # Запоминаем время начала паузы
    pause_start = pygame.time.get_ticks()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if continue_button.is_clicked(event):
                # Вычисляем длительность паузы и возвращаем её для корректировки таймера
                pause_duration = pygame.time.get_ticks() - pause_start
                return "resume", pause_duration
            if menu_button.is_clicked(event):
                return "menu"

        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        title_font = load_font(60)
        title = title_font.render("Пауза", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))

        continue_button.draw(screen)
        menu_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
