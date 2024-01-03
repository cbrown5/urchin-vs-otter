# Create a player class with attributes and methods

import pygame
import random


class Enemy:
    def __init__(self, x, y, width, height, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y

class Kelp:
    def __init__(self, window_width, window_height,
                 width, height, sprite):
        self.x = random.randint(0, window_width - width)
        self.y = random.randint(window_height // 3 * 2, 
                                window_height - height)
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.sprite = sprite

#create a lobster class
class Lobster:
    def __init__(self, window_width, window_height,
                 width, height, speed_x, speed_y, sprite):
        self.x = random.randint(0, window_width - width)
        self.y = random.randint(0, 
                                window_height - height)
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.sprite = sprite

    #create a method that moves the lobster in a random direction
    def move_random(self, window_width, window_height):
        if random.randint(0, 1000) == 1:
            self.speed_x *= -1
        if random.randint(0, 1000) == 1:
            self.speed_y *= -1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= window_width - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= window_height - self.rect.height:
            self.speed_y *= -1
        

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
        self.missiles = []

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
    def shoot_missile(self, keys, missile_properties, window):
        if keys[pygame.K_SPACE]:
                if self.missile_count > 0:
                    self.missile_count -= 1
                    #init a new missile
                    missile = Missile(self, missile_properties["width"],
                                    missile_properties["height"],
                                    0, #x speed
                                    missile_properties["speed"]
                    )
                    self.missiles.append(missile)
                    pygame.draw.circle(window, missile_properties["colour"], 
                                    (missile.rect.x, missile.rect.y), missile_properties["diameter"])
                elif pygame.time.get_ticks() - self.reload_time >= self.reload_delay:
                    self.missile_count = 1  # Reset the missile count
                    self.reload_time = pygame.time.get_ticks()  # Record the time of the reload

    def move_missile(self, enemies, 
                     missile_properties, window, crunch_sound):
        for missile in self.missiles:
            if missile.rect.y < 0:
                self.missiles.remove(missile)
            else:
                missile.rect.y -= missile.speed_y
                # Draw the missile
                pygame.draw.circle(window, missile_properties["colour"], 
                                (missile.rect.x, missile.rect.y), missile_properties["diameter"])
                # Check for collisions with enemies
                for enemy in enemies[:]:  # Iterate over a copy of the list
                    if missile.rect.colliderect(enemy):
                        self.missiles.remove(missile)
                        enemies.remove(enemy)
                        crunch_sound.play()
                        self.player_score += 1
                        break  # Break out of the inner loop




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

#Create a class for quiz questions. The questions will be addition or subtractoin of two random integers less than 10
class Question:

    def __init__(self):
        first = random.randint(0, 10)
        second = random.randint(0, 10)
        operation = random.randint(0, 1)
        if operation == 0:
            self.question = str(first) + " + " + str(second) + " = "
            self.answer = first + second
        else:
            self.question = str(first) + " - " + str(second) + " = "
            self.answer = first - second
        

