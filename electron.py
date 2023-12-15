class Electron:

    def __init__(self, initial_velocity, condenser):
        self.X = 0
        self.Y = (condenser.OuterRadius - condenser.InnerRadius) / 2
        self.VelocityByX = initial_velocity
        self.VelocityByY = 0
        self.Charge = -1.6 * 10 ** -19
        self.Mass = 9.1 * 10 ** -31
