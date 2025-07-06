import pygame
from sys import exit, argv, platform
from random import randint
from math import gcd

if platform == "win32":
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Slime class
class Slime(pygame.sprite.Sprite):
    def __init__(self, val, pos, font):
        super().__init__()
        self.selected = 0
        self.atk = val
        self.font = font

        # Load images
        slime_surf = pygame.image.load('images/slime.png').convert_alpha()
        slime_surf = pygame.transform.rotozoom(slime_surf, 0, 0.1)
        slime_selected = pygame.image.load('images/slime_selected.png').convert_alpha()
        slime_selected = pygame.transform.rotozoom(slime_selected, 0, 0.1)
        self.images = [slime_surf, slime_selected]

        self.image = self.images[self.selected]
        self.rect = self.image.get_rect(center=pos)

    def toggle(self):
        self.selected ^= 1
        self.image = self.images[self.selected]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        hp_surf = self.font.render(str(self.atk), True, 'black')
        surface.blit(hp_surf, hp_surf.get_rect(center=self.rect.center))


# --- Game Setup ---

# Handle argument
if len(argv) != 2:
    print('Usage: python3 main.py [1-5]')
    exit(1)

try:
    mode = int(argv[1])
    if not (1 <= mode <= 5):
        raise ValueError
except ValueError:
    print("Mode must be an integer between 1 and 5.")
    exit(1)

# Read input
try:
    with open(f'{mode}.txt', 'r') as f:
        input_values = [int(x) for x in f.readline().split()]
        if not (5 <= len(input_values) <= 10):
            raise ValueError
except Exception as e:
    print(f"Failed to read file {mode}.txt: {e}")
    exit(1)

# Cost function
def compute_cost(hp1, hp2, mode):
    if mode == 1:
        return hp1 * hp2
    elif mode == 2:
        return hp1 + hp2
    elif mode == 3:
        return min(hp1, hp2)
    elif mode == 4:
        return gcd(hp1, hp2)
    else:
        return hp1 + hp2

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1800, 1400))
pygame.display.set_caption('Merging Game')
clock = pygame.time.Clock()

# Timer setup
start_ticks = pygame.time.get_ticks()  # Milliseconds
time_limit = 150  # Seconds
game_lost = False

# Load background
bg_surface = pygame.image.load('images/grass.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (1800, 1400))

# Fonts
pixel_font_large = pygame.font.Font('fonts/Pixeltype.ttf', 140)
pixel_font_medium = pygame.font.Font('fonts/Pixeltype.ttf', 100)
summer_font_medium = pygame.font.Font('fonts/SimpleSummer-Regular.otf', 100)
pixel_font_small = pygame.font.Font('fonts/Pixeltype.ttf', 48)

title_surf = pixel_font_large.render('Merging Game', False, 'Black')
title_rect = title_surf.get_rect(center=(900, 100))

# Slime group and layout
slime_group = pygame.sprite.Group()
positions = []

start_x = 250
gap_x = 330
row_y = [400, 700]  # Widened vertical spacing

for i in range(len(input_values)):
    x = start_x + (i % 5) * gap_x
    y = row_y[i // 5]
    positions.append((x, y))

for val, pos in zip(input_values, positions):
    slime = Slime(val, pos, font=summer_font_medium)
    slime_group.add(slime)

selected_slimes = []
total_cost = 0

bg_music = pygame.mixer.Sound('audio/theme.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

pop_sound = pygame.mixer.Sound('audio/pop.mp3')

# --- Main Loop ---
running = True
while running:
    # Calculate time
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, time_limit - seconds_passed)
    if time_left <= 0:
        game_lost = True
        running = False

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for slime in slime_group:
                if slime.rect.collidepoint(event.pos):
                    slime.toggle()
                    pop_sound.play()
                    if slime in selected_slimes:
                        selected_slimes.remove(slime)
                    else:
                        selected_slimes.append(slime)

                    if len(selected_slimes) == 2:
                        s1, s2 = selected_slimes
                        cost = compute_cost(s1.atk, s2.atk, mode)
                        total_cost += cost

                        s2.atk += s1.atk
                        slime_group.remove(s1)
                        if s2.selected:
                            s2.toggle()
                        selected_slimes.clear()

                        if len(slime_group) == 1:
                            running = False

    # --- Draw ---
    screen.blit(bg_surface, (0, 0))
    screen.blit(title_surf, title_rect)

    for slime in slime_group:
        slime.draw(screen)

    # Draw cost and timer below the slimes
    cost_surf = pixel_font_medium.render(f'Total Cost: {total_cost}', True, 'Black')
    screen.blit(cost_surf, (100, 1050))

    min_left = time_left // 60
    sec_left = time_left % 60
    timer_surf = pixel_font_medium.render(f'Time Left: {min_left:02}:{sec_left:02}', True, 'Black')
    screen.blit(timer_surf, (100, 1120))

    pygame.display.update()
    clock.tick(60)

# --- End Screen ---
screen.fill((0, 0, 0))
end_font = pygame.font.Font('fonts/SimpleSummer-Regular.otf', 150)

if game_lost:
    end_text = end_font.render('Time Up! You Lost!', True, 'red')
else:
    end_text = end_font.render(f'Final Cost: {total_cost}', True, 'white')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
    screen.blit(end_text, end_text.get_rect(center=(900, 700)))
    pygame.display.update()
    clock.tick(60)
# pygame.time.delay(3000)
# pygame.quit()
# exit()
