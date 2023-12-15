import matplotlib
import matplotlib.pyplot as pt
from matplotlib.backends.backend_pdf import PdfPages
from pygame import gfxdraw

matplotlib.use('pgf')
dt = 10 ** (-12)


def acceleration_by_y(electron, condenser):
    return (electron.Charge * condenser.field_y_component(electron.Y)) / electron.Mass


def evaluate(electron, condenser, time):
    while electron.X < condenser.Length and electron.Y > 0:
        dvy = acceleration_by_y(electron, condenser)
        electron.VelocityByY += dvy * dt
        electron.Y += electron.VelocityByY * dt
        electron.X += electron.VelocityByX * dt
        time += dt
    return time - dt


def evaluate_all_values(electron, condenser, time):
    t = []
    x = []
    y = []
    v_y = []
    a_y = []
    while electron.X < condenser.Length or electron.Y > 0:
        y.append(electron.Y * 100)
        x.append(electron.X * 100)
        t.append(time)
        dvy = acceleration_by_y(electron, condenser)
        a_y.append(dvy)
        electron.VelocityByY += dvy * dt
        v_y.append(electron.VelocityByY)
        electron.Y += electron.VelocityByY * dt
        electron.X += electron.VelocityByX * dt
        time += dt
    return [t, x, y, v_y, a_y]


def format_number(number):
    return '{:e}'.format(number).replace('e', '*10^').replace('+', "")


def add_graph(x_values, y_values, title, x_label, y_label):
    pt.figure()
    pt.title(title)
    pt.xlabel(x_label)
    pt.ylabel(y_label)
    pt.plot(x_values, y_values)
    pt.grid()


def save_graphs(filename):
    p = PdfPages(filename)
    fig_nums = pt.get_fignums()
    figs = [pt.figure(n) for n in fig_nums]

    for fig in figs:
        p.savefig(fig)
    p.close()


def draw_circle(surface, color, pos, radius):
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), radius, color)
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), radius, color)
