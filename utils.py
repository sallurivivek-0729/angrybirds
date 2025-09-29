import pygame
from config import *

def draw_text(surface, text, font_size, color, x, y):
    """Draw text on the given surface."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_menu_buttons(screen):
    """Draws the main menu buttons."""
    font_size = 50
    draw_text(screen, "Start Game", font_size, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60)
    draw_text(screen, "Instructions", font_size, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text(screen, "Exit", font_size, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60)

def draw_name_entry_screen(screen, background_image):
    """Draws the player name entry screen."""
    screen.blit(background_image, (0, 0))
    draw_text(screen, "Enter Player Names and Press Enter:", 60, WHITE, SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 100)