import pygame
import random
import math

# Configuration\NSCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.35        # gravitational acceleration
SPAWN_INTERVAL = 1500 # milliseconds between fruit throws
MIN_LAUNCH_SPEED_Y = -15
MAX_LAUNCH_SPEED_Y = -20
MIN_LAUNCH_SPEED_X = -3
MAX_LAUNCH_SPEED_X = 3

class Fruit:
    def __init__(self, image):
        # Start at bottom center with random horizontal offset
        self.image_orig = image
        self.rect = self.image_orig.get_rect()
        self.x = random.randint(self.rect.width // 2, SCREEN_WIDTH - self.rect.width // 2)
        self.y = SCREEN_HEIGHT + self.rect.height // 2
        # Random initial velocity
        self.vel_x = random.uniform(MIN_LAUNCH_SPEED_X, MAX_LAUNCH_SPEED_X)
        self.vel_y = random.uniform(MAX_LAUNCH_SPEED_Y, MIN_LAUNCH_SPEED_Y)
        # Rotation
        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)
        self.sliced = False

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        # Rotate
        self.angle = (self.angle + self.rot_speed) % 360
        # Update rect center
        self.rect = self.image_orig.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        # Rotate image around center
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)

    def is_off_screen(self):
        return self.y - self.rect.height > SCREEN_HEIGHT or self.x < -self.rect.width or self.x > SCREEN_WIDTH + self.rect.width

    def check_slice(self, slice_points):
        # Check if any recent slice point intersects the fruit
        for point in slice_points:
            if self.rect.collidepoint(point):
                self.sliced = True
                break


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load fruit image (ensure transparent background, e.g., PNG ~64x64)
    fruit_img = pygame.image.load('watermelon.png').convert_alpha()

    fruits = []
    SLICE_POINTS = []  # recent mouse positions for slicing detection
    pygame.time.set_timer(pygame.USEREVENT, SPAWN_INTERVAL)

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                # Spawn a new fruit
                fruits.append(Fruit(fruit_img))
            elif event.type == pygame.MOUSEMOTION:
                # Record motion for slicing
                SLICE_POINTS.append(event.pos)
                # Keep only a short trail
                if len(SLICE_POINTS) > 15:
                    SLICE_POINTS.pop(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Clear slice trail when mouse button released
                SLICE_POINTS.clear()

        # Update fruits
        for fruit in fruits[:]:
            fruit.update()
            fruit.check_slice(SLICE_POINTS)
            if fruit.sliced or fruit.is_off_screen():
                fruits.remove(fruit)

        # Drawing
        screen.fill((25, 25, 25))
        # Draw fruits
        for fruit in fruits:
            fruit.draw(screen)
        # Draw slice trail
        if len(SLICE_POINTS) > 1:
            pygame.draw.lines(screen, (255, 0, 0), False, SLICE_POINTS, 3)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

