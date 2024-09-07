import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Move and Shoot the Triangle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Color for the enemy
BLACK = (0, 0, 0)  # Color for the game over text

# Triangle settings
triangle_size = 50
triangle_speed = 5
triangle_x = SCREEN_WIDTH // 2
triangle_y = SCREEN_HEIGHT - (triangle_size / 2)  # Positioned at the bottom

# Bullet settings
bullet_radius = 5
bullet_speed = 7
bullets = []
last_shot_time = 0
shot_delay = 300  # milliseconds

# Enemy settings
enemy_radius = 20
min_enemy_speed = 1  # Minimum speed for falling enemies
max_enemy_speed = 3  # Maximum speed for falling enemies
enemy_add_interval = 60  # Number of frames between adding enemies
enemies = []

# Font settings
font = pygame.font.SysFont(None, 55)

# Function to get triangle vertices
def get_triangle_vertices(x, y, size):
    half_size = size / 2
    height = (3 ** 0.5 / 2) * size  # Height of an equilateral triangle
    return [
        (x, y - height / 2),              # Top vertex
        (x - half_size, y + height / 2),  # Bottom left vertex
        (x + half_size, y + height / 2)   # Bottom right vertex
    ]

# Function to check collision between a bullet and an enemy
def check_collision(bullet, enemy):
    bx, by = bullet
    ex, ey = enemy
    return (bx - ex) ** 2 + (by - ey) ** 2 < (bullet_radius + enemy_radius) ** 2

# Function to check collision between the triangle and an enemy
def check_triangle_collision(triangle, enemy):
    tx, ty = triangle
    ex, ey = enemy
    triangle_vertices = get_triangle_vertices(tx, ty, triangle_size)
    # Check if the enemy is within the bounding box of the triangle
    min_x = min(v[0] for v in triangle_vertices)
    max_x = max(v[0] for v in triangle_vertices)
    min_y = min(v[1] for v in triangle_vertices)
    max_y = max(v[1] for v in triangle_vertices)
    return min_x <= ex <= max_x and min_y <= ey <= max_y

# Add a new enemy
def add_enemy():
    x = random.randint(enemy_radius, SCREEN_WIDTH - enemy_radius)
    y = -enemy_radius  # Start off the top of the screen
    speed = random.uniform(min_enemy_speed, max_enemy_speed)  # Random speed for each enemy
    enemies.append([x, y, speed])  # Store the enemy's position and speed

# Game over function
def game_over():
    screen.fill(WHITE)
    text = font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the message for 3 seconds

# Main loop
running = True
game_over_flag = False
frame_count = 0  # Frame counter for adding enemies

while running:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over_flag:
        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and triangle_x - triangle_size / 2 > 0:
            triangle_x -= triangle_speed
        if keys[pygame.K_RIGHT] and triangle_x + triangle_size / 2 < SCREEN_WIDTH:
            triangle_x += triangle_speed

        if keys[pygame.K_SPACE] and current_time - last_shot_time > shot_delay:
            # Shoot a bullet
            bullet_x = triangle_x
            bullet_y = triangle_y - (triangle_size / 2)  # Shoot from the top of the triangle
            bullets.append([bullet_x, bullet_y])
            last_shot_time = current_time

        # Update bullet positions
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed  # Move bullet up
            if bullet[1] < 0:  # Remove bullets that go off-screen
                bullets.remove(bullet)

        # Update enemy positions and check for collisions
        for enemy in enemies[:]:
            enemy[1] += enemy[2]  # Move enemy down with its specific speed
            if enemy[1] > SCREEN_HEIGHT + enemy_radius:  # Remove enemies that go off-screen
                enemies.remove(enemy)
            # Check collision with bullets
            for bullet in bullets[:]:
                if check_collision(bullet, enemy[:2]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break  # Exit loop after removing bullet and enemy
            # Check collision with triangle
            if check_triangle_collision((triangle_x, triangle_y), enemy[:2]):
                game_over_flag = True
                break  # Exit loop after detecting collision

        # Add a new enemy at intervals
        frame_count += 1
        if frame_count >= enemy_add_interval:
            add_enemy()
            frame_count = 0

        # Update the display
        screen.fill(WHITE)  # Clear screen with white color
        triangle_vertices = get_triangle_vertices(triangle_x, triangle_y, triangle_size)
        pygame.draw.polygon(screen, RED, triangle_vertices)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, BLUE, (int(bullet[0]), int(bullet[1])), bullet_radius)

        # Draw enemies
        for enemy in enemies:
            pygame.draw.circle(screen, GREEN, (int(enemy[0]), int(enemy[1])), enemy_radius)

        pygame.display.flip()  # Update the screen

    else:
        game_over()  # Show game over screen and wait before quitting

    # Cap the frame rate
    pygame.time.Clock().tick(30)  # 30 frames per second
