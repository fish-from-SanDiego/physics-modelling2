import matplotlib

import funcs
from condenser import Condenser
from electron import Electron
import matplotlib.pyplot as pt

params = {'axes.labelsize': 'large',
          'axes.titlesize': 'large',
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

y_x, vy_t, ay_t, y_t = funcs.evaluate_all_values(electron, condenser, 0)
print("Минимальное напряжение", voltage, "В")
print("Время полета", time, "с")
print("Конечная скорость", funcs.format_number((electron.VelocityByY ** 2 + electron.VelocityByX ** 2) ** 0.5), "м/с")

fig = pt.figure()

funcs.add_graph(y_x, r'Зависимость $y(x)$', '$x$, см', '$y$, см')
funcs.add_graph(vy_t, r'Зависимость $v_y(t)$', '$t$, с', r'$v_y(t), \frac{\text{см}}{\text{с}}$')

# pt.title('Зависимость ускорения от времени')
# pt.xlabel('Время, c')
# pt.ylabel('Ускорение, м/c^2')
# pt.grid()
# pt.plot([i[0] for i in ay_t], [i[1] for i in ay_t])
# pt.savefig('ay(t)', )
# pt.close()
#
# pt.title('Зависимость высоты от времени')
# pt.xlabel('Время, с')
# pt.ylabel('Высота, см')
# pt.grid()
# pt.plot([i[0] for i in y_t], [i[1] for i in y_t])
# pt.savefig('y(t)', )
# pt.close()
funcs.save_graphs('graphs.pdf')
