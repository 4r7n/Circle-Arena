import turtle, math, random

turtle.hideturtle()
turtle.speed("fastest")
turtle.colormode(255)

turtle.title("Arun")

turtle.tracer(0)

sc = turtle.Screen()

frameD = 120
frame_delay_ms = 1000 // frameD

restit = 1
gravity = -9.80665

circ = []

def baseWalls():
    turtle.setup(width=600, height=800)
    wall = turtle.Turtle()
    wall.hideturtle()
    wall.penup()
    wall.shape("square")

    wall.shapesize(2.5, 30)
    firinst = False

    for i in range(4):
        wall.hideturtle()
        wall.color("LightCyan"+str(4-i))
        wall.goto(0, 275+50*i)
        wall.showturtle()
        wall.stamp()

        wall.hideturtle()
        wall.goto(0, -275-50*i)
        wall.showturtle()
        wall.stamp()
        if firinst == False:
            wall.goto(0, -300)
            wall.color("LightCyan2")
            wall.write("Arun", align="center", font=("helvetica", 32, "italic"))
            firinst = True

    wall.hideturtle()
    wall.color("LightCyan4")
    wall.shapesize(25, 2.5)
    wall.goto(-275 ,0)
    wall.showturtle()
    wall.stamp()

    wall.hideturtle()
    wall.goto(275 ,0)
    wall.showturtle()
    wall.stamp()

    turtle.update()


def testCirc():
    alpha = []
    alpha.append(Ball(-200, 0, col="firebrick4", rad=3.5))
    alpha.append(Ball(200, 0, col="dodgerblue4", rad=3.5))
    #alpha.append(Ball(0, -200, col="darkseagreen4", rad=2.5))
    #alpha.append(Ball(0, 200, col="khaki4", rad=2.5))

    #alpha.append(Ball(0, 0, col="darkmagenta", rad=10, m=16))


    alpha[0].setVel(random.randint(1,20), random.randint(0, 360))
    alpha[1].setVel(random.randint(1,20), random.randint(0, 360))
    #alpha[2].setVel(random.randint(1,20), random.randint(0, 360))
    #alpha[3].setVel(random.randint(1,20), random.randint(0, 360))

    #alpha[4].setVel(random.randint(2,3), random.randint(0, 360))

    return alpha

class Ball:
    def __init__(self, x, y, m=1, col="gray", health=100, rad=1):
        [self.x, self.y] = [x, y]


        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.shape("circle")
        self.t.speed("fastest")
        self.t.shapesize(rad, rad)

        self.rad = rad
        self.t.color(col)
        self.m = m


        self.health = health



        self.t.goto(x, y)
        self.t.showturtle()



        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.penup()
        self.label.goto(x, y)
        self.label.write(str(health), align="center", font=("Arial", 12, "bold"))


        self.label.goto(self.x, self.y)

        [self.time, self.v, self.theta] = [0, 0, 0]

        self.a = gravity

        self.im = False

    def getVel(self):
        return [self.m, self.v, self.theta]

    def setPos(self, Nx, Ny):

        self.t.hideturtle()
        self.t.goto(Nx, Ny)
        self.t.showturtle()

        self.label.clear()

        self.label.goto(Nx, Ny)

        self.label.write(str(self.health), align="center", font=("Arial", 1, "bold"))

        self.x, self.y = Nx, Ny

    def getTurt(self):
        return [self.t, self.rad]

    def getPos(self):
        return [self.x, self.y]

    def setVel(self, Nv, Ntheta):
        self.v = Nv
        self.theta = Ntheta

    def move(self):
        dt = 1/frameD
        th = math.radians(self.theta)

        vx = self.v * math.cos(th)
        vy = self.v * math.sin(th)

        vx_new = vx
        vy_new = vy + self.a * dt

        self.v = math.hypot(vx_new, vy_new)
        self.theta = math.degrees(math.atan2(vy_new, vx_new))

        self.setPos(self.x + vx_new, self.y + vy_new)

    def immunity(self, gt=False, state=False):
        if gt:
            return self.im

        else:
            self.im = state



def collision2d(sphrs, phi, e=restit):
    [m1, v1, theta1] = sphrs[0].getVel()
    [m2, v2, theta2] = sphrs[1].getVel()

    t1 = math.radians(theta1)
    t2 = math.radians(theta2)
    ph = math.radians(phi)

    u1x, u1y = v1 * math.cos(t1), v1 * math.sin(t1)
    u2x, u2y = v2 * math.cos(t2), v2 * math.sin(t2)

    u1n = u1x * math.cos(ph) + u1y * math.sin(ph)
    u1t = -u1x * math.sin(ph) + u1y * math.cos(ph)
    u2n = u2x * math.cos(ph) + u2y * math.sin(ph)
    u2t = -u2x * math.sin(ph) + u2y * math.cos(ph)

    v1n = ((m1 - e*m2) * u1n + (1 + e) * m2 * u2n) / (m1 + m2)
    v2n = ((m2 - e*m1) * u2n + (1 + e) * m1 * u1n) / (m1 + m2)

    v1t = u1t
    v2t = u2t

    v1x = v1n * math.cos(ph) - v1t * math.sin(ph)
    v1y = v1n * math.sin(ph) + v1t * math.cos(ph)
    v2x = v2n * math.cos(ph) - v2t * math.sin(ph)
    v2y = v2n * math.sin(ph) + v2t * math.cos(ph)

    v1_final = math.sqrt(v1x**2 + v1y**2)
    v2_final = math.sqrt(v2x**2 + v2y**2)
    theta1_final = math.degrees(math.atan2(v1y, v1x))
    theta2_final = math.degrees(math.atan2(v2y, v2x))

    return [v1_final, theta1_final, v2_final, theta2_final]


