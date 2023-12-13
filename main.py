from math import log

from electron import Electron
import matplotlib.pyplot as pt

with open("config.txt", "r") as f:
    a = [float(item) for item in f.read().split(" ")]
Umax = 1000
Umin = 0
while Umax - Umin > 0.0000001:
    electron = Electron(a[2], a[0] / 100, a[1] / 100, a[3] / 100)
    U = (Umax + Umin) / 2
    electron.motion(U)
    if electron.X >= electron.l_:
        Umin = U
    else:
        Umax = U
electron = Electron(a[2], a[0] / 100, a[1] / 100, a[3] / 100)
yx, vy, ay, yt = electron.motion_for_graphic(U)
print("Минимальное напряжение", U)
print("Время полета", electron.t)
print("Скорость конечная", (electron.VelocityByY ** 2 + electron.VelocityByX ** 2) ** 0.5)
pt.title('Зависимость высоты от расстояния')
pt.xlabel('Пройденное расстояние, см')
pt.ylabel('Высота, см')
pt.plot([i[0] for i in yx], [i[1] for i in yx])
pt.grid()
pt.savefig('y(x)', )
pt.show()
pt.title('Зависимость скорости от времени')
pt.xlabel('Время, c')
pt.ylabel('Скорость, см/c')
pt.grid()
pt.plot([i[0] for i in vy], [i[1] for i in vy])
pt.savefig('Vy(t)', )
pt.show()
pt.title('Зависимость ускорения от времени')
pt.xlabel('Время, c')
pt.ylabel('Ускорение, см/c^2')
pt.grid()
pt.plot([i[0] for i in ay], [i[1] for i in ay])
pt.savefig('ay(t)', )
pt.show()
pt.title('Зависимость высоты от времени')
pt.xlabel('Время, с')
pt.ylabel('Высота, см')
pt.grid()
pt.plot([i[0] for i in yt], [i[1] for i in yt])
pt.savefig('y(t)', )
pt.show()
