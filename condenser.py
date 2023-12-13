from math import log


class Condenser:
    def __init__(self, length, inner_radius, outer_radius, voltage):
        self.Length = length
        self.InnerRadius = inner_radius
        self.OuterRadius = outer_radius
        self.Voltage = voltage

    def field_y_component(self, y):
        return self.Voltage / (log(self.OuterRadius / self.InnerRadius) * (y + self.InnerRadius))
    # E = U / (ln(R / r) * dist)
