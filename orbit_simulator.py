import math, turtle

xpos = 1.496e+11 # meters
ypos = 0.0 # meters
vel_x = 0.0 # m/s
vel_y = 29784 # m/s
mass_earth = 5.972e+24 # kg
sun_x = 0.0 # meters
sun_y = 0.0 # meters
mass_sun = 1.989e+30 # kg
time_step = 86400 * 10 # seconds
scale = 1e+10

def calculate_gravity(distance, g=6.67e-11):
    gravity = g * mass_earth * mass_sun / distance**2
    return gravity

def split_force(force, distance, xpos=xpos, ypos=ypos):
    force_x = xpos * force / distance
    force_y = ypos * force / distance
    return (force_x, force_y)

def calc_velocity(force, time):
    accel = force / mass_earth
    vel_change = accel * time
    return vel_change

if __name__ == '__main__':  
    s = turtle.getscreen()
    t = turtle.Turtle()
    t.penup()
    t.color('orange')
    t.goto(sun_x, sun_y)
    t.dot(6)
    earth = t.clone()
    earth.color('blue')
    earth.pendown()

    while True:
        distance = math.sqrt((sun_x - xpos)**2 + (sun_y - ypos)**2)
        gravity = calculate_gravity(distance)
        forces = split_force(gravity, distance)
        vel_x += calc_velocity(forces[0], time_step )
        vel_y += calc_velocity(forces[1], time_step )
        xpos += (vel_x * time_step)
        ypos += (vel_y * time_step)
        #print('{:.3e}'.format(vel_y))
        x_scaled = xpos/scale
        y_scaled = ypos/scale
        #print('{:.3e}'.format(y_scaled))
        earth.setpos(xpos/scale, ypos/scale)
