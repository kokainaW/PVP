import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Fight")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load background image and scale it
background_image = pygame.image.load("images/background.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load character images
male_character_image = pygame.image.load("images/male_character.png").convert_alpha()
female_character_image = pygame.image.load("images/female_character.png").convert_alpha()

# Character class
class Character:
    def __init__(self, x, y, image, color):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.vel = 5
        self.jump_vel = 10
        self.is_jumping = False
        self.health = 100
        self.image = pygame.transform.scale(image, (50, 100))
        self.color = color

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys, controls):
        if controls['left'] and keys[controls['left']] and self.x > 0:
            self.x -= self.vel
        if controls['right'] and keys[controls['right']] and self.x < WIDTH - self.width:
            self.x += self.vel
        if not self.is_jumping:
            if controls['up'] and keys[controls['up']]:
                self.is_jumping = True
        else:
            self.y -= self.jump_vel
            self.jump_vel -= 1
            if self.jump_vel < -10:
                self.is_jumping = False
                self.jump_vel = 10

    def jump_over(self, other):
        if self.x < other.x:
            self.x -= self.vel
            self.y -= self.vel
        else:
            self.x += self.vel
            self.y -= self.vel

# Health bar drawing function
def draw_health_bar(character, x, y, name):
    pygame.draw.rect(screen, BLACK, (x, y, 104, 24))
    pygame.draw.rect(screen, RED if character.color == RED else BLUE, (x + 2, y + 2, character.health, 20))
    font = pygame.font.SysFont(None, 20)
    text = font.render(name, True, WHITE)
    screen.blit(text, (x, y - 20))

# Create characters
player = Character(100, HEIGHT - 120, male_character_image, RED)
cpu = Character(WIDTH - 150, HEIGHT - 120, female_character_image, BLUE)

# Controls
player_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w}
cpu_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP}

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Draw background
    screen.blit(background_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Player movement
    player.move(keys, player_controls)

    # CPU random movement
    cpu_actions = ['left', 'right', 'up']
    cpu_key = random.choice(cpu_actions)
    cpu_controls_state = {key: (cpu_controls[key] if key == cpu_key else None) for key in cpu_actions}
    cpu.move(keys, cpu_controls_state)

    # Prevent overlap of players
    if abs(player.x - cpu.x) < 50:
        if player.x < cpu.x:
            player.x -= player.vel
            cpu.x += cpu.vel
        else:
            player.x += player.vel
            cpu.x -= cpu.vel

    # Draw characters
    player.draw()
    cpu.draw()

    # Draw health bars
    draw_health_bar(player, 50, 20, "Player 1")
    draw_health_bar(cpu, WIDTH - 150, 20, "Player 2")

    # Update display
    pygame.display.flip()

pygame.quit()

