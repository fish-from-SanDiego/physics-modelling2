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


def evaluate_graph_values(electron, condenser, time):
    y_x = []
    vy_t = []
    ay_t = []
    y_t = []
    while electron.X < condenser.Length or electron.Y > 0:
        y_x.append((electron.X * 100, electron.Y * 100))
        vy_t.append((time, electron.VelocityByY * 100))
        dvy = acceleration_by_y(electron, condenser)
        ay_t.append((time, dvy * 100))
        y_t.append((time, electron.Y * 100))
        electron.VelocityByY += dvy * dt
        electron.Y += electron.VelocityByY * dt
        electron.X += electron.VelocityByX * dt
        time += dt
    return [y_x, vy_t, ay_t, y_t]
