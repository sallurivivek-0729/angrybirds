import pygame

def load_image(path, size):
    try:
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None