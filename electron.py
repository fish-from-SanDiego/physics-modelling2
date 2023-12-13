from math import log


class Electron:
    dt = 1 / 1000000000000

    def __init__(self, initial_velocity, r1, r2, l):
        self.X = 0
        self.Y = (r2 - r1) / 2 + r1
        self.r1 = r1
        self.r2 = r2
        self.VelocityByX = initial_velocity
        self.VelocityByY = 0
        self.Charge = -1.6 * 10 ** -19
        self.Mass = 9.1 * 10 ** -31
        self.l_ = l
        self.t = 0

    def aay(self, voltage):
        return (self.Charge * voltage) / (self.Y * self.Mass * log(self.r2 / self.r1))

    def motion(self, voltage):
        while self.X < self.l_ and self.Y > self.r1:
            dvy = self.aay(voltage)
            self.VelocityByY += dvy * Electron.dt
            self.Y += self.VelocityByY * Electron.dt
            self.X += self.VelocityByX * Electron.dt
            self.t += Electron.dt

    def motion_for_graphic(self, voltage):
        yx = []
        vy = []
        ay = []
        yt = []
        while self.X < self.l_ or self.Y > self.r1:
            yx.append((self.X * 100, self.Y * 100))
            vy.append((self.t, self.VelocityByY * 100))
            dvy = self.aay(voltage)
            ay.append((self.t, dvy * 100))
            yt.append((self.t, self.Y * 100))
            self.VelocityByY += dvy * Electron.dt
            self.Y += self.VelocityByY * Electron.dt
            self.X += self.VelocityByX * Electron.dt
            self.t += Electron.dt
        return [yx, vy, ay, yt]
