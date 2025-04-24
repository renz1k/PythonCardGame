# game.py
import random
import pygame
from settings import *
from card import Card, select_player_cards, resolve_turn, apply_blur, draw_description
from menu import pause_menu, final_screen
from cards import ATTACK_CARDS

player_score = 5
hacker_score = 5
rounds = 0
player_wins = 0
hacker_wins = 0

def game_screen(manager, screen):
    # Очищаем элементы интерфейса перед началом игры
    manager.clear_and_reset()

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

    clock = pygame.time.Clock()
    running = True

    while running and rounds < 3:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit", player_wins, hacker_wins

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_menu(manager, screen)
                    if result == "menu":
                        return "menu", player_wins, hacker_wins
                    elif result == "resume":
                        manager.clear_and_reset()  # Очищаем элементы паузы
                        last_turn_start = pygame.time.get_ticks()
                    elif result == "exit":
                        return "exit", player_wins, hacker_wins

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if hacker_card and not description_card:
                    for card in player_cards:
                        if card.rect.collidepoint(mouse_pos):
                            player_score, hacker_score = resolve_turn(card, hacker_card, player_score, hacker_score)
                            hacker_deck_used.append(hacker_card.name)
                            hacker_card = None
                            turn_timer = TURN_TIME
                            last_turn_start = pygame.time.get_ticks()
                            break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
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

            manager.process_events(event)

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

        screen.blit(BACKGROUNDS["game"], (0, 0))  # Отображаем фоновое изображение

        font = load_font(36)
        # Отрисовка раунда по центру сверху с отступом
        round_text = font.render(f"Раунд: {rounds + 1}", True, WHITE)
        screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 10))

        # Отрисовка счета игрока с тенью
        player_text = font.render(f"Игрок: {player_score}", True, NEON_BLUE)
        player_shadow = font.render(f"Игрок: {player_score}", True, (0, 100, 150))
        screen.blit(player_shadow, (MARGIN + 2, MARGIN + 2))
        screen.blit(player_text, (MARGIN, MARGIN))

        # Отрисовка счета хакера с тенью
        hacker_text = font.render(f"Хакер: {hacker_score}", True, NEON_RED)
        hacker_shadow = font.render(f"Хакер: {hacker_score}", True, (100, 0, 0))
        screen.blit(hacker_shadow, (WIDTH - hacker_text.get_width() - MARGIN + 2, MARGIN + 2))
        screen.blit(hacker_text, (WIDTH - hacker_text.get_width() - MARGIN, MARGIN))

        # Отрисовка оставшихся карт хакера с тенью
        remaining_hacker_cards = len(hacker_deck) - len(hacker_deck_used)
        hacker_cards_text = font.render(f"Карт хакера: {remaining_hacker_cards}", True, NEON_RED)
        hacker_cards_shadow = font.render(f"Карт хакера: {remaining_hacker_cards}", True, (100, 0, 0))
        screen.blit(hacker_cards_shadow, (WIDTH - hacker_cards_text.get_width() - MARGIN + 2, MARGIN + 45))
        screen.blit(hacker_cards_text, (WIDTH - hacker_cards_text.get_width() - MARGIN, MARGIN + 45))

        # Отрисовка таймера с тенью и анимацией при малом времени
        timer_color = NEON_ORANGE if turn_timer <= 10 else NEON_CYAN
        timer_shadow_color = (100, 50, 0) if turn_timer <= 10 else (0, 100, 100)
        timer_text = font.render(f"Время: {int(turn_timer)}", True, timer_color)
        timer_shadow = font.render(f"Время: {int(turn_timer)}", True, timer_shadow_color)
        screen.blit(timer_shadow, (MARGIN + 2, MARGIN + 45))
        screen.blit(timer_text, (MARGIN, MARGIN + 45))

        if hacker_card:
            hacker_card.draw(screen)
        for card in player_cards:
            card.draw(screen)

        if blur_alpha > 0:
            apply_blur(screen, blur_alpha, WIDTH, HEIGHT)
        if description_alpha > 0:
            draw_description(screen, description_card, description_alpha, WIDTH, HEIGHT)

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
            return "final", player_wins, hacker_wins

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
    return "menu", player_wins, hacker_wins