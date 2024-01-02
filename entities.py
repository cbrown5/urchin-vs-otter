# Create a player class with attributes and methods

import pygame
import pygame

#Define a player class with methods for moving and shooting

class Player: 

    #Create a constructor
    def __init__(self, x, y, width, height, speed_x, speed_y, player_sprite, 
                 player_score, player_lives, player_air, crunch_delay, reload_delay):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.width = width
        self.height = height
        self.player_sprite = pygame.transform.scale(player_sprite, (width, height))
        self.player_score = player_score
        self.player_lives = player_lives
        self.player_air = player_air
        self.missile_count = 0
        self.reload_time = 0  # Initialize reload_time
        self.reload_delay = reload_delay
        self.paused = False
        self.crunch_delay = crunch_delay



    #Create a method to move the player
    def move_player(self, keys, window_width, window_height):
        if not self.paused:
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed_x
            if keys[pygame.K_RIGHT] and self.rect.x < window_width - self.height:
                self.rect.x += self.speed_x
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed_y
            if keys[pygame.K_DOWN] and self.rect.y < window_height - self.width:
                self.rect.y += self.speed_y

#     #Create a method to shoot missiles
#     def shootMissile(self, keys, missile_list, missile_sprite):
#         if keys[pygame.K_SPACE]:
#             if self.missile_count > 0:
#                 self.missile_count -= 1
#                 missile_x = self.rect.x +  self.width // 2 - missile_width // 2
#                 missile_y = self.rect.y - missile_height
#                 #draw the missile as a grey circle
#                 missile = pygame.Rect(missile_x, missile_y, missile_width, missile_height)
#                 missiles.append(missile)
#                 pygame.draw.circle(window, (144, 144, 144), (missile_x, missile_y), 10)
#             elif pygame.time.get_ticks() - self.reload_time >= reload_delay:
#                 self.missile_count = 1  # Reset the missile count
#                 self.reload_time = pygame.time.get_ticks()  # Record the time of the reload


# Create a class for the missile
class Missile:

    def __init__(self, entity, width, height, 
                 speed_x, speed_y):
        x = entity.rect.x +  entity.width // 2 - width // 2
        y = entity.rect.y - height
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def move_missile(self):
        self.rect.y -= self.speed_y

