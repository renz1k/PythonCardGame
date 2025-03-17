# cyberstorm.py
import pygame
import random
import math

try:
    from cards import ATTACK_CARDS, DEFENSE_CARDS, CARD_DESCRIPTIONS, DEFENSE_MAP
except ImportError as e:
    print(f"Ошибка импорта: {e}. Убедитесь, что файл 'cards.py' находится в той же директории и не содержит ошибок.")
    exit(1)

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1460, 700
CARD_WIDTH, CARD_HEIGHT = 130, 200
FPS = 60
TURN_TIME = 60
MARGIN = 20

# Цвета
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
NEON_RED = (255, 50, 50)
HIGHLIGHT_CYAN = (0, 255, 255)
GLOW_CYAN = (0, 255, 255, 128)

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("КиберШторм")
clock = pygame.time.Clock()

# Загрузка изображений для карт (фиксированный размер 130x200)
try:
    ATTACK_CARD_IMAGE = pygame.transform.scale(pygame.image.load("images/attack_card.jpg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
    DEFENSE_CARD_IMAGE = pygame.transform.scale(pygame.image.load("images/defense_card.jpg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
except pygame.error as e:
    print(f"Ошибка загрузки изображений: {e}. Убедитесь, что файлы 'attack_card.png' и 'defense_card.png' есть в папке 'images/'.")
    exit(1)

# Класс для кнопок
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Arial", 28, bold=True)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Класс для карты
class Card:
    def __init__(self, name, x, y, target_y=None, is_attack=False):
        self.name = name
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.base_y = y if target_y is None else target_y
        if target_y is not None:
            self.rect.y = target_y
        self.rotation = 0
        self.rotating = False
        self.show_description = False
        self.target_rotation = 0
        self.highlighted = False
        self.is_attack = is_attack  # Флаг для выбора фона: атака или защита

    def update_rotation(self):
        if self.rotation != self.target_rotation:
            self.rotation += (self.target_rotation - self.rotation) * 0.15
            if abs(self.rotation - self.target_rotation) < 1:
                self.rotation = self.target_rotation
                self.rotating = False
            self.show_description = (self.rotation >= 90 and self.rotation <= 270) or (self.rotation >= 450)
        return self.rotating

    def draw(self, surface):
        card_surface = pygame.Surface((CARD_WIDTH + 20, CARD_HEIGHT + 20), pygame.SRCALPHA)
        card_surface.fill((0, 0, 0, 0))
        
        # Выбираем фоновое изображение в зависимости от типа карты
        card_image = ATTACK_CARD_IMAGE if self.is_attack else DEFENSE_CARD_IMAGE
        
        # Рисуем фон карты
        card_surface.blit(card_image, (10, 10))
        
        # Подсветка, если карта выделена
        if self.highlighted:
            pygame.draw.rect(card_surface, GLOW_CYAN, (10, 10, CARD_WIDTH, CARD_HEIGHT), 10, border_radius=5)
        
        # Граница карты
        border_color = HIGHLIGHT_CYAN if self.highlighted else WHITE
        border_width = 6 if self.highlighted else 2
        pygame.draw.rect(card_surface, border_color, (10, 10, CARD_WIDTH, CARD_HEIGHT), border_width, border_radius=5)
        
        # Надпись на карте
        font = pygame.font.SysFont("Arial", 20, bold=True)
        words = self.name.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] < CARD_WIDTH - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)  # Белый текст для читаемости
            text_rect = text.get_rect(center=(CARD_WIDTH // 2 + 10, 25 + i * 25 + 10))
            card_surface.blit(text, text_rect)

        # Поворот и масштабирование
        scale = abs(math.cos(math.radians(self.rotation)))
        rotated_surface = pygame.transform.smoothscale(card_surface, (int((CARD_WIDTH + 20) * scale), int(CARD_HEIGHT + 20)))
        y_offset = -5 if self.highlighted else 0
        rotated_rect = rotated_surface.get_rect(center=(self.rect.centerx, self.base_y + y_offset + (CARD_HEIGHT + 20) // 2))
        
        surface.blit(rotated_surface, rotated_rect.topleft)
        self.rect = rotated_rect

# Функции игры
def select_player_cards(hacker_deck):
    required_defenses = set()
    for attack in hacker_deck:
        defense_options = list(DEFENSE_MAP[attack].keys())
        required_defenses.add(random.choice(defense_options))
    
    player_deck = list(required_defenses)
    remaining_slots = 10 - len(player_deck)
    available_defenses = [d for d in DEFENSE_CARDS if d not in player_deck]
    
    if remaining_slots > 0 and available_defenses:
        additional_cards = random.sample(available_defenses, min(remaining_slots, len(available_defenses)))
        player_deck.extend(additional_cards)
    
    return player_deck[:10]

def resolve_turn(player_card, hacker_card):
    global player_score, hacker_score
    defense_options = DEFENSE_MAP[hacker_card.name]
    if player_card.name in defense_options:
        points = defense_options[player_card.name]
        hacker_score -= points
        player_score += points
    else:
        hacker_score += 2
        player_score -= 2

def apply_blur(surface, alpha):
    blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur_surface.fill((100, 100, 100, int(alpha)))
    surface.blit(blur_surface, (0, 0))

def draw_description(surface, card, alpha):
    if not card:
        return
    font = pygame.font.SysFont("Arial", 30)
    desc = CARD_DESCRIPTIONS[card.name]
    words = desc.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] < WIDTH - 50:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    desc_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i, line in enumerate(lines[:8]):
        text = font.render(line, True, WHITE)
        text.set_alpha(int(alpha))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80 + i * 40))
        desc_surface.blit(text, text_rect)
    surface.blit(desc_surface, (0, 0))

# Главное меню
def main_menu():
    button_width, button_height = 400, 60
    start_button = Button("Начать игру", WIDTH // 2 - button_width // 2, HEIGHT // 2 - 100, button_width, button_height, NEON_BLUE, HIGHLIGHT_CYAN)
    rules_button = Button("Прочитать правила и карты", WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height, NEON_PURPLE, HIGHLIGHT_CYAN)
    exit_button = Button("Выйти из игры", WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height, NEON_RED, HIGHLIGHT_CYAN)

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

        screen.fill(BLACK)
        font = pygame.font.SysFont("Arial", 60, bold=True)
        title = font.render("КиберШторм", True, NEON_BLUE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, MARGIN + 50))
        
        start_button.draw(screen)
        rules_button.draw(screen)
        exit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Экран правил и карт
def rules_screen():
    back_button = Button("Назад", WIDTH - 150 - MARGIN, HEIGHT - 70 - MARGIN, 120, 50, NEON_RED, HIGHLIGHT_CYAN)
    font = pygame.font.SysFont("Arial", 36, bold=True)
    card_font = pygame.font.SysFont("Arial", 20)
    max_width = WIDTH - 2 * MARGIN
    line_height = 25

    content_height = 0
    lines = []

    content_height += 60
    content_height += 40
    lines.append(("Правила будут добавлены позже", WHITE, MARGIN + 60))

    content_height += 30
    lines.append(("Атакующие карты:", NEON_BLUE, content_height + MARGIN))
    content_height += 30
    for card in ATTACK_CARDS:
        desc = f"{card}: {CARD_DESCRIPTIONS[card]}"
        words = desc.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if card_font.size(test_line)[0] < max_width:
                line = test_line
            else:
                lines.append((line, NEON_BLUE, content_height + MARGIN))
                content_height += line_height
                line = word
        if line:
            lines.append((line, NEON_BLUE, content_height + MARGIN))
            content_height += line_height

    content_height += 20
    content_height += 30
    lines.append(("Защитные карты:", NEON_PURPLE, content_height + MARGIN))
    content_height += 30
    for card in DEFENSE_CARDS:
        desc = f"{card}: {CARD_DESCRIPTIONS[card]}"
        words = desc.split()
        line = ""
        for word in words:
            test_line = line + " " + word if line else word
            if card_font.size(test_line)[0] < max_width:
                line = test_line
            else:
                lines.append((line, NEON_PURPLE, content_height + MARGIN))
                content_height += line_height
                line = word
        if line:
            lines.append((line, NEON_PURPLE, content_height + MARGIN))
            content_height += line_height

    content_height += 70

    running = True
    scroll_y = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if back_button.is_clicked(event):
                return "menu"
            if event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(scroll_y - event.y * 20, max(0, content_height - HEIGHT)))

        screen.fill(BLACK)
        title = font.render("Правила и карты", True, NEON_PURPLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, MARGIN))

        for text, color, y_pos in lines:
            if MARGIN < y_pos - scroll_y < HEIGHT - MARGIN:
                screen.blit(card_font.render(text, True, color), (MARGIN, y_pos - scroll_y))

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

# Финальный экран
def final_screen(player_wins, hacker_wins):
    button_width, button_height = 400, 60
    replay_button = Button("Сыграть ещё раз", WIDTH // 2 - button_width // 2, HEIGHT - 350, button_width, button_height, NEON_BLUE, HIGHLIGHT_CYAN)
    menu_button = Button("В главное меню", WIDTH // 2 - button_width // 2, HEIGHT - 250, button_width, button_height, NEON_PURPLE, HIGHLIGHT_CYAN)
    exit_button = Button("Выйти из игры", WIDTH // 2 - button_width // 2, HEIGHT - 150, button_width, button_height, NEON_RED, HIGHLIGHT_CYAN)

    winner_text = "Победа Игрока!" if player_wins > hacker_wins else "Победа Хакера!"
    winner_color = NEON_BLUE if player_wins > hacker_wins else NEON_PURPLE
    score_text = f"Игрок {player_wins} - {hacker_wins} Хакер"

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

        screen.fill(BLACK)
        font = pygame.font.SysFont("Arial", 60, bold=True)
        winner_surface = font.render(winner_text, True, winner_color)
        score_surface = font.render(score_text, True, WHITE)
        
        screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, MARGIN + 50))
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, MARGIN + 150))
        
        replay_button.draw(screen)
        menu_button.draw(screen)
        exit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

