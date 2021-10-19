import math
import cairo
import Participant
from PIL import Image
import numpy as np
import random

WIDTH, HEIGHT = 600, 600
r = 0.05


# This function is a mess. I am SURE there has to be a more elegant solution
def find_angle(x1, y1, x2, y2):
    if x2 == x1:
        if y2 > y1:
            return math.pi / 2
        else:
            return -math.pi / 2
    elif y1 == y2:
        if x1 > x2:
            return math.pi
        else:
            return 0
    else:
        arrow_angle = np.arctan((y2 - y1) / (x2 - x1))
        # print(arrow_angle)
        # II quadrant
        if y2 > y1 and x2 < x1:
            # print(2)
            arrow_angle += math.pi
        # III quadrant
        elif y2 < y1 and x2 < x1:
            # print(3)
            arrow_angle += math.pi
        return arrow_angle


def set_color(role):
    if role == 'physics':
        ctx.set_source_rgb(0.7, 0.2, 0)
    elif role == 'business':
        ctx.set_source_rgb(0, 0.5, 0)
    elif role == 'software':
        ctx.set_source_rgb(0.1, 0, 1)
    else:
        ctx.set_source_rgb(0, 0, 0)


def draw_arrow(x1, y1, x2, y2, role):
    # print(x1, y1, x2, y2)
    arrow_length = np.linalg.norm(np.array([x1, y1] - np.array([x2, y2]))) - r
    if arrow_length > 0.1:

        arrow_angle = find_angle(x1, y1, x2, y2)
        # print(arrow_angle * 180 / math.pi)

        arrowhead_angle = math.pi / 6
        arrowhead_length = 0.05

        ctx.move_to(x1, y1)

        ctx.rel_line_to(arrow_length * math.cos(arrow_angle), arrow_length * math.sin(arrow_angle))
        ctx.rel_move_to(-arrowhead_length * math.cos(arrow_angle - arrowhead_angle),
                        -arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        ctx.rel_line_to(arrowhead_length * math.cos(arrow_angle - arrowhead_angle),
                        arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        ctx.rel_line_to(-arrowhead_length * math.cos(arrow_angle + arrowhead_angle),
                        -arrowhead_length * math.sin(arrow_angle + arrowhead_angle))

        set_color(role)
        ctx.set_line_width(0.01)
        ctx.stroke()


def draw_text(x, y, txt):
    ctx.move_to(x, y)
    ctx.show_text(txt)


def draw_coordinate_system():
    border = 1.2
    draw_arrow(0, 0, border, border, "")
    draw_arrow(0, 0, -border, border, "")
    draw_arrow(0, 0, border, -border, "")
    draw_arrow(0, 0, -border, -border, "")
    border = 1
    x_offset = 0.1
    draw_text(border + x_offset, border, "c2")
    draw_text(-border - x_offset, border, "c1")
    draw_text(border + x_offset, -border, "c4")
    draw_text(-border - x_offset, -border, "c3")


def draw_participant(participant):
    set_color(participant.role)
    ctx.arc(participant.x, participant.y, r, 0, 2 * math.pi)
    ctx.close_path()
    ctx.fill()


def draw_idx(participant, idx):

    dist = 0.1
    angle = idx % 4 * math.pi / 4
    x_offset = dist * math.cos(angle)
    y_offset = dist * math.sin(angle)

    ctx.move_to(participant.x - r/2 + x_offset, participant.y + 0.02 + y_offset)
    ctx.show_text(str(idx))


def calculate_participant_position(participant):
    x = (1 / 4) * (-(participant.c[0] - 1) + (participant.c[1] - 1) - (participant.c[2] - 1) + (participant.c[3] - 1))
    y = (1 / 4) * ((participant.c[0] - 1) + (participant.c[1] - 1) - (participant.c[2] - 1) - (participant.c[3] - 1))
    d = 1 + abs((x + y) * (x - y)) / 4
    x /= d
    y /= d
    return x, y


def add_noise(participants, noise_size):
    for i in range(len(participants)):
        angle = random.uniform(0, 1) * 2 * math.pi
        participants[i].x += noise_size * math.cos(angle)
        participants[i].y += noise_size * math.sin(angle)
    return participants


if __name__ == "__main__":

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    canvas_size = 2.5
    ctx.scale(WIDTH/canvas_size, HEIGHT/canvas_size)  # Normalizing the canvas
    ctx.translate(canvas_size/2, canvas_size/2)
    ctx.set_line_width(9)

    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(0.05)

    participants = Participant.load_participants_from_csv('dummy_data.csv')

    # Calculate positions
    for participant in participants:
        participant.x, participant.y = calculate_participant_position(participant)

    # # Add a little noise to make the distances bigger, if needed:
    noise_size = 0.05
    participant = add_noise(participants, noise_size)

    # Draw
    for c, participant in enumerate(participants):
        draw_participant(participant)
        for friend_name in participant.friends:
            if isinstance(friend_name, str):
                friend = Participant.get_participant_by_name(participants, friend_name)
                # draw_participant(friend_object) # TMP
                draw_arrow(participant.x, participant.y, friend.x, friend.y, participant.role)

    draw_coordinate_system()

    for c, participant in enumerate(participants):
        ctx.set_source_rgb(1, 0, 0.8)
        # draw_idx(participant, c + 1)
        draw_text(participant.x, participant.y, participant.name)

    surface.write_to_png("example.png")

    img = Image.open('example.png')
    img.show()
