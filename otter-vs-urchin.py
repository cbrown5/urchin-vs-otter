import pygame
import random
import time
import numpy as np
import importlib

# Import custom modules
import entities
importlib.reload(entities)

# exec(open('otter-vs-urchin.py').read()) 

#TODO
#modularise the code
# add lobster

#  
# Initialize Pygame
pygame.init()
# Initialize the font
pygame.font.init()
font = pygame.font.Font(None, 50)

#load teh sounds
# Initialize the mixer
pygame.mixer.init()
# Load the sound
crunch_sound = pygame.mixer.Sound('assets/crunching-urchin.wav')  # Replace with the path to your sound file
munch_sound = pygame.mixer.Sound('assets/munching-kelp.wav')  # Replace with the path to your sound file

#Load the sprites 
player_sprite = pygame.image.load('assets/otter.png')  # Replace with the path to your image
urchin_sprite = pygame.image.load('assets/urchin.png')  # Replace with the path to your image
kelp_sprite = pygame.image.load('assets/kelp.png')  # Replace with the path to your image

# Set up the game window
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Invaders")

#Manage the player's air
player_air_max = 3000
# player_air = player_air_max
air_replenish_rate = 100

# Set up the player with the constructor
player = entities.Player(x=window_width // 2, y=window_height - 100, 
                         width=75, height=75, speed_x=1, speed_y=1, 
                         player_sprite=player_sprite, player_score=0, 
                         player_lives=3, player_air=player_air_max,
                         crunch_delay = 300,  # Time to wait between crunching urchins, in milliseconds
                         reload_delay = 500  # Time to wait between missile shots, in milliseconds
)

nbubble = 5
bubble_width = 50
bubble_height = 50
bubbles = []
# Calculate the x-coordinates for evenly distributing the bubbles
bubble_x_coords = np.linspace(0, window_width - bubble_width, nbubble)

