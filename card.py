import math
import random

import pygame

from cards import DEFENSE_CARDS, CARD_DESCRIPTIONS, DEFENSE_MAP
from settings import CARD_WIDTH, CARD_HEIGHT, WHITE, HIGHLIGHT_CYAN, GLOW_CYAN
from settings import IMAGE_DIR
from settings import load_font

# Загрузка изображений для карт
try:
    ATTACK_CARD_IMAGE = pygame.transform.scale(
        pygame.image.load(f"{IMAGE_DIR}/attack_card.jpg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
    DEFENSE_CARD_IMAGE = pygame.transform.scale(
        pygame.image.load(f"{IMAGE_DIR}/defense_card.jpg").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT))
except pygame.error as e:
    print(f"Ошибка загрузки изображений: {e}")
    exit(1)

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
        self.is_attack = is_attack  # Для выбора фона карты

    def update_rotation(self):
        if self.rotation != self.target_rotation:
            self.rotation += (self.target_rotation - self.rotation) * 0.15
            if abs(self.rotation - self.target_rotation) < 1:
                self.rotation = self.target_rotation
                self.rotating = False
            self.show_description = (90 <= self.rotation <= 270) or (self.rotation >= 450)
        return self.rotating

    def draw(self, surface):
        card_surface = pygame.Surface((CARD_WIDTH + 20, CARD_HEIGHT + 20), pygame.SRCALPHA)
        card_surface.fill((0, 0, 0, 0))
        card_image = ATTACK_CARD_IMAGE if self.is_attack else DEFENSE_CARD_IMAGE
        card_surface.blit(card_image, (10, 10))
        if self.highlighted:
            pygame.draw.rect(card_surface, GLOW_CYAN, (10, 10, CARD_WIDTH, CARD_HEIGHT), 10, border_radius=5)
        border_color = HIGHLIGHT_CYAN if self.highlighted else WHITE
        border_width = 6 if self.highlighted else 2
        pygame.draw.rect(card_surface, border_color, (10, 10, CARD_WIDTH, CARD_HEIGHT), border_width, border_radius=5)
        font = load_font(20)
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
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(CARD_WIDTH // 2 + 10, 25 + i * 25 + 10))
            card_surface.blit(text, text_rect)
        scale = abs(math.cos(math.radians(self.rotation)))
        rotated_surface = pygame.transform.smoothscale(card_surface, (int((CARD_WIDTH + 20) * scale), int(CARD_HEIGHT + 20)))
        y_offset = -5 if self.highlighted else 0
        rotated_rect = rotated_surface.get_rect(center=(self.rect.centerx, self.base_y + y_offset + (CARD_HEIGHT + 20) // 2))
        surface.blit(rotated_surface, rotated_rect.topleft)
        self.rect = rotated_rect

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
