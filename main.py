from math import log

import funcs
from condenser import Condenser
from electron import Electron
import matplotlib.pyplot as pt

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

y_x, vy_t, ay_t, y_t = funcs.evaluate_graph_values(electron, condenser, 0)
print("Минимальное напряжение", voltage)
print("Время полета", time)
print("Скорость конечная", (electron.VelocityByY ** 2 + electron.VelocityByX ** 2) ** 0.5)
pt.title('Зависимость высоты от расстояния')
pt.xlabel('Пройденное расстояние, см')
pt.ylabel('Высота, см')
pt.plot([i[0] for i in y_x], [i[1] for i in y_x])
pt.grid()
pt.savefig('y(x)', )
pt.show()
pt.title('Зависимость скорости от времени')
pt.xlabel('Время, c')
pt.ylabel('Скорость, см/c')
pt.grid()
pt.plot([i[0] for i in vy_t], [i[1] for i in vy_t])
pt.savefig('Vy(t)', )
pt.show()
pt.title('Зависимость ускорения от времени')
pt.xlabel('Время, c')
pt.ylabel('Ускорение, см/c^2')
pt.grid()
pt.plot([i[0] for i in ay_t], [i[1] for i in ay_t])
pt.savefig('ay(t)', )
pt.show()
pt.title('Зависимость высоты от времени')
pt.xlabel('Время, с')
pt.ylabel('Высота, см')
pt.grid()
pt.plot([i[0] for i in y_t], [i[1] for i in y_t])
pt.savefig('y(t)', )
pt.show()
