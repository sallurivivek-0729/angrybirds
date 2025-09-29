import pygame
import random
from config import *

def generation(rows, cols, block_size, x_offset, y_offset):
    """Generates blocks for the fortress layout."""
    fortress = []
    for row in range(rows):
        for col in range(cols):
            block_type = random.choice(["wood", "stone", "ice"])
            block_health = {"wood": 100, "stone": 150, "ice": 50}[block_type]
            block_color = {"wood": YELLOW, "stone": BLUE, "ice": WHITE}[block_type]

            block = {
                "rect": pygame.Rect(x_offset + col * block_size, y_offset + row * block_size, block_size, block_size),
                "type": block_type,
                "health": block_health,
                "color": block_color,
            }
            fortress.append(block)
    return fortress

def render(screen, fortress):
    """Draws fortress blocks and their health bars."""
    for block in fortress:
        pygame.draw.rect(screen, block["color"], block["rect"])
        # Health bar
        health_ratio = block["health"] / {"wood": 100, "stone": 150, "ice": 50}[block["type"]]
        health_bar_width = int(block["rect"].width * health_ratio)
        pygame.draw.rect(screen, RED, (block["rect"].x, block["rect"].y - 5, health_bar_width, 5))

def check_collision(projectile_rect, fortress):
    """Checks for collisions and applies damage to blocks."""
    for block in fortress:
        if projectile_rect.colliderect(block["rect"]):
            block["health"] -= 50
            if block["health"] <= 0:
                fortress.remove(block)
            return True
    return False