for bubble_x in bubble_x_coords:
    bubble_y = random.randint(window_height // 3 * 2, window_height - bubble_height)
    bubble = pygame.Rect(int(bubble_x), bubble_y, bubble_width, bubble_height)
    bubbles.append(bubble)

# Set up the enemies
max_enemies_per_wave = 20
enemy_min_speed = 1
enemy_max_speed = 2
enemy_pause_rate = 20 #this sets the rate at which the enemy pauses before moving again
# ie 20 means 1/20 chance of moving each frame. 
score_speed_increment = 10 #increase the speed of the enemies every time the player gets this many points
enemy_width = 75
enemy_height = 75
urchin_sprite = pygame.transform.scale(urchin_sprite, (enemy_width, enemy_height))

enemies = []
# Initialize the timer for waves of enemies
new_wave = 1
wave_time = 0
wave_delay = 5*1E3  # Time to wait between waves, in milliseconds
enemy_speed_increased = True #flag to indicate if the enemy speed has been increased

#Set up the kelp
kelp_properties = {
    "width":20,
    "height":50
}
kelp_sprite = pygame.transform.scale(kelp_sprite, (kelp_width, kelp_height))
nkelps = 20
kelp_remaining = nkelps
kelps = []
for i in range(nkelps):
    kelp = entities.Kelp(window_width, window_height,
                kelp_properties["width"],
                kelp_properties["height"])
    kelps.append(kelp)

#setup the missile
missile_properties = {
    "width": 20,
    "height": 50,
    "speed": 3,
    "diameter": 10,
    "colour": (144, 144, 144)
}
# Initialize the list of missiles

#setup the shooting spines
spine_width = 5
spine_height = 50
spine_speed = 3
spine_air_cost = player_air_max // 10
# Initialize the list of missiles
spines = []

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #pause if player eats an urchin
        if event.type == pygame.USEREVENT:
            player.paused = False 
        
    #Create a random number of new enemies
    num_enemies_per_wave = random.randint(1, max_enemies_per_wave)
    if new_wave > 0: 
       new_wave -= 1
       for i in range(1, num_enemies_per_wave):
            enemy_x = random.randint(0, window_width - enemy_width)
            enemy_y = 0
            enemy_speed_x = random.uniform(enemy_min_speed, enemy_max_speed)
            enemy_speed_y = enemy_speed_x
            #randomly create an enemy that moves left or right
            if random.randint(1, 2) == 1:
                enemy_speed_x *= -1
            enemy = entities.Enemy(enemy_x, enemy_y, enemy_width, enemy_height, enemy_speed_x, enemy_speed_y)
            enemies.append(enemy)
    elif pygame.time.get_ticks() - wave_time >= wave_delay:
        new_wave = 1  # Reset the indicator to allow a new wave
        wave_time = pygame.time.get_ticks()  # Record the time of the reload

        
    # Move the player
    #Put this here, not in the event loop, the event loop
    # only gets trigged when the key is pressed, not held
    keys = pygame.key.get_pressed()
    player.move_player(keys, window_width, window_height)

    # Move all the enemies
    for enemy in enemies:
        if random.randint(1, enemy_pause_rate) == 1:    
            if random.randint(1, 20) == 1:
                enemy.rect.x += enemy.speed_x
            if enemy.rect.x <= 0 or enemy.rect.x >= window_width - enemy_width:
                enemy.speed_x *= -1
            #randomly change the direction of the enemy
            if random.randint(1, 2500) == 1:
                enemy.speed_x *= -1
            #randomly advance the enemy
            if random.randint(1, 10) == 1:
                enemy.rect.y += enemy.speed_y
            if enemy.rect.y > window_height:
                enemies.remove(enemy)
    
    # Check for collision and remove enemy and/or kelp
    for enemy in enemies:
        if player.rect.colliderect(enemy):
            enemies.remove(enemy)  # Remove the enemy that collided with the player
            crunch_sound.play()
            player.player_score += 1
            player.paused = True  # Pause the player
            pygame.time.set_timer(pygame.USEREVENT, player.crunch_delay)
            continue
        for kelp in kelps:
            if kelp.rect.colliderect(enemy):
               # enemies.remove(enemy)
                kelps.remove(kelp)
                munch_sound.play()
                kelp_remaining -= 1
                break  # Break out of the inner loop

    # reduce players air
    player.player_air -= 1

    #end the game if the player runs out of air
    if  player.player_air <= 0:
        running = False
        print("Game Over")
        break

    #end the game if the player runs out of kelp
    if len(kelps) == 0:
        running = False
        print("Game Over")
        break
    #
    # Clear the screen
    #
    window.fill((2, 31, 232))

    # Draw the bubbles
    for bubble in bubbles:
        pygame.draw.rect(window, (66, 217, 255), bubble)
        #window.blit(kelp_sprite, (kelp.x, kelp.y))

    # Draw the kelp
    for kelp in kelps:
        #pygame.draw.rect(window, (171, 146, 5), kelp)
        window.blit(kelp_sprite, (kelp.x, kelp.y))
    
    # Draw the player's lives
    nkelp_text = font.render(f"Kelp remaining: {kelp_remaining}", True, (171, 146, 5))
    window.blit(nkelp_text, (5, 5))  # Change the position as needed

    #Draw the player's score
    score_text = font.render(f"Score: { player.player_score}", True, (137, 52, 235))
    window.blit(score_text, (5, 50))  # Change the position as needed

    #show a health bar with the player's air
    pygame.draw.rect(window, (255, 0, 0), (5, 100, 100, 20))
    pygame.draw.rect(window, (66, 217, 255), (5, 100, (100* player.player_air/player_air_max), 20))

    # Draw the player and enemy
    window.blit(player.player_sprite, (player.rect.x, player.rect.y))

    for enemy in enemies:
        window.blit(urchin_sprite, (enemy.rect.x, enemy.rect.y))

    # Make the player shoot a missile when space is pressed 
    player.shoot_missile(keys, missile_properties, window)

    # Update the position of each missile
    player.move_missile(enemies,
                      missile_properties, window,
                      crunch_sound)

    if ( player.player_score % 10 == 0) and not enemy_speed_increased:
        enemy_max_speed += 1
        enemy_min_speed += 1
        # halve the pause rate
        enemy_pause_rate = max(1, enemy_pause_rate // 2)
        enemy_speed_increased = True
    #reset the flag
    if  player.player_score % 10 != 0:
        enemy_speed_increased = False

    # Make the enemies randomly shoot spines
    for enemy in enemies:
        if random.randint(1, 5000) == 1:
            spine_x = enemy.rect.x + enemy_width // 2 - spine_width // 2
            spine_y = enemy.rect.y + enemy_height
            spine = pygame.Rect(spine_x, spine_y, spine_width, spine_height)
            spines.append(spine)
            pygame.draw.rect(window, (235, 149, 52), spine)
    # Update the position of each spine
    for spine in spines:
        if spine.y > window_height:
            spines.remove(spine)
        else:
            spine.y += spine_speed
            # Draw the spine
            pygame.draw.rect(window, (235, 149, 52), spine)
            # Check for collisions with the player
            if spine.colliderect(player):
                spines.remove(spine)
                player.player_air -= spine_air_cost
                break

    #replenish the air if the player is on a bubble
    for bubble in bubbles:
        if player.rect.colliderect(bubble):
            #Add air up until it reaches the max
            if player.player_air < player_air_max:
                 player.player_air += min(player_air_max -  player.player_air, air_replenish_rate)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
