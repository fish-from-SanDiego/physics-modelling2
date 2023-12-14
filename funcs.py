import matplotlib
import matplotlib.pyplot as pt
from matplotlib.backends.backend_pdf import PdfPages

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
    return time


def evaluate_all_values(electron, condenser, time):
    y_x = []
    vy_t = []
    ay_t = []
    y_t = []
    while electron.X < condenser.Length or electron.Y > 0:
        y_x.append((electron.X * 100, electron.Y * 100))
        vy_t.append((time, electron.VelocityByY))
        dvy = acceleration_by_y(electron, condenser)
        ay_t.append((time, dvy))
        y_t.append((time, electron.Y * 100))
        electron.VelocityByY += dvy * dt
        electron.Y += electron.VelocityByY * dt
        electron.X += electron.VelocityByX * dt
        time += dt
    return [y_x, vy_t, ay_t, y_t]


def format_number(number):
    return '{:e}'.format(number).replace('e', '*10^').replace('+', "")


def add_graph(values, title, xlabel, ylabel):
    pt.figure()
    pt.title(title)
    pt.xlabel(xlabel)
    pt.ylabel(ylabel)
    pt.plot([i[0] for i in values], [i[1] for i in values])
    pt.grid()


def save_graphs(filename):
    p = PdfPages(filename)
    fig_nums = pt.get_fignums()
    figs = [pt.figure(n) for n in fig_nums]

    for fig in figs:
        p.savefig(fig)
    p.close()
