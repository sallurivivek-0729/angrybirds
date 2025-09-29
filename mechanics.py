import pygame
from config import GRAVITY, MAX_DRAG_DISTANCE

def handle_dragging( mouse_pos, slingshot_x,  slingshot_y):
    distance = ((mouse_pos[0] - slingshot_x)**2 +  (mouse_pos[1] - slingshot_y)**2)**0.5
    if distance > MAX_DRAG_DISTANCE:
        factor = MAX_DRAG_DISTANCE / distance
        return [
             slingshot_x + ( mouse_pos[0] - slingshot_x) * factor,
                slingshot_y + (mouse_pos[1] - slingshot_y) * factor
        ]
    return list(mouse_pos)

def handle_projectile_flight( projectile_pos, velocity_x, velocity_y):
    projectile_pos[0] +=  velocity_x
    projectile_pos[1]  += velocity_y
    velocity_y +=  GRAVITY
    return projectile_pos, velocity_y