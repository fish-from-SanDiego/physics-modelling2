import sys

import matplotlib
import pygame

import funcs
from condenser import Condenser
from electron import Electron
import matplotlib.pyplot as pt


class Point:
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y


FPS = 240
TOTAL_FRAMES = 600
GREY_COLOR = (128, 128, 128)
BLACK_COLOR = (0, 0, 0)
CARDINAL_COLOR = (196, 30, 58)
BLUE_COLOR = (128, 166, 255)
params = {'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'large',
          'ytick.labelsize': 'large',
          "figure.autolayout": True,
          "figure.figsize": [7.00, 3.50],
          'text.usetex': True,
          }
matplotlib.use('pgf')
pt.rcParams.update(params)
pt.ioff()

with open("config.txt", "r") as f:
    config = [float(item) for item in f.read().split(" ")]
voltage = max_voltage = 1000000
min_voltage = 0
time = 0
while max_voltage - min_voltage > 0.0000000001:
    voltage = (max_voltage + min_voltage) / 2
    condenser = Condenser(config[3] / 100, config[0] / 100, config[1] / 100, voltage)
    electron = Electron(config[2], condenser)
    time = funcs.evaluate(electron, condenser, 0)
    if electron.X >= condenser.Length:
        min_voltage = voltage
    else:
        max_voltage = voltage

condenser = Condenser(config[3] / 100, config[0] / 100, config[1] / 100, voltage)
electron = Electron(config[2], condenser)

t, x, y, v_y, a_y = funcs.evaluate_all_values(electron, condenser, 0)

funcs.add_graph(x, y, r' $y(x)$', '$x$, $cm$', '$y$, $cm$')
funcs.add_graph(t, v_y, r' $v_y(t)$', '$t$, $s$', r'$v_y(t), \frac{m}{s}$')
funcs.add_graph(t, a_y, r' $a_y(t)$', '$t$, $s$', r'$a_y(t), \frac{m}{s^2}$')
funcs.add_graph(t, y, r' $y(t)$', '$t$, $s$', r'$y(t), cm$')
funcs.save_graphs('graphs.pdf')

pygame.init()
display = pygame.display
display.set_caption('Моделирование \'Частица в конденсаторе\'')
info = pygame.display.Info()
k = 0.7
screen = pygame.display.set_mode((info.current_w * k, info.current_h * k))
width, height = screen.get_size()

origin_offset_w = 0.1
origin_offset_h = 0.3
origin = Point(width * origin_offset_w, height * (1 - origin_offset_h))
c_length = 0.5 * width
transform_coefficient = c_length / condenser.Length
c_inner_radius = condenser.InnerRadius * transform_coefficient
c_outer_radius = condenser.OuterRadius * transform_coefficient
c_inner = pygame.Rect((origin.X, origin.Y), (c_length, 2 * c_inner_radius))

outer_lt = (origin.X, origin.Y - (c_outer_radius - c_inner_radius))
outer_rt = (origin.X + c_length, origin.Y - (c_outer_radius - c_inner_radius))
outer_lb = (origin.X, origin.Y + c_inner_radius + c_outer_radius)
outer_rb = (origin.X + c_length, origin.Y + c_inner_radius + c_outer_radius)

clock = pygame.time.Clock()
axis_label_font = pygame.font.SysFont('arial', 60)
math_font = pygame.font.SysFont('cambriamath', 50)
x_label = axis_label_font.render('x', True, GREY_COLOR)
y_label = axis_label_font.render('y', True, GREY_COLOR)

t_screen = []
x_screen = []
y_screen = []
vy_screen = []
shift = len(t) // TOTAL_FRAMES
for i in range(0, len(t), shift):
    t_screen.append(t[i])
    x_screen.append(origin.X + x[i] / 100 * transform_coefficient)
    y_screen.append(origin.Y - y[i] / 100 * transform_coefficient)
    vy_screen.append(v_y[i])
t_screen.append(t[-1])
x_screen.append(origin.X + x[-1] / 100 * transform_coefficient)
y_screen.append(origin.Y - y[-1] / 100 * transform_coefficient)
vy_screen.append(v_y[-1])

electron_radius = 15
counter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, GREY_COLOR, (-1, origin.Y), (width + 1, origin.Y), 2)
    pygame.draw.line(screen, GREY_COLOR, (origin.X, -1), (origin.X, height + 1), 2)
    pygame.draw.line(screen, BLUE_COLOR, outer_lt, outer_lb, 2)
    pygame.draw.line(screen, BLUE_COLOR, outer_rt, outer_rb, 2)
    pygame.draw.rect(screen, BLACK_COLOR, c_inner, 5)
    pygame.draw.line(screen, BLACK_COLOR, outer_lt, outer_rt, 5)
    pygame.draw.line(screen, BLACK_COLOR, outer_lb, outer_rb, 5)
    t_text = math_font.render(f't = {funcs.format_number(t_screen[counter])} с', True, BLACK_COLOR)
    v_text = math_font.render(
        f'|v| = {funcs.format_number((electron.VelocityByX ** 2 + vy_screen[counter] ** 2) ** 0.5)} м/с', True,
        BLACK_COLOR)
    screen.blit(x_label, (width - x_label.get_width() * 1.5, origin.Y))
    screen.blit(y_label, (origin.X - y_label.get_width() * 1.5, 0))
    screen.blit(t_text, (width - 600, 0))
    screen.blit(v_text, (width - 600, t_text.get_height()))
    funcs.draw_circle(screen, CARDINAL_COLOR, (x_screen[counter], y_screen[counter]), electron_radius)
    display.flip()
    if counter == 0:
        pygame.time.wait(2000)
    if counter < len(t_screen) - 1:
        counter += 1
    clock.tick(FPS)
