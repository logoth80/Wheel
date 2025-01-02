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
bg_color = (146, 43, 33)
colors = [
    (198, 40, 40),  # Red
    (118, 68, 138),
    (130, 224, 170),
    (51, 153, 0),  # Green
    (40, 53, 147),  # Blue
    (255, 125, 0),
    (0, 255, 255),  # Cyan
    (241, 196, 15),  # Yellow
    (0, 125, 255),
    (175, 122, 197),  # Magenta
    (238, 238, 238),
    (60, 60, 60),
]
texts = ["BANKRUT", "2500", "200", "300", "500", "Wycieczka", "750", "1000", "1500", "Niespodzianka", "100", "5000"]

# Starting point of the triangles
center_x, center_y = width // 2, height // 2

pies = 24
# Angle between each triangle in degrees
angle_of_pie = 360 / pies
current_degree = -1
rotation_tick = 0.004
wheel_rotation_step = 0
last_tick_time = time.time()
last_rest = 0
play_sound_step = 360 / (3 * pies)  # 3 spokes per pie 0, 1/3, 2/3, (4th in next)
next_sound_angle = -play_sound_step
click_sound = pygame.mixer.Sound("click.mp3")

# Set up the font
font_wheel = pygame.font.SysFont("Book Antiqua", int(24 * line_length / 280))  # None uses the default system font
# font_wheel.bold = True
font_result = pygame.font.SysFont("Georgia", 36)
font_fps = pygame.font.SysFont("Arial", 16)
added_power = 0


def roll_wheel(power_added):
    global wheel_rotation_step
    power_added = power_added - 0.40 * power_added + random.random() * power_added / 2.5
    wheel_rotation_step = power_added / 100
    if power_added > 0:
        global wheel_moving
        wheel_moving = True


def sound_click():
    click_sound.set_volume(0.3 + wheel_rotation_step)
    click_sound.play()


def draw_power(power):
    x = 180
    multi = (line_length * 2) / 120
    prop = int(line_length / (line_length * multi) + 1)
    for p in range(int(power * multi)):
        pygame.draw.rect(screen, (25, 200, 0), pygame.Rect(2 * line_length + x, center_y + line_length - p * prop - 6, 50, 8))
    for p in range(0, int(power * multi), 20):
        pygame.draw.rect(
            screen,
            (240, max(0, int((240 - 0.4 * p) / 10)) * 10, 0),
            pygame.Rect(2 * line_length + x + 2, center_y + line_length - 3 - p * prop - 19, 46, int(line_length / 100) + 18),
        )
        pygame.draw.rect(
            screen,
            (200, max(0, int((200 - 0.4 * p) / 10)) * 10, 0),
            pygame.Rect(2 * line_length + x + 2, center_y + line_length - 1 - p * prop - 17, 44, int(line_length / 100) + 16),
        )


teststart = time.time()
fpstest = 0
fps = 0