def collisionWall(sphr, phi, e=restit):
    [v, theta] = sphr.getVel()[1:]

    t = math.radians(theta)
    ph = math.radians(phi)

    v_n = v * math.cos(t - ph)
    v_t = v * math.sin(t - ph)

    v_n_after = -e * v_n
    v_t_after = v_t

    v_x = v_n_after * math.cos(ph) - v_t_after * math.sin(ph)
    v_y = v_n_after * math.sin(ph) + v_t_after * math.cos(ph)

    v_new = math.sqrt(v_x**2 + v_y**2)
    theta_new = math.degrees(math.atan2(v_y, v_x))

    return [v_new, theta_new]


def lineOfCentres(sphrs):
    r1, r2 = sphrs[0].getTurt()[1]*10, sphrs[1].getTurt()[1]*10
    [x1, y1] = sphrs[0].getPos()
    [x2, y2] = sphrs[1].getPos()

    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)

    if dist == 0.0:

        nx, ny = 1.0, 0.0
        phi_rad = 0.0
    else:
        nx = dx / dist
        ny = dy / dist
        phi_rad = math.atan2(dy, dx)

    tx = -ny
    ty = nx

    contact1 = (x1 + nx * r1, y1 + ny * r1)
    contact2 = (x2 - nx * r2, y2 - ny * r2)

    penetration = (r1 + r2) - dist
    is_colliding = dist <= (r1 + r2)

    return {
        "phi_rad": phi_rad,
        "phi_deg": math.degrees(phi_rad),
        "normal": (nx, ny),
        "tangent": (tx, ty),
        "contact1": contact1,
        "contact2": contact2,
        "dist": dist,
        "penetration": penetration,
        "is_colliding": is_colliding
    }



def resolvePenetration(sphrs):
    r1, r2 = sphrs[0].getTurt()[1]*10, sphrs[1].getTurt()[1]*10
    [x1, y1] = sphrs[0].getPos()
    [x2, y2] = sphrs[1].getPos()
    m1, m2 = sphrs[0].getVel()[0], sphrs[1].getVel()[0]


    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)


    if dist == 0:

        nx, ny = 1.0, 0.0
        dist = 1e-8
    else:
        nx, ny = dx / dist, dy / dist


    penetration = (r1 + r2) - dist


    if penetration <= 0:
        return x1, y1, x2, y2, 0.0


    total_mass = m1 + m2
    move1 = (penetration * (m2 / total_mass))
    move2 = (penetration * (m1 / total_mass))


    x1_new = x1 - nx * move1
    y1_new = y1 - ny * move1
    x2_new = x2 + nx * move2
    y2_new = y2 + ny * move2

    return [x1_new, y1_new, x2_new, y2_new]

baseWalls()
circ = testCirc()


def tick():
    for item in circ:
        coord, radius = item.getPos(), item.getTurt()[1]*10

        if coord[0] + radius >=250:
            item.setPos(250-radius, coord[1])

            cols = collisionWall(item, 0)
            item.setVel(cols[0], cols[1])

        if coord[0] - radius <=-250:
            item.setPos(-250+radius, coord[1])

            cols = collisionWall(item, 0)
            item.setVel(cols[0], cols[1])


        if coord[1] + radius >=250:
            item.setPos(coord[0], 250-radius)

            cols = collisionWall(item, 90)
            item.setVel(cols[0], cols[1])

        if coord[1] - radius <=-250:
            item.setPos(coord[0], -250+radius)

            cols = collisionWall(item, 90)
            item.setVel(cols[0], cols[1])


    if len(circ)>1:
        for i, item in enumerate(circ):
            for j in range(i, len(circ)):
                if not item==circ[j]:
                    loc = lineOfCentres([item, circ[j]])

                    if loc["is_colliding"]==True:
                        penet = resolvePenetration([item, circ[j]])

                        item.setPos(penet[:2][0], penet[:2][1])
                        circ[j].setPos(penet[2:][0], penet[2:][1])

                        cols = collision2d([item, circ[j]], loc["phi_deg"])

                        item.setVel(cols[:2][0], cols[:2][1])
                        circ[j].setVel(cols[2:][0], cols[2:][1])

    for item in circ:
        if item.immunity(gt=True)==False:
            item.move()

    turtle.update()
    sc.ontimer(tick, frame_delay_ms)





tick()



sc.mainloop()