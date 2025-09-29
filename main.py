import pygame
import sys
from config import *
from helpers import main_menu, name_entry, render_bird_options, generation, render, check_collision,resizeimages,winscreen

from assets_loader import load_image
import random
def main():
    winner =  None
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption( "Turn-Based Game")
    clock = pygame.time.Clock()
 
    start_button, exit_button = main_menu(screen, BACKGROUND_PATH + "main_menu.png")
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint( mouse_pos):
                    waiting = False
                elif exit_button.collidepoint( mouse_pos):
                    pygame.quit()
                    sys.exit()

    player_names = name_entry(screen, BACKGROUND_PATH + "player_interface.png")
    gameplay_background = load_image(BACKGROUND_PATH + "gameplay.png", (W, H))
    left_catapult = load_image(CATAPULT_PATH +  "left_catapult.png", (100, 100))
    right_catapult = load_image(CATAPULT_PATH + "right_catapult.png"  , (100, 100))
    projectile_images = {
        "red":  load_image ( PROJECTILE_PATH +  "red.png", (40, 40)),
        "chuck": load_image(PROJECTILE_PATH + "chuck.png", (40, 40)),
        "blues": load_image(PROJECTILE_PATH +  "blues.png", (40, 40)),
        "bomb":  load_image( PROJECTILE_PATH  + "bomb.png", (40 , 40)),
    }
    block_type_1 = pygame.image.load( BLOCK_PATH+"ice.png" ).convert_alpha()
    block_type_2 = pygame.image.load(BLOCK_PATH+"stone.png" ).convert_alpha()
    block_type_3 = pygame.image.load( BLOCK_PATH+"wood.png" ).convert_alpha()

    blw = 50  # Width of blocks in the fortress
    blh = 50  # Height of blocks in the fortress
    image_paths = [BLOCK_PATH + "ice.png",BLOCK_PATH + "stone.png",BLOCK_PATH + "wood.png"]  # Paths to block images

# Resize and load block images
    blocks = resizeimages(image_paths, blw, blh)
    fortress_1 =generation(3, 4, 50, 250, H - 300,blocks)
    fortress_2 =generation(3, 4, 50, W - 450, H - 300,blocks)
    projectile_pos =  [150, H - 150]
    velocity_x, velocity_y = 0, 0
    dragging, inflight = False, False
    player_1_birds = ["red", "chuck", "blues",  "bomb"]
    player_2_birds = ["red" , "chuck" , "blues", "bomb" ]
    selected_bird_player_1 = player_1_birds[0]
    selected_bird_player_2 = player_2_birds[0]
    current_player = 1

    running = True
    while running:
        screen.fill((30, 30, 30))  # Fill screen with background color (e.g., dark gray)
        screen.blit(gameplay_background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        fortress = generation(3, 4, blw, 50, 300, blocks)
        if len(fortress_1) == 0:  # Player 2 destroys Player 1's fortress
               winner = player_names[1]  # Player 2 wins
               winscreen(screen, winner)
               running=False
        elif len(fortress_2) == 0:  # Player 1 destroys Player 2's fortress
               winner =player_names[0]  # Player 1 wins
               winscreen( screen, winner)
               running = False

        render(screen, fortress_1 )  # Render Player 1's fortress
        render(screen, fortress_2 )  # Render Player 2's fortress
        render_bird_options( screen, player_1_birds,50, H - 100, projectile_images)
        render_bird_options( screen, player_2_birds, W - 250, H - 100, projectile_images)
        screen.blit( left_catapult, (150 - 50, H - 200))
        screen.blit(right_catapult , (W - 150 - 50, H - 200))

        if current_player == 1:
            screen.blit(projectile_images[selected_bird_player_1], (140 - 15, H - 170 -15 ))
        else:
            screen.blit(projectile_images[selected_bird_player_2], (W - 140 - 15, H - 170 -15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, bird in enumerate(player_1_birds if current_player == 1 else player_2_birds):
                    bird_rect= pygame.Rect(50 + i * 50 if current_player == 1 else W - 250 + i * 50, H - 100, 40, 40)
                    if bird_rect.collidepoint(mouse_pos):
                        if current_player == 1:
                            selected_bird_player_1 = bird
                        else:
                            selected_bird_player_2 = bird
               
                if current_player == 1 and not inflight and 140 - 30 <= mouse_pos[0] <= 140 + 30 and H - 170 - 30 <= mouse_pos[1] <= H - 170 + 30:
                    dragging = True
                elif current_player == 2 and not inflight and W - 140 - 30 <= mouse_pos[0] <= W - 140 + 30 and H - 170 - 30 <= mouse_pos[1] <= H - 170 + 30:
                    dragging = True
            elif event.type ==  pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                inflight = True
                if current_player == 1:
                    velocity_x = (150 - mouse_pos[0] ) * 1.5 / 10
                    velocity_y = (H - 150  - mouse_pos[1]) * 1.5 / 10
                elif current_player == 2:
                    velocity_x = ( W - 150 - mouse_pos[0]) * 1.5 / 10
                    velocity_y = (H - 150 - mouse_pos[1]) * 1.5 / 10

        if inflight:
            projectile_pos[0] += velocity_x
            projectile_pos[1] += velocity_y
            velocity_y += GRAVITY
            projectile_rect = pygame.Rect( projectile_pos[0], projectile_pos[1], 40, 40)

            if current_player == 1 and check_collision( projectile_rect , fortress_2):
                inflight = False
                current_player = 2
                projectile_pos = [ W - 150 , H - 150]
            elif current_player == 2 and check_collision(projectile_rect, fortress_1):
                inflight = False
                current_player = 1
                projectile_pos = [150 , H - 150]

            # Check if projectile leaves the screen
            if projectile_pos[0] < 0 or projectile_pos[0] > W or projectile_pos[1] > H:
                current_player = 1 if current_player == 2 else 2  # Switch turn
                inflight = False
                projectile_pos = [150, H - 150 ] if current_player == 1 else [W - 250, H - 150]

        render(screen,   fortress_1)
        render( screen, fortress_2)

        if inflight:
            if current_player == 1:
                screen.blit( projectile_images[selected_bird_player_1], (projectile_pos[0] - 15, projectile_pos[1] - 15))
            elif current_player == 2:
                screen.blit(projectile_images [selected_bird_player_2],   (   projectile_pos[0] - 15, projectile_pos[1] - 15))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()