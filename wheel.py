import pygame
import math
import time

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("36 Triangles from a Point")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
]
texts = ["BANKRUT", "2500", "200", "300", "500", "WYCIECZKA", "750", "1000", "1500", "Niespodzianka", "100", "5000"]

# Starting point of the triangles
center_x, center_y = width // 2, height // 2

# Length of each line
line_length = 250
pies = 24
# Angle between each triangle in degrees
angle_step = 360 / pies
current_degree = 0
rotation_tick = 0.004
rotation_step = 0.3
last_tick_time = time.time()

# Set up the font
font = pygame.font.Font(None, 24)  # None uses the default system font


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    def draw_wheel(degree):
        # Draw pies * triangles
        current_angle = degree
        for i in range(pies):
            end_x = center_x + line_length * math.cos(math.radians(current_angle))
            end_y = center_y - line_length * math.sin(math.radians(current_angle))

            third_vertex_x = center_x + line_length * math.cos(math.radians(current_angle + angle_step))
            third_vertex_y = center_y - line_length * math.sin(math.radians(current_angle + angle_step))

            # Draw and fill the triangle
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

            pygame.draw.circle(screen, black, (center_x, center_y), radius=line_length + 2, width=4)

            # Calculate text position for each triangle
            text_angle = current_angle + angle_step / 2
            word_len = texts[i % len(texts)]
            t1_x = center_x + (line_length - 20 - 5 * len(texts[i % len(texts)])) * math.cos(math.radians(text_angle))  # Adjusted distance
            t1_y = center_y - (line_length - 20 - 5 * len(texts[i % len(texts)])) * math.sin(math.radians(text_angle))

            # Render text into a surface
            text_surface = font.render(texts[i % len(texts)], True, black)

            # Rotate the text surface
            rotated_text_surface = pygame.transform.rotate(text_surface, text_angle)

            # Get the rectangle of the rotated surface to center it
            rotated_rect = rotated_text_surface.get_rect(center=(t1_x, t1_y))
            screen.blit(rotated_text_surface, rotated_rect)

            current_angle += angle_step

    draw_wheel(current_degree)

    # Update the display
    pygame.display.flip()
    if time.time() > last_tick_time + rotation_tick:
        current_degree -= rotation_step
        if current_degree <= -360:
            current_degree += 360
        last_tick_time = time.time()


# Quit Pygame
pygame.quit()
