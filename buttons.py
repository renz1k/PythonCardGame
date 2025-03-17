import pygame

from settings import WHITE, BLACK, load_font


class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = load_font(28)
        self.hovered = False  # Флаг для анимации

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Цвет кнопки
        current_color = self.hover_color if self.hovered else self.color

        # Рисуем тень (чёрный прямоугольник слегка ниже кнопки)
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(surface, BLACK, shadow_rect, border_radius=12)

        # Рисуем кнопку с закруглёнными краями
        pygame.draw.rect(surface, current_color, self.rect, border_radius=12)

        # Рисуем границу кнопки (если на неё навели)
        if self.hovered:
            pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=12)

        # Рисуем текст кнопки по центру
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """ Проверяет, была ли нажата кнопка """
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
