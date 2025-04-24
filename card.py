# card.py
import math
import random
import pygame
import pyphen
from cards import DEFENSE_CARDS, CARD_DESCRIPTIONS, DEFENSE_MAP
from settings import CARD_WIDTH, CARD_HEIGHT, WHITE, HIGHLIGHT_CYAN, GLOW_CYAN, IMAGE_DIR, load_font

# Переменные для изображений (пока None)
ATTACK_CARD_IMAGE = None
DEFENSE_CARD_IMAGE = None

hyphenator = pyphen.Pyphen(lang='ru')

def load_card_images():
    global ATTACK_CARD_IMAGE, DEFENSE_CARD_IMAGE
    try:
        ATTACK_CARD_IMAGE = pygame.transform.scale(
            pygame.image.load(f"{IMAGE_DIR}/attack_card.svg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
        DEFENSE_CARD_IMAGE = pygame.transform.scale(
            pygame.image.load(f"{IMAGE_DIR}/defense_card.svg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
    except pygame.error as e:
        print(f"Ошибка загрузки изображений: {e}")
        # Вместо exit(1) создадим заглушки
        ATTACK_CARD_IMAGE = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        ATTACK_CARD_IMAGE.fill((255, 0, 0))  # Красный цвет для заглушки
        DEFENSE_CARD_IMAGE = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        DEFENSE_CARD_IMAGE.fill((0, 0, 255))  # Синий цвет для заглушки

def split_into_syllables(word):
    vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
    consonants = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ"
    soft_sign = "ьЬ"
    hard_sign = "ъЪ"
    
    syllables = []
    current_syllable = ""
    i = 0
    
    while i < len(word):
        current_syllable += word[i]
        
        # Если текущая буква гласная
        if word[i] in vowels:
            # Если это не последняя буква
            if i < len(word) - 1:
                next_char = word[i + 1]
                
                # Если следующая буква согласная
                if next_char in consonants:
                    # Проверяем следующую букву после согласной
                    if i + 2 < len(word):
                        after_next = word[i + 2]
                        # Если после согласной идет гласная, включаем согласную в текущий слог
                        if after_next in vowels:
                            current_syllable += next_char
                            i += 1
                        # Если после согласной идет согласная, делим после гласной
                        else:
                            syllables.append(current_syllable)
                            current_syllable = ""
                    else:
                        # Если это предпоследняя буква, включаем последнюю согласную в слог
                        current_syllable += next_char
                        i += 1
                # Если следующая буква мягкий или твёрдый знак
                elif next_char in soft_sign + hard_sign:
                    current_syllable += next_char
                    i += 1
                else:
                    syllables.append(current_syllable)
                    current_syllable = ""
            else:
                syllables.append(current_syllable)
                current_syllable = ""
        i += 1
    
    # Добавляем оставшиеся буквы в последний слог
    if current_syllable:
        if syllables:
            syllables[-1] += current_syllable
        else:
            syllables.append(current_syllable)
    
    return syllables

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
        self.is_attack = is_attack

    def update_rotation(self):
        if self.rotation != self.target_rotation:
            self.rotation += (self.target_rotation - self.rotation) * 0.15
            if abs(self.rotation - self.target_rotation) < 1:
                self.rotation = self.target_rotation
                self.rotating = False
            self.show_description = (90 <= self.rotation <= 270) or (self.rotation >= 450)
        return self.rotating

    @staticmethod
    def wrap_text(text, font, max_width):
        text = text.replace("-", " ")
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if not word:
                continue

            test_line = f"{current_line} {word}".strip()

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if font.size(word)[0] > max_width:
                    if current_line:
                        lines.append(current_line)
                    current_line = ""
                    hyphenated_parts = hyphenator.inserted(word, hyphen="-").split("-")

                    temp_part = ""
                    for part in hyphenated_parts:
                        test_part = f"{temp_part}{part}".strip()

                        if font.size(test_part + "-")[0] <= max_width:
                            temp_part = test_part
                        else:
                            if temp_part:
                                lines.append(temp_part + "-")
                            temp_part = part

                    if temp_part:
                        lines.append(temp_part)

                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw(self, surface):
        card_surface = pygame.Surface((CARD_WIDTH + 20, CARD_HEIGHT + 20), pygame.SRCALPHA)
        card_surface.fill((0, 0, 0, 0))
        
        # Создаем маску с закругленными углами
        mask_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        mask_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, CARD_WIDTH, CARD_HEIGHT), border_radius=10)
        
        # Создаем поверхность для карты с применением маски
        card_image = ATTACK_CARD_IMAGE if self.is_attack else DEFENSE_CARD_IMAGE
        masked_card = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        masked_card.blit(card_image, (0, 0))
        masked_card.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        
        # Отображаем закругленную карту
        card_surface.blit(masked_card, (10, 10))
        
        if self.highlighted:
            # Внешняя мягкая подсветка (полупрозрачная)
            soft_glow = (100, 200, 255, 80)  # Более мягкий голубой цвет с меньшей прозрачностью
            pygame.draw.rect(card_surface, soft_glow, (10, 10, CARD_WIDTH, CARD_HEIGHT), 4, border_radius=10)
            
            # Внутренняя обводка (более тонкая)
            inner_highlight = (150, 220, 255)  # Нежно-голубой цвет
            pygame.draw.rect(card_surface, inner_highlight, (10, 10, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=10)
        else:
            # Обычная обводка
            pygame.draw.rect(card_surface, WHITE, (10, 10, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=10)
        
        font = load_font(18)
        lines = Card.wrap_text(self.name, font, CARD_WIDTH - 20)
        
        line_height = 18
        total_text_height = len(lines) * line_height - (line_height - font.get_height())
        
        start_y = (CARD_HEIGHT - total_text_height) // 2 + 10
        
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(CARD_WIDTH // 2 + 10, start_y + i * line_height))
            card_surface.blit(text, text_rect)
        
        scale = abs(math.cos(math.radians(self.rotation)))
        rotated_surface = pygame.transform.smoothscale(card_surface, (int((CARD_WIDTH + 20) * scale), int(CARD_HEIGHT + 20)))
        y_offset = -5 if self.highlighted else 0
        rotated_rect = rotated_surface.get_rect(center=(self.rect.centerx, self.base_y + y_offset + (CARD_HEIGHT + 20) // 2))
        surface.blit(rotated_surface, rotated_rect.topleft)
        self.rect = rotated_rect

import random
from cards import DEFENSE_CARDS, DEFENSE_MAP

def select_player_cards(hacker_deck):
    """
    Для каждой атаки из hacker_deck гарантированно выбираем
    по одной соответствующей защите, затем добираем случайные
    карты до 10 и перемешиваем колоду.
    """
    # Шаг A: для каждой атаки выбираем ровно одну защиту
    required = []
    for attack in hacker_deck:
        options = list(DEFENSE_MAP[attack].keys())
        choice = random.choice(options)
        required.append(choice)

    # Убираем дубликаты, сохраняя порядок
    unique_required = []
    for card in required:
        if card not in unique_required:
            unique_required.append(card)

    # Шаг B: формируем начальную колоду игрока
    player_deck = unique_required.copy()

    # Шаг C: добираем до 10 карт из оставшихся защит
    if len(player_deck) < 10:
        remaining = 10 - len(player_deck)
        available = [d for d in DEFENSE_CARDS if d not in player_deck]
        extras = random.sample(available, min(remaining, len(available)))
        player_deck.extend(extras)

    # (случай, когда unique_required > 10 не возможен, т.к. hacker_deck ровно 10 атак)

    # Шаг D: финальная перетусовка
    random.shuffle(player_deck)
    return player_deck
    
def resolve_turn(player_card, hacker_card, player_score, hacker_score):
    defense_options = DEFENSE_MAP[hacker_card.name]
    if player_card.name in defense_options:
        points = defense_options[player_card.name]
        hacker_score -= points
        player_score += points
    else:
        hacker_score += 2
        player_score -= 2
    return player_score, hacker_score

def apply_blur(surface, alpha, width, height):
    blur_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    blur_surface.fill((100, 100, 100, int(alpha)))
    surface.blit(blur_surface, (0, 0))

def draw_description(surface, card, alpha, width, height):
    if not card:
        return
    font = load_font(30)
    desc = CARD_DESCRIPTIONS[card.name]
    words = desc.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] < width - 50:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    desc_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i, line in enumerate(lines[:8]):
        text = font.render(line, True, WHITE)
        text.set_alpha(int(alpha))
        text_rect = text.get_rect(center=(width // 2, height // 2 - 80 + i * 40))
        desc_surface.blit(text, text_rect)
    surface.blit(desc_surface, (0, 0))