# Основной игровой цикл
def game_screen():
    global player_score, hacker_score, rounds, player_wins, hacker_wins
    player_score = 5
    hacker_score = 5
    rounds = 0
    player_wins = 0
    hacker_wins = 0
    description_card = None
    blur_alpha = 0
    target_blur_alpha = 0
    description_alpha = 0
    target_description_alpha = 0
    turn_timer = TURN_TIME
    last_turn_start = pygame.time.get_ticks()

    hacker_deck = random.sample(ATTACK_CARDS, 10)
    hacker_deck_used = []
    player_deck = select_player_cards(hacker_deck)
    total_cards_width = len(player_deck) * CARD_WIDTH + (len(player_deck) - 1) * 10
    spacing = (WIDTH - total_cards_width) // 2
    player_cards = [Card(card, spacing + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20, is_attack=False) 
                    for i, card in enumerate(player_deck)]
    hacker_card = None

    running = True
    while running and rounds < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if hacker_card and not description_card:
                    for card in player_cards:
                        if card.rect.collidepoint(mouse_pos):
                            resolve_turn(card, hacker_card)
                            hacker_deck_used.append(hacker_card.name)
                            hacker_card = None
                            turn_timer = TURN_TIME
                            last_turn_start = pygame.time.get_ticks()
                            break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                if description_card:
                    description_card.highlighted = False
                    description_card = None
                    target_blur_alpha = 0
                    target_description_alpha = 0
                else:
                    for card in player_cards:
                        if card.rect.collidepoint(mouse_pos):
                            description_card = card
                            card.highlighted = True
                            target_blur_alpha = 200
                            target_description_alpha = 255
                            break
                    if hacker_card and hacker_card.rect.collidepoint(mouse_pos):
                        description_card = hacker_card
                        hacker_card.highlighted = True
                        target_blur_alpha = 200
                        target_description_alpha = 255

        if hacker_card is None and player_score > 0 and hacker_score > 0:
            available_hacker_cards = [card for card in hacker_deck if card not in hacker_deck_used]
            if available_hacker_cards:
                new_card = random.choice(available_hacker_cards)
                hacker_card = Card(new_card, WIDTH // 2 - CARD_WIDTH // 2, 50, is_attack=True)
                turn_timer = TURN_TIME
                last_turn_start = pygame.time.get_ticks()

        if hacker_card:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - last_turn_start) / 1000
            turn_timer = max(0, TURN_TIME - elapsed_time)
            if turn_timer <= 0:
                player_score -= 2
                hacker_score += 2
                hacker_deck_used.append(hacker_card.name)
                hacker_card = None
                turn_timer = TURN_TIME
                last_turn_start = pygame.time.get_ticks()
                if description_card:
                    description_card.highlighted = False
                    description_card = None
                    target_blur_alpha = 0
                    target_description_alpha = 0

        blur_alpha += (target_blur_alpha - blur_alpha) * 0.1
        description_alpha += (target_description_alpha - description_alpha) * 0.1

        if hacker_card:
            hacker_card.update_rotation()
        for card in player_cards:
            card.update_rotation()

        screen.fill(BLACK)
        for i in range(0, WIDTH, 50):
            pygame.draw.line(screen, NEON_PURPLE, (i, 0), (i, HEIGHT), 1)
        for i in range(0, HEIGHT, 50):
            pygame.draw.line(screen, NEON_BLUE, (0, i), (WIDTH, i), 1)

        font = pygame.font.SysFont("Arial", 36, bold=True)
        player_text = font.render(f"Игрок: {player_score}", True, NEON_BLUE)
        hacker_text = font.render(f"Хакер: {hacker_score}", True, NEON_PURPLE)
        round_text = font.render(f"Раунд: {rounds + 1}", True, WHITE)
        remaining_hacker_cards = len(hacker_deck) - len(hacker_deck_used)
        hacker_cards_text = font.render(f"Карт хакера: {remaining_hacker_cards}", True, NEON_PURPLE)
        timer_text = font.render(f"Время: {int(turn_timer)}", True, NEON_RED)

        screen.blit(player_text, (MARGIN, MARGIN))
        screen.blit(hacker_text, (WIDTH - hacker_text.get_width() - MARGIN, MARGIN))
        screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, MARGIN))
        screen.blit(hacker_cards_text, (WIDTH - hacker_cards_text.get_width() - MARGIN, MARGIN + 40))
        screen.blit(timer_text, (MARGIN, MARGIN + 40))

        if hacker_card:
            hacker_card.draw(screen)
        for card in player_cards:
            card.draw(screen)

        if blur_alpha > 0:
            apply_blur(screen, blur_alpha)
        if description_alpha > 0:
            draw_description(screen, description_card, description_alpha)

        if player_score <= 0 or hacker_score <= 0 or len(hacker_deck_used) >= 10:
            rounds += 1
            if player_score <= 0:
                hacker_wins += 1
            elif hacker_score <= 0:
                player_wins += 1
            elif len(hacker_deck_used) >= 10:
                if player_score > hacker_score:
                    player_wins += 1
                else:
                    hacker_wins += 1
            player_score = 5
            hacker_score = 5
            hacker_card = None
            if description_card:
                description_card.highlighted = False
            description_card = None
            blur_alpha = 0
            target_blur_alpha = 0
            description_alpha = 0
            target_description_alpha = 0
            turn_timer = TURN_TIME
            last_turn_start = pygame.time.get_ticks()
            hacker_deck = random.sample(ATTACK_CARDS, 10)
            hacker_deck_used = []
            player_deck = select_player_cards(hacker_deck)
            total_cards_width = len(player_deck) * CARD_WIDTH + (len(player_deck) - 1) * 10
            spacing = (WIDTH - total_cards_width) // 2
            player_cards = [Card(card, spacing + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 20, is_attack=False) 
                            for i, card in enumerate(player_deck)]
            pygame.time.wait(1000)

        if player_wins >= 2 or hacker_wins >= 2:
            return final_screen(player_wins, hacker_wins)

        pygame.display.flip()
        clock.tick(FPS)

    return "menu"

# Основной цикл программы
state = "menu"
running = True
while running:
    if state == "menu":
        state = main_menu()
    elif state == "game":
        state = game_screen()
    elif state == "rules":
        state = rules_screen()
    elif state == "exit":
        running = False

pygame.quit()