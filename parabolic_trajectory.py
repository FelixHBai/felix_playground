import math, turtle

#vel_x = 20
#vel_y = 60
clones = 5
clone_list = []
properties = [[80, 65, 0.1, turtle.Turtle()], 
              [80, 56, 0.1, turtle.Turtle()],
              [80, 45, 0.1, turtle.Turtle()],
              [80, 35, 0.1, turtle.Turtle()],
              [80, 25, 0.1, turtle.Turtle()]
              ]
starting_y = -300

class Projectile:
    def __init__(self, vel_magnitude, vel_direction, scale, turtle_instance, starting_y = -300, g=9.8):
        self.vel_magnitude = vel_magnitude
        self.vel_direction = vel_direction
        self.scale = scale
        self.g = g
        self.t = turtle_instance

        self.vel_x = math.cos(vel_direction * math.pi/180) * vel_magnitude
        self.vel_y = math.sin(vel_direction * math.pi/180) * vel_magnitude
        self.ypos = starting_y

    def move(self):
        t.goto(t.xcor() + self.vel_x * self.scale,
               t.ycor() + self.vel_y * self.scale)
        self.vel_y -= self.g * self.scale
        self.ypos += self.vel_y * self.scale

'''def calc_velocity(vel_y, scale, g=9.8):
    vel_y += g * scale'''

if __name__ == '__main__':
    s = turtle.getscreen()
    t = turtle.Turtle()
    '''t.up()
    t.goto(-100, -100)
    t.down()'''
    for i in range(clones):
        c = Projectile(properties[i][0], properties[i][1], properties[i][2], properties[i][3])
        clone_list.append(c)
    for c in clone_list:
        t.up()
        t.speed(0)
        t.goto(-300, starting_y)
        t.down()
        t.speed(6)
        while c.ypos >= starting_y:
            c.move()
    '''while t.ycor() >= -100:
        t.goto(t.xcor() + vel_x * scale, 
               t.ycor() + vel_y * scale)
        vel_y -= g * scale'''
    
    input()
