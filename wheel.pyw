import pygame
import math
import time
from pygame import gfxdraw
import random

# Initialize Pygame
pygame.init()

line_length = 250
# Set up the display window
width, height = 2 * line_length + 300, 2 * line_length + 100
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("the Wheel")

wheel_moving = False

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

pies = 24
# Angle between each triangle in degrees
angle_step = 360 / pies
current_degree = -1
rotation_tick = 0.004
rotation_step = 0
last_tick_time = time.time()
last_rest = 0
play_sound_step = 360 / (3 * pies)
next_sound_angle = -play_sound_step
click_sound = pygame.mixer.Sound("click.mp3")

# Set up the font
font = pygame.font.SysFont("Book Antiqua", int(24 * line_length / 280))  # None uses the default system font
font2 = pygame.font.SysFont("Georgia", 36)
added_power = 0


def calculate_stop_time(rotation_step_0, rotation_tick):
    total_time = 0
    current_step = rotation_step_0

    while current_step >= 0.02:
        if current_step < 0.08:
            decay_factor = 0.9965
        elif current_step < 0.2:
            decay_factor = 0.9975
        elif current_step < 0.5:
            decay_factor = 0.9985
        else:
            decay_factor = 0.999

        # Calculate time for this step
        steps_to_next_threshold = math.ceil(math.log(0.02 / current_step) / math.log(decay_factor))
        total_time += steps_to_next_threshold * rotation_tick
        current_step *= decay_factor**steps_to_next_threshold  # Decay to threshold

    return total_time


def roll_wheel(power_added):
    global rotation_step
    power_added = power_added - 0.40 * power_added + random.random() * power_added / 2.5
    rotation_step = power_added / 100
    if power_added > 0:
        global wheel_moving
        wheel_moving = True

    time_to_stop = calculate_stop_time(rotation_step, rotation_tick)
    print(f"Speed: {power_added}. Time to stop: {time_to_stop:.2f} seconds")


def sound_click():
    click_sound.set_volume(0.3 + rotation_step)
    click_sound.play()


def draw_power(power):
    for p in range(int(power)):
        pygame.draw.rect(screen, (25, 200, 0), pygame.Rect(2 * line_length + 200, 2 * line_length - p * int(line_length / 101 + 1) - 6, 51, 8))
    for p in range(int(power)):
        pygame.draw.rect(
            screen,
            (240, max(0, 240 - 2 * p), 0),
            pygame.Rect(2 * line_length + 203, 2 * line_length - 3 - p * int(line_length / 101 + 1), 45, int(line_length / 101) + 1),
        )


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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                restarting_loop = False
                running = False
            elif event.key == pygame.K_F5:
                print("restart")
            elif event.key == pygame.K_SPACE and not wheel_moving:
                print("powering up ")
                added_power = max(added_power, 15)  # Ensure a minimum value
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and not wheel_moving:
                print("release ", added_power)
                if added_power > 0:
                    roll_wheel(added_power)
                    added_power = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle mouse button release
            if not wheel_moving and added_power >= 15:
                roll_wheel(added_power)
                added_power = 0

    # Continuous checks outside of event handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not wheel_moving:
        added_power += 0.7
        added_power = min(line_length / 2, added_power)  # Limit max power
        draw_power(added_power)

    if pygame.mouse.get_pressed()[0] and not wheel_moving:
        added_power += 0.7
        added_power = max(added_power, 15)
        added_power = min(line_length / 2, added_power)
        draw_power(added_power)
    elif pygame.mouse.get_pressed()[2] and wheel_moving:
        if rotation_step > 0.3:
            rotation_step *= 0.998

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

    def current_result():
        current_index = int(((-90 - current_degree) % 360) / (360 / pies))
        # print(texts[(current_index % len(texts))])
        return current_index % len(texts)

    if rotation_step == 0:  # or rotation_step != 0:
        index = current_result()
        text_surface = font2.render(texts[index], 100, (50, 40, 40))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(line_length - text_width - 5, 25, text_width + 30, text_height + 30))
        pygame.draw.rect(screen, colors[index], pygame.Rect(line_length - text_width, 30, text_width + 20, text_height + 20))
        screen.blit(text_surface, (line_length + 10 - text_width, 36))

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

    def turn_wheel():
        global last_tick_time, current_degree, next_sound_angle, rotation_step, wheel_moving

        if time.time() > last_tick_time + rotation_tick:
            last_tick_time = time.time()
            current_degree -= rotation_step

            if rotation_step < 0.02:
                rotation_step = 0
                wheel_moving = False
            elif rotation_step < 0.08:
                rotation_step = rotation_step * 0.996
            elif rotation_step < 0.2:
                rotation_step = rotation_step * 0.9975
            elif rotation_step < 0.5:
                rotation_step = rotation_step * 0.9985
            else:
                rotation_step = rotation_step * 0.999
            if current_degree < next_sound_angle:
                sound_click()
                next_sound_angle -= play_sound_step
                current_result()
            if current_degree <= -360:
                current_degree += 360
                next_sound_angle += 360

    if rotation_step > 0:
        turn_wheel()

# Quit Pygame
pygame.quit()
