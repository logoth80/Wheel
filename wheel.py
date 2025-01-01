import pygame
import math
import time
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("the Wheel")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 170, 20)
silver = (140, 140, 140)
bg_color = (120, 30, 0)
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (255, 0, 125),
    (0, 255, 125),
    (0, 0, 255),  # Blue
    (255, 125, 0),
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (0, 125, 255),
    (255, 0, 255),  # Magenta
    (255, 255, 255),
    (60, 60, 60),
]
texts = ["BANKRUT", "2500", "200", "300", "500", "WYCIECZKA", "750", "1000", "1500", "Niespodzianka", "100", "5000"]

# Starting point of the triangles
center_x, center_y = width // 2, height // 2

# Length of each line
line_length = 250
pies = 24
# Angle between each triangle in degrees
angle_step = 360 / pies
current_degree = -1
rotation_tick = 0.005
rotation_step = 0
last_tick_time = time.time()
last_rest = 0
play_sound_step = 360 / (3 * pies)
next_sound_angle = -play_sound_step
click_sound = pygame.mixer.Sound("click.mp3")
print(click_sound.get_volume())
# Set up the font
font = pygame.font.Font(None, 24)  # None uses the default system font

added_power = 0


def roll_wheel(power_added):
    global rotation_step
    rotation_step = power_added / 100


def sound_click():
    click_sound.set_volume(1 + rotation_step / 3)
    click_sound.play()


def draw_power(power):
    for p in range(int(power)):
        pygame.draw.rect(screen, (25, 200, 0), pygame.Rect(697, 497 - p * 3, 51, 8))
    for p in range(int(power)):
        pygame.draw.rect(screen, (240, max(0, 240 - 2 * p), 0), pygame.Rect(700, 500 - p * 3, 45, 3))
        # pygame.display.flip()


teststart = time.time()
fpstest = 0
# Main game loop
running = True
while running:
    fpstest += 1
    if fpstest % 1000 == 0:
        print(1000 / (time.time() - teststart), " fps")
        teststart = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key).lower()
            if event.key == pygame.K_ESCAPE:
                restarting_loop = False
                running = False
            if event.key == pygame.K_F5:
                print("restart")
            if event.key == pygame.K_SPACE:
                print("release ", added_power)
                if added_power > 0:
                    roll_wheel(added_power)
                    added_power = 0
        elif event.type == pygame.K_DOWN:
            key = pygame.key.name(event.key).lower()
            if event.key == pygame.K_SPACE:
                print("powering up ")
                added_power = min(added_power, 100)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                added_power += 5
                added_power = max(added_power, 25)
                added_power = min(120, added_power)
                draw_power(added_power)
                print(added_power)

    screen.fill(bg_color)

    def draw_wheel(degree):
        # Draw pies * triangles
        current_angle = degree
        for i in range(pies):
            end_x = center_x + line_length * math.cos(math.radians(current_angle))
            end_y = center_y - line_length * math.sin(math.radians(current_angle))

            third_vertex_x = center_x + line_length * math.cos(math.radians(current_angle + angle_step))
            third_vertex_y = center_y - line_length * math.sin(math.radians(current_angle + angle_step))

            # Draw and fill the triangle
            # gfxdraw.aapolygon(screen, [(center_x, center_y), (int(end_x), int(end_y)), (int(third_vertex_x), int(third_vertex_y))], colors[i % len(colors)])
            pygame.draw.polygon(
                screen,
                colors[i % len(colors)],
                [
                    (center_x, center_y),
                    (int(end_x), int(end_y)),
                    (int(third_vertex_x), int(third_vertex_y)),
                ],
                width=0,
            )
            if rotation_step == 0:
                gfxdraw.aapolygon(screen, [(center_x, center_y), (int(end_x), int(end_y)), (int(third_vertex_x), int(third_vertex_y))], colors[i % len(colors)])

            gfxdraw.aacircle(screen, center_x, center_y, line_length + 1, gold)
            pygame.draw.circle(screen, gold, (center_x, center_y), radius=line_length + 1, width=7)
            gfxdraw.aacircle(screen, center_x, center_y, line_length - 6, gold)

            # Calculate text position for each triangle
            text_angle = current_angle + angle_step / 2
            # Render text into a surface
            text_surface = font.render(texts[i % len(texts)], True, black)
            offset = int(0.5 * text_surface.get_width()) + 20
            t1_x = center_x + ((line_length - offset) * math.cos(math.radians(text_angle)))  # Adjusted distance
            t1_y = center_y - ((line_length - offset) * math.sin(math.radians(text_angle)))

            # Rotate the text surface
            rotated_text_surface = pygame.transform.rotate(text_surface, text_angle)

            # Get the rectangle of the rotated surface to center it
            rotated_rect = rotated_text_surface.get_rect(center=(t1_x, t1_y))
            screen.blit(rotated_text_surface, rotated_rect)

            current_angle += angle_step

        for i in range(3 * pies):  # spokes
            degree_1 = i * (360 / (3 * pies)) + current_degree
            x1 = int(center_x + (line_length - 2.5) * math.cos(math.radians(degree_1)))
            y1 = int(center_y - (line_length - 2.5) * math.sin(math.radians(degree_1)))
            gfxdraw.aacircle(screen, x1, y1, 3, (60, 60, 60))
            pygame.draw.circle(screen, silver, (x1, y1), 3)

    draw_wheel(current_degree)
    draw_power(added_power)

    pygame.draw.polygon(
        screen,
        (200, 0, 0),
        [(center_x, center_y - line_length + 5), (center_x - 5, center_y - line_length - 15), (center_x + 5, center_y - line_length - 15)],
        0,
    )

    # Update the display
    pygame.display.flip()
    if time.time() > last_tick_time + rotation_tick:
        current_degree -= rotation_step
        if rotation_step < 0.02:
            rotation_step = 0
        elif rotation_step < 0.08:
            rotation_step = rotation_step * 0.997
        elif rotation_step < 0.2:
            rotation_step = rotation_step * 0.998
        elif rotation_step < 0.5:
            rotation_step = rotation_step * 0.999
        else:
            rotation_step = rotation_step * 0.9993
        if current_degree <= -360:
            current_degree += 360

        print(f"c: {int(current_degree)}, n: {int(next_sound_angle)}")
        if current_degree < next_sound_angle:
            sound_click()
            next_sound_angle -= play_sound_step
            if next_sound_angle <= -360:
                next_sound_angle += 360

        last_tick_time = time.time()


# Quit Pygame
pygame.quit()