running = True
# main loop
while running:
    fpstest += 1
    if fpstest % 1000 == 0:
        fps = 1000 / (time.time() - teststart)
        teststart = time.time()

    screen.fill(bg_color)
    text_surface = font_fps.render("FPS: " + str(int(fps)), True, black)
    screen.blit(text_surface, (width - 66, height - 21))

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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not wheel_moving:
        added_power += 0.7
        added_power = min(line_length / 2, added_power)
        draw_power(added_power)

    if pygame.mouse.get_pressed()[0] and not wheel_moving:
        added_power += 0.7
        added_power = max(added_power, 15)
        added_power = min(line_length / 2, added_power)
        draw_power(added_power)
    elif pygame.mouse.get_pressed()[2] and wheel_moving:
        if wheel_rotation_step > 0.3:
            wheel_rotation_step *= 0.998

    def draw_wheel(degree):
        current_angle = degree
        for i in range(pies):
            end_x = center_x + line_length * math.cos(math.radians(current_angle))
            end_y = center_y - line_length * math.sin(math.radians(current_angle))

            third_vertex_x = center_x + line_length * math.cos(math.radians(current_angle + angle_of_pie))
            third_vertex_y = center_y - line_length * math.sin(math.radians(current_angle + angle_of_pie))

            temp_color = colors[i % len(colors)]

            pygame.draw.polygon(screen, temp_color, [(center_x, center_y), (end_x, end_y), (third_vertex_x, third_vertex_y)], width=0)

            if wheel_rotation_step == 0:
                gfxdraw.aapolygon(screen, [(center_x, center_y), (end_x, end_y), (third_vertex_x, third_vertex_y)], temp_color)

            gfxdraw.aacircle(screen, center_x, center_y, line_length + 1, gold)
            pygame.draw.circle(screen, gold, (center_x, center_y), radius=line_length + 1, width=7)
            gfxdraw.aacircle(screen, center_x, center_y, line_length - 6, gold)

            # Calculate text position for each triangle
            text_angle = current_angle + angle_of_pie / 2
            # Render text into a surface
            temp_text = texts[i % len(texts)]
            if temp_color[0] + temp_color[1] + temp_color[2] >= 340:
                text_surface = font_wheel.render(temp_text, 1, black)
            else:
                text_surface = font_wheel.render(temp_text, 1, (255, 241, 118))

            offset = int(0.5 * text_surface.get_width()) + 20
            t1_x = center_x + ((line_length - offset) * math.cos(math.radians(text_angle)))  # Adjusted distance
            t1_y = center_y - ((line_length - offset) * math.sin(math.radians(text_angle)))

            # Rotate the text surface
            rotated_text_surface = pygame.transform.rotate(text_surface, text_angle)

            # Get the rectangle of the rotated surface to center it
            rotated_rect = rotated_text_surface.get_rect(center=(t1_x, t1_y))
            screen.blit(rotated_text_surface, rotated_rect)

            current_angle += angle_of_pie

        for i in range(3 * pies):  # spokes
            degree_1 = i * (360 / (3 * pies)) + current_degree
            x1 = int(center_x + (line_length - 2.5) * math.cos(math.radians(degree_1)))
            y1 = int(center_y - (line_length - 2.5) * math.sin(math.radians(degree_1)))
            gfxdraw.aacircle(screen, x1, y1, 3, (60, 60, 60))
            pygame.draw.circle(screen, silver, (x1, y1), 3)

    def current_result():
        current_index = int(((-90 - current_degree) % 360) / (360 / pies))
        return current_index % len(texts)

    if wheel_rotation_step == 0 or wheel_rotation_step != 0:
        index = current_result()
        temp_color = colors[index % len(colors)]
        if temp_color[0] + temp_color[1] + temp_color[2] < 330:
            temp_color_text = (255, 241, 118)
        else:
            temp_color_text = black
        text_surface = font_result.render(texts[index], 100, temp_color_text)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        offset = line_length // 2 - text_width // 2
        x1 = offset
        y1 = 20
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(x1, y1, text_width + 23, text_height + 26))
        pygame.draw.rect(screen, colors[index], pygame.Rect(x1 + 3, y1 + 3, text_width + 17, text_height + 20))
        screen.blit(text_surface, (x1 + 13, y1 + 13))

    draw_wheel(current_degree)
    draw_power(added_power)

    pygame.draw.polygon(
        screen,
        (200, 0, 0),
        [(center_x, center_y - line_length + 5), (center_x - 5, center_y - line_length - 15), (center_x + 5, center_y - line_length - 15)],
        0,
    )

    pygame.display.flip()

    def turn_wheel():
        global last_tick_time, current_degree, next_sound_angle, wheel_rotation_step, wheel_moving

        if time.time() > last_tick_time + rotation_tick:
            last_tick_time = time.time()
            current_degree -= wheel_rotation_step

            if wheel_rotation_step < 0.02:
                wheel_rotation_step = 0
                wheel_moving = False
            elif wheel_rotation_step < 0.08:
                wheel_rotation_step = wheel_rotation_step * 0.996
            elif wheel_rotation_step < 0.2:
                wheel_rotation_step = wheel_rotation_step * 0.9975
            elif wheel_rotation_step < 0.5:
                wheel_rotation_step = wheel_rotation_step * 0.9985
            else:
                wheel_rotation_step = wheel_rotation_step * 0.999
            if current_degree < next_sound_angle:
                sound_click()
                next_sound_angle -= play_sound_step
                current_result()
            if current_degree <= -360:
                current_degree += 360
                next_sound_angle += 360

    if wheel_rotation_step > 0:
        turn_wheel()

pygame.quit()
