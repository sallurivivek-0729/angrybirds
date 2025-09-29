import pygame
import sys
from ui import draw
from assets_loader import load_image
import random
from config import *

def main_menu( screen, background_path):
    background = load_image(background_path, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))
    start_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 - 50, 200, 50)
    exit_button = pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 200, 50)

    pygame.draw.rect(screen, (0, 255, 0), start_button)
    pygame.draw.rect(screen, (255, 0, 0), exit_button)
    draw(screen, "Start Game", 30, (255, 255, 255), start_button.x + 50, start_button.y + 10)
    draw(screen, "Exit", 30, (255, 255, 255), exit_button.x + 70, exit_button.y + 10)

    pygame.display.flip()
    return start_button, exit_button


def name_entry(screen, background_path):
    background = load_image(background_path, (screen.get_width(), screen.get_height()))
    screen.blit(background, (0, 0))

    player_names = ["", ""]
    current_player = 0

    font = pygame.font.Font(None, 40)

    while True:
        screen.blit(background, (0, 0))
        draw(screen, f"Enter Player {current_player + 1} Name:", 40, (255, 255, 255), screen.get_width() // 2 - 150, screen.get_height() // 2 - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_player += 1
                    if current_player == len(player_names):
                        return player_names
                elif event.key == pygame.K_BACKSPACE:
                    player_names[current_player] = player_names[current_player][:-1]
                else:
                    player_names[current_player] += event.unicode

        draw(screen, player_names[current_player], 30, (0, 255, 0), screen.get_width() // 2 - 150, screen.get_height() // 2)
        pygame.display.flip()


def render_bird_options(screen, birds, x_start, y_start, projectile_images):
    for i, bird in enumerate(birds):
        bird_x = x_start + i * 50
        bird_y = y_start
        screen.blit(projectile_images[bird], (bird_x, bird_y))
        pygame.draw.rect(screen, (255, 255, 255), (bird_x, bird_y, 40, 40), 1)


def generation(rows, cols, blw, x_start, y_start, blocks  ):
    fortress = []
    for row in range(rows):
        for col in range(cols):
            block_type = random.choice(blocks)  # Randomly choose a block type
            rect = pygame.Rect( x_start + col * blw, y_start + row * blw, blw , blw)
            block = {
                "rect": rect,
                "image": block_type,
                "health": random.choice([3, 2, 1])  # Assign random health
            }
            fortress.append(block)
    return fortress


def render(screen, fortress):
    for block in fortress:
        screen.blit(block["image"], block["rect"]) # Render block image

        # Render health bar above the block
        health = block["health"]
        health_bar_color = (0, 255, 0) if health == 3 else (255, 255, 0) if health == 2 else (255, 0, 0)
        health_bar_width = block["rect"].width * (health / 3)  # Scale health bar width based on health
        health_bar_rect = pygame.Rect(block["rect"].x, block["rect"].y - 8, health_bar_width, 5)
        pygame.draw.rect( screen, health_bar_color, health_bar_rect  )


def check_collision(rect, fortress):
    for block in fortress:
        if rect.colliderect(block["rect"]):  # If collision happens
            block["health"] -= 1  # Decrease health by 1
            if block["health"] <= 0:  # Remove block if health is 0
                fortress.remove(block)
            return True
    return False
def resizeimages(image_paths, blw, blh):
    resized_images = []
    for path in image_paths:
        image = pygame.image.load(path).convert_alpha()  # Load image
        resized_image = pygame.transform.scale( image, (blw, blh))  # Resize image
        resized_images.append(resized_image)
    return resized_images
def winscreen(screen, winner):
    end_screen_image = pygame.image.load( BACKGROUND_PATH+"end_screen.jpg" ).convert_alpha()  # Replace with your image path
    end_screen_image = pygame.transform.scale(end_screen_image , (W, H))  # Scale to screen size

    screen.blit( end_screen_image, (0, 0))  # Render the end screen image

    font = pygame.font.Font(None, 74)  # Font for text
    winner_text = f"{winner} Wins!"
    instruction_text = "Press ENTER to exit."

    # Render winner message
    winner_surface =font.render(winner_text, True, (255, 255, 255))  # White text
    instruction_surface =font.render(instruction_text, True, (200, 200, 200))  # Light gray text

    # Center the text on the screen
    winner_rect =winner_surface.get_rect( center=(W // 2 , H // 2 - 50))
    instruction_rect =instruction_surface.get_rect( center=(W // 2, H // 2 + 50))

    screen.blit( winner_surface, winner_rect)
    screen.blit(instruction_surface, instruction_rect )
    pygame.display.flip()

    # Wait for Enter key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:  # Exit if the game is closed
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                waiting = False  # Exit loop when Ente