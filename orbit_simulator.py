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
scale = 1e+9

def calculate_gravity(distance, g=6.67e-11):
    gravity = g * mass_earth * mass_sun / distance**2
    return gravity

def split_force(force, distance, xpos, ypos):
    force_x = -xpos * force / distance
    #print('{:.3e} * {:.3e} / {:.3e} = {:.3e}'.format(-xpos, force, distance, force_x))
    force_y = -ypos * force / distance
    return (force_x, force_y)

def calc_velocity(force, time):
    accel = force / mass_earth
    #print('{:.3e}'.format(accel))
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

    for i in range(int(1e+9)):
        #print('Iteration {}, '.format(i, xpos), end='')
        distance = math.sqrt((sun_x - xpos)**2 + (sun_y - ypos)**2)
        gravity = calculate_gravity(distance)
        forces = split_force(gravity, distance, xpos, ypos)
        #print('xpos: {:.3e}, x accel: '.format(xpos), end='')   

        vel_x += calc_velocity(forces[0], time_step )
        #print('ypos: {:.3e}, y accel:'.format(ypos), end='')
        vel_y += calc_velocity(forces[1], time_step )
        #print()
        xpos += (vel_x * time_step)
        ypos += (vel_y * time_step)
        
        x_scaled = xpos/scale
        y_scaled = ypos/scale
        earth.setpos(xpos/scale, ypos/scale)
        earth.pendown()
