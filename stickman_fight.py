import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Fight")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # CPU character
BLUE = (0, 0, 255)  # Player character
GREEN = (0, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load character images
try:
    male_character = pygame.image.load("/home/irobot/Desktop/git/PVP/images/male_character.png").convert_alpha()
    female_character = pygame.image.load("/home/irobot/Desktop/git/PVP/images/female_character.png").convert_alpha()
    print("Images loaded successfully.")
except pygame.error as e:
    print(f"Error loading images: {e}")
    male_character = pygame.Surface((50, 100))  # Fallback to placeholder
    male_character.fill(BLUE)
    female_character = pygame.Surface((50, 100))  # Fallback to placeholder
    female_character.fill(RED)

# Draw health bars and labels
def draw_health_bar(stickman, x, y, label):
    pygame.draw.rect(screen, RED, (x, y, 100, 10))  # Background (red for full damage)
    pygame.draw.rect(screen, GREEN, (x, y, stickman.health, 10))  # Health (green for remaining health)
    font = pygame.font.SysFont(None, 24)
    label_text = font.render(label, True, BLACK)
    screen.blit(label_text, (x, y + 15))

class Character:
    def __init__(self, x, y, image, health=100):
        self.x = x
        self.y = y
        self.image = image
        self.health = health
        self.vel = 5
        self.is_jumping = False
        self.jump_count = 10
        self.ground_level = y  # Initial y position as ground level

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys, controls):
        if keys:
            if keys[controls['left']]:
                self.x -= self.vel
            if keys[controls['right']]:
                self.x += self.vel
            if not self.is_jumping and keys[controls['up']]:
                self.is_jumping = True
        
        # Handle jumping mechanics
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

        # Boundaries
        self.x = max(0, min(WIDTH - self.image.get_width(), self.x))
        if not self.is_jumping:
            self.y = self.ground_level

    def jump_over(self, opponent):
        if abs(self.x - opponent.x) < 60 and self.y == self.ground_level:
            self.is_jumping = True

    def take_damage(self):
        if self.health > 0:
            self.health -= 10

# Initialize player and CPU characters
player = Character(200, HEIGHT - 110, male_character)
cpu = Character(600, HEIGHT - 110, female_character)

# Controls mapping for players
player_controls = {
    'up': pygame.K_w,
    'left': pygame.K_a,
    'right': pygame.K_d
}

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Player movement
    player.move(keys, player_controls)

    # CPU movement (randomized for demonstration)
    cpu_actions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]
    cpu_key = random.choice(cpu_actions)
    
    # Map CPU actions to controls
    cpu_controls = {
        pygame.K_LEFT: {'left': True, 'right': False, 'up': False},
        pygame.K_RIGHT: {'left': False, 'right': True, 'up': False},
        pygame.K_UP: {'left': False, 'right': False, 'up': True}
    }

    # Fix: Always pass a valid dictionary for controls, with default False values
    controls = cpu_controls.get(cpu_key, {'left': False, 'right': False, 'up': False})
    cpu.move(keys, controls)

    # Prevent overlap of players
    if abs(player.x - cpu.x) < 50:
        if player.x < cpu.x:
            player.x -= player.vel
            cpu.x += cpu.vel
        else:
            player.x += player.vel
            cpu.x -= cpu.vel

    # Player jump over CPU
    if keys[pygame.K_w]:
        player.jump_over(cpu)

    # CPU jump over player
    if cpu.x < player.x and abs(cpu.x - player.x) < 60:
        if keys[pygame.K_UP]:
            cpu.jump_over(player)

    # Draw characters
    player.draw()
    cpu.draw()

    # Draw health bars and labels
    draw_health_bar(player, 50, 20, "Player 1")
    draw_health_bar(cpu, WIDTH - 150, 20, "Player 2")

    # Check for game over
    if player.health <= 0 or cpu.health <= 0:
        winner = "Player 1" if cpu.health <= 0 else "Player 2"
        running = False

    pygame.display.flip()

pygame.quit()

