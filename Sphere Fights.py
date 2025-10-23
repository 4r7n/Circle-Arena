import turtle, math, random
from statistics import mean


turtle.hideturtle()
turtle.speed("fastest")
turtle.colormode(255)

turtle.title("Arun")

turtle.tracer(0)

sc = turtle.Screen()

frameD = 120
frame_delay_ms = 1000 // frameD
xframe = 0

restit = 1
gravity = -9.80665

circ = []
objs = []
prjs = []

def ringGen(name="ring", color="black", thickness=3, step=1):
    ring = turtle.Shape("compound")

    outer, inner = [], []

    innerRadius = max(10 - thickness, 1)

    for a in range(0, 360, step):
        rad = math.radians(a)
        outer.append((10 * math.cos(rad), 10 * math.sin(rad)))

    for a in range(360, 0, -step):
        rad = math.radians(a)
        inner.append((innerRadius * math.cos(rad), innerRadius * math.sin(rad)))

    ring.addcomponent(outer + inner, outline=color, fill=color)
    sc.register_shape(name, ring)

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

def testCirc(): # "firebrick4" "dodgerblue4" "khaki4" "darkgreen"
    alpha = []
    alpha.append(Ball(200, 0, 1, "shotgun", col="firebrick4", rad=3.5, ring=4, health=100))
    alpha.append(Ball(-200, 0, 2, "sword", col="dodgerblue4", rad=3.5, ring=4, health=100))



    for item in alpha:
        item.setVel(random.randint(3, 7), random.randint(0, 360))


    return alpha

class Ball:
    def __init__(self, x, y, team, weapon, m=1, col="gray", health=100, rad=1, ring=False):
        [self.x, self.y] = [x, y]

        self.team = team

        self.weapon = weapon
        self.internal = 0

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        if not ring:
            self.t.shape("circle")
            self.t.shapesize(rad, rad)

        else:
            randN = str(random.getrandbits(128))
            ringGen(name=randN, color=col, thickness=ring)
            self.t.shape(randN)
            self.t.shapesize(rad)


        self.rad = rad
        self.col = col
        self.t.color(col)
        self.m = m


        self.health = health

        self.weapon = weapon
        self.dead = False
        self.count = 0


        self.t.goto(x, y)
        self.t.showturtle()



        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.penup()
        self.label.color(col)
        self.label.goto(x, y)
        self.label.write(str(health), align="center", font=("Arial", 1, "bold"))


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

        self.label.goto(Nx, Ny-12)

        self.label.write(str(self.health), align="center", font=("Helvetica", 16, "bold"))

        self.x, self.y = Nx, Ny

    def getTurt(self):
        return [self.t, self.rad, self.team]

    def getPos(self):
        return [self.x, self.y]

    def setVel(self, Nv, Ntheta):
        self.v = Nv
        self.theta = Ntheta

    def move(self):
        if not self.dead:
            dt = 1/frameD
            th = math.radians(self.theta)

            vx = self.v * math.cos(th)
            vy = self.v * math.sin(th)

            vx_new = vx
            vy_new = vy + self.a * dt

            self.v = math.hypot(vx_new, vy_new)
            self.theta = math.degrees(math.atan2(vy_new, vx_new))

            self.setPos(self.x + vx_new, self.y + vy_new)

            self.weapon.update()

    def immunity(self, gt=False, state=False):
        if gt:
            return self.im

        else:
            self.im = state

    def equip(self, weapon):
        self.weapon = weapon
        weapon.owner = self
        self.weapon.start()

        return self.weapon

    def kill(self):
        self.t.hideturtle()
        self.label.hideturtle()
        self.label.clear()
        self.weapon.hide()
        self.dead = True

        self.t.goto(-9999, -9999)
        self.weapon.update()

    def getWeapon(self):
        return self.weapon

    def takeDamg(self, damg):
        self.health -= damg
        if self.health <= 0:
            self.kill()

    def getDead(self):
        return self.dead

    def setCount(self, val):
        self.count = val

    def redu(self):
        if self.count>0:
            self.count -=1
            self.label.color("brown1")
        else:
            self.im = False
            self.label.color(self.col)

        self.internal += 1

    def getIntr(self):
        return self.internal



class Weapon:
    def __init__(self, damage, width, height):
        self.damage = damage
        self.team = None
        self.w = width
        self.h = height
        self.owner = None
        self.dead = False


    def getCenter(self):
        cx, cy = self.local_centre
        s = self.t.shapesize()[0]
        θ = math.radians(self.t.heading())
        dx = cx * s * math.cos(θ) - cy * s * math.sin(θ)
        dy = cx * s * math.sin(θ) + cy * s * math.cos(θ)
        return [self.t.xcor() + dx, self.t.ycor() + dy]

    def hide(self):
        self.t.hideturtle()
        self.dead = True

    def getRect(self):
        return self.getCenter() + [self.w, self.h, self.theta]

    def getStun(self):
        return self.stun

    def getTeam(self):
        return self.team

    def getDead(self):
        return self.dead

    def getOwner(self):
        return self.owner

    def update(self):
        self.theta = (self.theta + self.spin_speed * 1/frameD) % 360
        self.t.seth(self.theta)

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.t.goto(px, py)

        #self.ts.goto(self.getCenter()[0], self.getCenter()[1])

    def getDamg(self):
        return self.damage

    def getType(self):
        return self.type

    def flipSp(self):
        self.spin_speed *= -1

    def shoot(self, xframe):
        return []


HANDLE  = "#6b4226"
GUARD   = "#c2a55f"
BLADE   = "#a8e6ff"
EDGE    = "#5cc4e0"
OUTLINE = ""
pixels = [
    (-1, 0, HANDLE), (0, 0, HANDLE), (1, 0, HANDLE),
    (-1, 1, HANDLE), (0, 1, HANDLE), (1, 1, HANDLE),
    (-1, 2, HANDLE), (0, 2, HANDLE), (1, 2, HANDLE),
    (-2, 3, GUARD), (-1, 3, GUARD), (0, 3, GUARD), (1, 3, GUARD), (2, 3, GUARD),
    (-2, 4, GUARD), (-1, 4, GUARD), (0, 4, GUARD), (1, 4, GUARD), (2, 4, GUARD),
    (-1, 5, EDGE), (0, 5, BLADE), (1, 5, EDGE),
    (-1, 6, EDGE), (0, 6, BLADE), (1, 6, EDGE),
    (-1, 7, EDGE), (0, 7, BLADE), (1, 7, EDGE),
    (-1, 8, EDGE), (0, 8, BLADE), (1, 8, EDGE),
    (-1, 9, EDGE), (0, 9, BLADE), (1, 9, EDGE),
    (-1,10, EDGE), (0,10, BLADE), (1,10, EDGE),
    (-1,11, EDGE), (0,11, BLADE), (1,11, EDGE),
    (-1,12, EDGE), (0,12, BLADE), (1,12, EDGE),
    (0,13, BLADE),
    (0,14, BLADE),
    (0,15, EDGE)
]
shape = turtle.Shape("compound")
for x, y, color in pixels:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    shape.addcomponent(square, fill=color, outline=OUTLINE)

sc.register_shape("sword", shape)

class Sword(Weapon):
    def __init__(self, damage=1, width=80, height=15):
        self.spin_speed = 1000
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.1
        self.type = "sword"
        self.stun = 15

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        self.local_centre = (7.5, 0)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.t.goto(px, py)

        self.t.shape("sword")
        self.t.shapesize(5, 5)

        self.t.showturtle()

        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")

    def hit(self):
        damg = int(str(self.damage))
        self.damage += 1

        return [damg, self.knockback]

    def stats(self):
        return "🗡️ Sword "+str(self.team)+"\nDamage: "+str(self.damage)+"\n\n"



WOOD_DARK = "#5a3a1a"
WOOD_LIGHT = "#c68c53"
STRING = "#e6e6e6"
OUTLINE = ""
orig_pixels = [
    (-2, -6, STRING), (-2, -5, STRING), (-2, -4, STRING),
    (-2, -3, STRING), (-2, -2, STRING), (-2, -1, STRING),
    (-2,  0, STRING), (-2,  1, STRING), (-2,  2, STRING),
    (-2,  3, STRING), (-2,  4, STRING), (-2,  5, STRING), (-2,  6, STRING),

    (-1, -6, WOOD_DARK), (0, -5, WOOD_LIGHT), (1, -4, WOOD_LIGHT),
    (1, -3, WOOD_LIGHT), (2, -2, WOOD_LIGHT), (2, -1, WOOD_LIGHT),
    (2,  0, WOOD_LIGHT), (2,  1, WOOD_LIGHT), (2,  2, WOOD_LIGHT),
    (1,  3, WOOD_LIGHT), (1,  4, WOOD_LIGHT), (0,  5, WOOD_LIGHT),
    (-1,  6, WOOD_DARK),

    (-1, 0, WOOD_DARK), (0, 0, WOOD_DARK), (1, 0, WOOD_DARK),
]
rotated = [(-y, x, col) for (x, y, col) in orig_pixels]
xs = [x for x, y, c in rotated]
ys = [y for x, y, c in rotated]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x + 1
height = max_y - min_y + 1
shift_y = -min_y
pixels_shifted = [(x, y + shift_y, col) for (x, y, col) in rotated]
screen = turtle.Screen()
shape = turtle.Shape("compound")
for x, y, color in pixels_shifted:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    shape.addcomponent(square, fill=color, outline=OUTLINE)

sc.register_shape("bow", shape)


class Bow(Weapon):
    def __init__(self, damage = 0, arrows = 1, width = 25, height=65):
        self.arrows = arrows

        self.spin_speed = 300
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.05
        self.type = "bow"

        self.accumulator = 0

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        self.local_centre = (7.5, 0)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.local_centre = (3.0, 0)

        self.t.shape("bow")
        self.t.shapesize(5, 5)

        self.t.showturtle()

    def hit(self):
        damg = int(str(self.damage))

        return [damg, self.knockback]

    def prhit(self):
        self.arrows += 1

    def shoot(self, frame):
        def arrow_shooter(arrows_owned, frame, accumulator, reload_frames=50, shoot_frames=30):
            arrows_to_shoot = 0
            cycle_frame = frame % reload_frames

            if cycle_frame < shoot_frames:
                arrows_per_frame = arrows_owned / shoot_frames
                accumulator += arrows_per_frame
                arrows_to_shoot = int(accumulator)
                accumulator -= arrows_to_shoot
            frame = (frame + 1) % reload_frames

            return [arrows_to_shoot, accumulator]

        [val, self.accumulator] = arrow_shooter(self.arrows, frame, self.accumulator)

        retr = []
        for i in range(val):
            retr.append(Arrow(self.getCenter()[0]+random.randint(-5,5), self.getCenter()[1]+random.randint(-5,5), self.theta+90, self))

        return retr

    def stats(self):
        return "🏹 Bow "+str(self.team)+"\nArrows: "+str(self.arrows)+"\n\n"


METAL = "#777777"
DARK = "#4b4b4b"
WOOD = "#6b4226"
HIGHLIGHT = "#cfcfcf"
OUTLINE = ""

orig_pixels = [
    (-4,  0, METAL), (-3,  0, METAL), (-2,  0, METAL), (-1,  0, METAL),
    (-4,  1, METAL), (-3,  1, DARK),  (-2,  1, DARK),  (-1,  1, DARK),
    (0,  0, METAL), (0,  1, METAL), (1, 0, METAL), (1, 1, METAL),
    (2, 0, METAL), (2, 1, METAL),
    (0, 2, DARK), (1, 2, DARK), (2, 2, DARK),
    (-1, 2, DARK), (-2, 2, DARK),
    (2, -1, WOOD), (2, -2, WOOD), (3, -1, WOOD), (3, -2, WOOD),
    (1, -1, HIGHLIGHT),
    (4, -2, DARK), (4, -1, DARK)
]


rotated = [(y, -x, col) for (x, y, col) in orig_pixels]
handle_pixels = [(x, y) for (x, y, col) in rotated if col == WOOD]
if not handle_pixels:
    raise RuntimeError("No handle pixels found in rotated data; check color constant.")
handle_centers_x = [x + 0.5 for x, y in handle_pixels]
handle_centers_y = [y + 0.5 for x, y in handle_pixels]
center_handle_x = mean(handle_centers_x)
center_handle_y = mean(handle_centers_y)
pixels_shifted = [ (x - center_handle_x, y - center_handle_y, col) for (x, y, col) in rotated ]
xs = [x for x, y, c in pixels_shifted]
ys = [y for x, y, c in pixels_shifted]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x + 1
height = max_y - min_y + 1
shape = turtle.Shape("compound")
for x, y, color in pixels_shifted:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    shape.addcomponent(square, fill=color, outline=OUTLINE)
sc.register_shape("revolver", shape)


class Revolver(Weapon):
    def __init__(self, damage = 0, width = 25, height = 45):
        self.probs = [71,20,7,2]

        self.spin_speed = 644
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.05
        self.type = "revolver"

        self.accumulator = 0

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.local_centre = (2.4, -2)

        self.t.shape("revolver")
        self.t.shapesize(5, 5)

        self.t.showturtle()

        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")

    def stats(self):
        return ""

    def shoot(self, frame):
        def shooter(frame, accumulator, reload_frames=74, shoot_frames=34, bullets=4):
            bullets_to_shoot = 0
            cycle_frame = frame % reload_frames

            if cycle_frame < shoot_frames:
                bullets_per_frame = bullets / shoot_frames
                accumulator += bullets_per_frame
                bullets_to_shoot = int(accumulator)
                accumulator -= bullets_to_shoot
            frame = (frame + 1) % reload_frames

            return [bullets_to_shoot, accumulator]

        [val, self.accumulator] = shooter(frame, self.accumulator)

        def chooseW(probabilities, outcomes=None):

            total = sum(probabilities)
            probs = [p / total for p in probabilities]

            r = random.random()
            cumulative = 0

            for i, p in enumerate(probs):
                cumulative += p
                if r < cumulative:
                    return outcomes[i] if outcomes else i

            return outcomes[-1] if outcomes else len(probabilities) - 1

        retr = []
        for i in range(val):
            bullet = chooseW(self.probs, ["b", "s", "g", "p"])
            if bullet=="b":
                retr.append(Bullet(self.getCenter()[0], self.getCenter()[1], self.theta+90, self, 1, "chocolate4"))
            elif bullet=="s":
                retr.append(Bullet(self.getCenter()[0], self.getCenter()[1], self.theta+90, self, 4, "azure4"))
            elif bullet=="g":
                retr.append(Bullet(self.getCenter()[0], self.getCenter()[1], self.theta+90, self, 14, "darkgoldenrod3"))
            else:
                retr.append(Bullet(self.getCenter()[0], self.getCenter()[1], self.theta+90, self, 44, "darkslategray2"))

        return retr

    def prhit(self, rate=0.05):
        new_probs = self.probs[:]
        n = len(self.probs)

        for i in range(n - 1):
            shift = new_probs[i] * rate
            new_probs[i] -= shift
            new_probs[i + 1] += shift


        total = sum(new_probs)
        new_probs = [p * 100 / total for p in new_probs]

        self.probs = new_probs



BLADE_LIGHT = "#cfe9f9"
BLADE_DARK  = "#7da0b4"
HANDLE_DARK = "#3a2e1f"
HANDLE_LIGHT = "#5a4630"
GUARD_METAL = "#9c8f7a"
OUTLINE = ""
pixels = [
    (0, 7, BLADE_LIGHT),
    (0, 6, BLADE_LIGHT),
    (0, 5, BLADE_LIGHT),
    (-1, 4, BLADE_DARK), (0, 4, BLADE_LIGHT),
    (-1, 3, BLADE_DARK), (0, 3, BLADE_LIGHT),
    (-1, 2, BLADE_DARK), (0, 2, BLADE_LIGHT),
    (-1, 1, BLADE_DARK), (0, 1, BLADE_LIGHT),
    (-2, 0, GUARD_METAL), (-1, 0, GUARD_METAL),
    (0, 0, GUARD_METAL), (1, 0, GUARD_METAL), (2, 0, GUARD_METAL),
    (-1, -1, HANDLE_DARK), (0, -1, HANDLE_LIGHT),
    (-1, -2, HANDLE_DARK), (0, -2, HANDLE_LIGHT),
    (-1, -3, HANDLE_DARK), (0, -3, HANDLE_LIGHT),
    (-1, -4, GUARD_METAL), (0, -4, GUARD_METAL)
]

handle_px = [(x, y) for x, y, c in pixels if HANDLE_LIGHT in c or HANDLE_DARK in c]
handle_center_x = mean([x + 0.5 for x, y in handle_px])
handle_center_y = mean([y + 0.5 for x, y in handle_px])
shifted = [(x - handle_center_x, y - handle_center_y, c) for x, y, c in pixels]
xs, ys = [x for x, _, _ in shifted], [y for _, y, _ in shifted]
width = max(xs) - min(xs) + 1
height = max(ys) - min(ys) + 1
dagger_shape = turtle.Shape("compound")
for x, y, color in shifted:
    sq = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    dagger_shape.addcomponent(sq, fill=color, outline=OUTLINE)
sc.register_shape("dagger", dagger_shape)



class Dagger(Weapon):
    def __init__(self, damage=1, width=25, height=60):
        self.spin_speed = 800
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.01
        self.type = "dagger"
        self.stun = 0

        self.mlt = 1

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        self.local_centre = (3.4, 0)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.t.goto(px, py)

        self.t.shape("dagger")
        self.t.shapesize(5, 5)

        self.t.showturtle()


        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")


    def hit(self):
        damg = int(str(self.damage))
        self.mlt *= 1.25

        return [damg, self.knockback]

    def stats(self):
        return "🗡️ Dagger "+str(self.team)+"\nSpin: "+str(self.spin_speed)+"\n\n"

    def update(self):
        self.theta = (self.theta + self.mlt * self.spin_speed * 1/frameD) % 360
        self.t.seth(self.theta)

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.t.goto(px, py)

        #self.ts.goto(self.getCenter()[0], self.getCenter()[1])

BLADE_LIGHT = "#ff4d4d"
BLADE_DARK  = "#b30000"
GUARD_GOLD  = "#d4af37"
HANDLE_DARK = "#3a1f0f"
HANDLE_LIGHT = "#5c2e15"
OUTLINE = ""

pixels = [
    (0, 12, BLADE_LIGHT),
    (0, 11, BLADE_LIGHT),
    (-1, 10, BLADE_DARK), (0, 10, BLADE_LIGHT), (1, 10, BLADE_DARK),
    (-1, 9, BLADE_DARK), (0, 9, BLADE_LIGHT), (1, 9, BLADE_DARK),
    (-1, 8, BLADE_DARK), (0, 8, BLADE_LIGHT), (1, 8, BLADE_DARK),
    (-1, 7, BLADE_DARK), (0, 7, BLADE_LIGHT), (1, 7, BLADE_DARK),
    (-1, 6, BLADE_DARK), (0, 6, BLADE_LIGHT), (1, 6, BLADE_DARK),
    (-1, 5, BLADE_DARK), (0, 5, BLADE_LIGHT), (1, 5, BLADE_DARK),
    (-1, 4, BLADE_DARK), (0, 4, BLADE_LIGHT), (1, 4, BLADE_DARK),
    (-3, 3, GUARD_GOLD), (-2, 3, GUARD_GOLD),
    (-1, 3, GUARD_GOLD), (0, 3, GUARD_GOLD),
    (1, 3, GUARD_GOLD), (2, 3, GUARD_GOLD), (3, 3, GUARD_GOLD),
    (-1, 2, HANDLE_DARK), (0, 2, HANDLE_LIGHT),
    (-1, 1, HANDLE_DARK), (0, 1, HANDLE_LIGHT),
    (-1, 0, HANDLE_DARK), (0, 0, HANDLE_LIGHT),
]

xs = [x for x, y, c in pixels]
ys = [y for x, y, c in pixels]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x + 1
height = max_y - min_y + 1
bottom_y = min_y
center_x = (min_x + max_x) / 2
shifted = [(x - center_x, y - bottom_y, c) for x, y, c in pixels]
ruby_sword = turtle.Shape("compound")
for x, y, color in shifted:
    sq = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    ruby_sword.addcomponent(sq, fill=color, outline=OUTLINE)
sc.register_shape("perfect", ruby_sword)



class Perfect(Weapon):
    def __init__(self, damage=1, width=35, height=65):
        self.spin_speed = 777
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.07
        self.type = "perfect"
        self.stun = 11

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        self.local_centre = (3.5, 0)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.t.goto(px, py)

        self.t.shape("perfect")
        self.t.shapesize(5, 5)

        self.t.showturtle()

        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")

    def hit(self):
        damg = int(str(self.damage))
        self.damage += 4

        return [damg, self.knockback]

    def reset(self):
        self.damage = 1

    def stats(self):
        return "🗡️ Perfect "+str(self.team)+"\nDamage: "+str(self.damage)+"\n\n"

METAL = "#777777"
METAL_DARK = "#4b4b4b"
HANDLE = "#6b4226"
STOCK = "#8a5a3c"
HIGHLIGHT = "#cfcfcf"
OUTLINE = ""


pixels = [

    (-6, 0, STOCK), (-6, 1, STOCK), (-5, 0, STOCK), (-5, 1, STOCK),


    (-2, -1, HANDLE), (-1, -1, HANDLE), (-2, 0, HANDLE), (-1, 0, HANDLE),


    (0, -1, HIGHLIGHT),


    (0, 0, METAL), (1, 0, METAL), (2, 0, METAL), (3, 0, STOCK), (4, 0, STOCK),
    (0, 1, METAL), (1, 1, METAL), (2, 1, METAL), (3, 1, METAL), (4, 1, METAL),


    (4, 2, METAL), (5, 2, METAL), (6, 2, METAL), (7, 2, METAL),
    (8, 2, METAL), (9, 2, METAL), (10, 2, METAL), (11, 2, METAL),

    (5, 1, METAL), (6, 1, METAL), (7, 1, METAL), (8, 1, METAL),
    (9, 1, METAL), (10, 1, METAL), (11, 1, METAL),


    (12, 1, METAL),


    (8, 3, METAL_DARK),
]

xs = [x for x, y, c in pixels]
ys = [y for x, y, c in pixels]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x + 1
height = max_y - min_y + 1


handle_pixels = [(x, y) for (x, y, c) in pixels if c == HANDLE]
if not handle_pixels:

    center_x = (min_x + max_x) / 2.0
    center_y = (min_y + max_y) / 2.0
else:
    hx = [x + 0.5 for x, y in handle_pixels]
    hy = [y + 0.5 for x, y in handle_pixels]
    center_x = mean(hx)
    center_y = mean(hy)

pixels_shifted = [(x - center_x, y - center_y, col) for (x, y, col) in pixels]

shape = turtle.Shape("compound")
for x, y, color in pixels_shifted:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    shape.addcomponent(square, fill=color, outline=OUTLINE)

sc.register_shape("shotgun", shape)

class Shotgun(Weapon):
    def __init__(self, damage = 0, width = 25, height = 85):

        self.spin_speed = 810
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.09
        self.type = "shotgun"
        self.reload = 64
        self.framel = []

    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.local_centre = (2, -5.2)

        self.t.shape("shotgun")
        self.t.shapesize(5, 5)

        self.t.showturtle()

        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")

    def stats(self):
        return ""

    def getCtr(self):
        cx, cy = 2, -9
        s = self.t.shapesize()[0]
        θ = math.radians(self.t.heading())
        dx = cx * s * math.cos(θ) - cy * s * math.sin(θ)
        dy = cx * s * math.sin(θ) + cy * s * math.cos(θ)
        return [self.t.xcor() + dx, self.t.ycor() + dy]

    def shoot(self, frame):
        retr = []
        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        if frame%(math.ceil(self.reload)+1)==0:
            retr.append(Pellet(self.getCtr()[0], self.getCtr()[1], self.theta, self))
            retr.append(Pellet(self.getCtr()[0], self.getCtr()[1], self.theta+27, self))
            retr.append(Pellet(self.getCtr()[0], self.getCtr()[1], self.theta-27, self))
            retr.append(Pellet(self.getCtr()[0], self.getCtr()[1], self.theta-13, self))
            retr.append(Pellet(self.getCtr()[0], self.getCtr()[1], self.theta+13, self))

        return retr

    def prhit(self, xframe):
        if not xframe in self.framel:
            self.reload *= 0.95
            self.framel.append(xframe)

GOLD_LIGHT = "#ffd84d"
GOLD_DARK  = "#b38f00"
TRIGGER    = "#444444"
HANDLE     = "#2b1b0f"
GRIP_LIGHT = "#3c2415"
OUTLINE = ""

pixels = [
    (0, 3, GOLD_LIGHT), (1, 3, GOLD_LIGHT), (2, 3, GOLD_LIGHT),
    (3, 3, GOLD_LIGHT), (4, 3, GOLD_LIGHT), (5, 3, GOLD_DARK),
    (6, 3, GOLD_DARK), (7, 3, GOLD_DARK),
    (0, 2, GOLD_LIGHT), (1, 2, GOLD_LIGHT), (2, 2, GOLD_LIGHT),
    (3, 2, GOLD_LIGHT), (4, 2, GOLD_DARK), (5, 2, GOLD_DARK),
    (6, 2, GOLD_DARK),
    (1, 1, TRIGGER), (2, 1, TRIGGER), (3, 1, GOLD_DARK), (4, 1, GOLD_DARK),
    (0, 0, HANDLE), (-1, 0, HANDLE),
    (-1, -1, GRIP_LIGHT), (0, -1, GRIP_LIGHT),
    (-1, -2, GRIP_LIGHT),
]
xs = [x for x, y, _ in pixels]
ys = [y for x, y, _ in pixels]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
width = max_x - min_x + 1
height = max_y - min_y + 1
handle_pixels = [(x, y) for (x, y, c) in pixels if c in (HANDLE, GRIP_LIGHT)]
hx = [x + 0.5 for x, y in handle_pixels]
hy = [y + 0.5 for x, y in handle_pixels]
center_x = mean(hx)
center_y = mean(hy)
shifted = [(x - center_x, y - center_y, c) for x, y, c in pixels]
gold_deagle = turtle.Shape("compound")
for x, y, color in shifted:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    gold_deagle.addcomponent(square, fill=color, outline=OUTLINE)
sc.register_shape("igneous", gold_deagle)


class Igneous(Weapon):
    def __init__(self, damage = 0, width = 45, height = 30):

        self.spin_speed = 200
        self.x, self.y, self.theta = 0, 0, 0

        self.damage = damage
        self.w = width
        self.h = height
        self.dead = False

        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.t.penup()
        self.t.speed("fastest")

        self.knockback = 1.12
        self.type = "igneous"

        self.dam = 0
        self.ext = 0


    def start(self):
        self.team = self.owner.getTurt()[2]

        cx, cy = self.owner.getPos()[0], self.owner.getPos()[1]
        r = self.owner.getTurt()[1]*10
        tx = math.radians(self.theta)

        px = cx + r * math.cos(tx)
        py = cy + r * math.sin(tx)

        self.local_centre = (3, -4.5)

        self.t.shape("igneous")
        self.t.shapesize(5, 5)

        self.t.showturtle()

        #self.ts = turtle.Turtle()
        #self.ts.shape("circle")

    def stats(self):
        return ""

    def shoot(self, frame):
        retr = []
        tx = math.radians(self.theta)

        ax = 1000 * math.cos(math.radians(self.theta-90)) * 1
        ay = 1000 * math.sin(math.radians(self.theta-90)) * 1

        if frame%270==0:
            retr.append(Beam(self.getCenter()[0] +ax , self.getCenter()[1] +ay, self.theta, self, 20+self.ext))
        elif frame%90==0:
            retr.append(Hcal(self.getCenter()[0] + ax, self.getCenter()[1] +ay, self.theta, self ,4+self.dam))

        return retr

    def prhit(self):
        self.dam += 4
        self.ext += 20

class Projectile:
    def __init__(self, damage, width, height):
        self.damage = damage
        self.team = team

        self.w = width
        self.h = height
        self.dead = False

    def getCenter(self):
        cx, cy = self.local_centre
        s = self.t.shapesize()[0]
        θ = math.radians(self.t.heading())
        dx = cx * s * math.cos(θ) - cy * s * math.sin(θ)
        dy = cx * s * math.sin(θ) + cy * s * math.cos(θ)
        return [self.t.xcor() + dx, self.t.ycor() + dy]

    def getRect(self):
        return self.getCenter() + [self.w, self.h, self.theta]

    def getTeam(self):
        return self.team

    def getDamg(self):
        return self.damage

    def hide(self):
        self.t.hideturtle()
        self.t.clear()
        self.dead = True

    def setPos(self, nx, ny):
        self.x, self.y = nx, ny
        self.t.goto(nx, ny)

    def getOwner(self):
        return self.owner

    def getVel(self):
        return [self.v, self.theta]

    def getStun(self):
        return self.stun

    def getType(self):
        return self.type


SHAFT = "#8B4513"
HEAD = "#555555"
TAIL = "#FF0000"
OUTLINE = ""
pixels = [
    (0, 0, SHAFT), (1, 0, SHAFT), (2, 0, SHAFT), (3, 0, SHAFT),
    (4, -1, HEAD), (4, 0, HEAD), (4, 1, HEAD),
    (5, 0, HEAD),
    (-1, -1, TAIL), (-1, 1, TAIL),
    (-2, -1, TAIL), (-2, 1, TAIL)
]
xs = [x for x, y, c in pixels]
ys = [y for x, y, c in pixels]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

width = max_x - min_x + 1
height = max_y - min_y + 1
center_x = (min_x + max_x + 1) / 2
center_y = (min_y + max_y + 1) / 2
pixels_shifted = [(x - center_x, y - center_y, c) for x, y, c in pixels]
arrow_shape = turtle.Shape("compound")
for x, y, color in pixels_shifted:
    square = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    arrow_shape.addcomponent(square, fill=color, outline=OUTLINE)

sc.register_shape("arrow", arrow_shape)



class Arrow(Projectile):
    def __init__(self, x, y, theta, owner, damage = 1, width = 32, height = 12):
        self.v = 2000
        self.w = width
        self.h = height
        self.local_centre = (1.5, 0)
        self.damage = 1
        self.owner = owner
        self.type = "arrow"

        self.x, self.y, self.theta = x, y, theta

        self.team = self.owner.getTeam()

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shape("arrow")
        self.t.shapesize(4,4)
        self.t.seth(self.theta)

        self.t.goto(self.x, self.y)
        self.t.showturtle()
        self.stun = 1

    def move(self):
        dt = 1/frameD
        dx = self.v * math.cos(math.radians(self.theta-90)) * dt
        dy = self.v * math.sin(math.radians(self.theta-90)) * dt
        self.setPos(self.x + dx, self.y + dy)

class Bullet(Projectile):
    def __init__(self, x, y, theta, owner, damage, colour, width = 8, height = 18):
        self.v = 3000
        self.w = width
        self.h = height
        self.local_centre = (0, 0)
        self.damage = damage
        self.owner = owner
        self.col = colour
        self.type = "bullet"

        self.x, self.y, self.theta = x, y, theta

        self.team = self.owner.getTeam()

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shape("square")
        self.t.shapesize(1.8, 0.8)
        self.t.color(self.col)
        self.t.seth(self.theta)
        self.t.pensize(2)

        self.t.goto(self.x, self.y)
        self.t.showturtle()
        self.stun = 2
        self.t.pendown()

    def move(self):
        dt = 1/frameD
        dx = self.v * math.cos(math.radians(self.theta-90)) * dt
        dy = self.v * math.sin(math.radians(self.theta-90)) * dt
        self.setPos(self.x + dx, self.y + dy)


class Pellet(Projectile):
    def __init__(self, x, y, theta, owner, damage=2, width = 8, height = 18):
        self.v = 2700
        self.w = width
        self.h = height
        self.local_centre = (0, 0)
        self.damage = damage
        self.owner = owner
        self.type = "pellet"

        self.x, self.y, self.theta = x, y, theta

        self.team = self.owner.getTeam()

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shape("circle")
        self.t.shapesize(0.7, 0.7)
        self.t.color("orange")
        self.t.seth(self.theta)
        self.t.pensize(10)

        self.t.goto(self.x, self.y)
        self.t.showturtle()
        self.stun = 0
        self.t.pendown()

        self.frames = 0

    def move(self):
        dt = 1/frameD
        dx = self.v * math.cos(math.radians(self.theta-90)) * dt
        dy = self.v * math.sin(math.radians(self.theta-90)) * dt
        self.setPos(self.x + dx, self.y + dy)
        self.frames+=1

    def lifetime(self):
        return self.frames>5

class Hcal(Projectile):
    def __init__(self, x, y, theta, owner, damage, width = 1, height = 2000):
        self.v = 0
        self.w = width
        self.h = height
        self.local_centre = (0, 0)
        self.damage = damage
        self.owner = owner
        self.type = "hcal"

        ax = 1000 * math.cos(math.radians(theta-90)) * 1
        ay = 1000 * math.sin(math.radians(theta-90)) * 1

        self.x, self.y, self.theta = x, y, theta

        self.team = self.owner.getTeam()

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shape("square")
        self.t.shapesize(100, 0.1)
        self.t.color("orangered")
        self.t.seth(self.theta)

        self.t.goto(x, y)
        self.t.showturtle()
        self.stun = 10

        self.frames = 0

    def move(self):
        dt = 1/frameD
        dx = self.v * math.cos(math.radians(self.theta-90)) * dt
        dy = self.v * math.sin(math.radians(self.theta-90)) * dt
        self.setPos(self.x + dx, self.y + dy)
        self.frames+=1

    def lifetime(self):
        return self.frames>3


class Beam(Projectile):
    def __init__(self, x, y, theta, owner, lf, damage=1, width = 5, height = 2000):
        self.v = 0
        self.w = width
        self.h = height
        self.local_centre = (0, 0)
        self.damage = damage
        self.owner = owner
        self.type = "beam"
        self.lf = lf

        ax = 1000 * math.cos(math.radians(theta-90)) * 1
        ay = 1000 * math.sin(math.radians(theta-90)) * 1

        self.x, self.y, self.theta = x, y, theta

        self.team = self.owner.getTeam()

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.shape("square")
        self.t.shapesize(100, 0.5)
        self.t.color("greenyellow")
        self.t.seth(self.theta)

        self.t.goto(x, y)
        self.t.showturtle()
        self.stun = 1

        self.frames = 0

    def move(self):
        dt = 1/frameD
        dx = self.v * math.cos(math.radians(self.theta-90)) * dt
        dy = self.v * math.sin(math.radians(self.theta-90)) * dt
        self.setPos(self.x + dx, self.y + dy)
        self.frames+=1

    def lifetime(self):
        return self.frames>self.lf




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


def circHit(rct, sphr):

    [cx, cy] = sphr.getPos()
    cr = sphr.getTurt()[1]*10

    [rx, ry, w, h, theta_deg] = rct.getRect()

    theta = math.radians(-theta_deg)

    dx = cx - rx
    dy = cy - ry


    local_x = dx * math.cos(theta) - dy * math.sin(theta)
    local_y = dx * math.sin(theta) + dy * math.cos(theta)

    half_w, half_h = w / 2, h / 2
    nearest_x = max(-half_w, min(local_x, half_w))
    nearest_y = max(-half_h, min(local_y, half_h))

    dist_x = local_x - nearest_x
    dist_y = local_y - nearest_y
    dist_sq = dist_x**2 + dist_y**2

    return dist_sq <= cr**2

def rectHit(rcts):

    [x1, y1, w1, h1, theta1_deg] = rcts[0].getRect()
    [x2, y2, w2, h2, theta2_deg] = rcts[1].getRect()

    def get_corners(x, y, w, h, theta_deg):
        theta = math.radians(theta_deg)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        hw, hh = w / 2, h / 2
        return [
            (x + cos_t * hw - sin_t * hh, y + sin_t * hw + cos_t * hh),
            (x - cos_t * hw - sin_t * hh, y - sin_t * hw + cos_t * hh),
            (x - cos_t * hw + sin_t * hh, y - sin_t * hw - cos_t * hh),
            (x + cos_t * hw + sin_t * hh, y + sin_t * hw - cos_t * hh),
        ]

    def project_polygon(axis, corners):
        dots = [cx * axis[0] + cy * axis[1] for cx, cy in corners]
        return min(dots), max(dots)

    def overlap_on_axis(axis, c1, c2):
        min1, max1 = project_polygon(axis, c1)
        min2, max2 = project_polygon(axis, c2)
        return not (max1 < min2 or max2 < min1)


    c1 = get_corners(x1, y1, w1, h1, theta1_deg)
    c2 = get_corners(x2, y2, w2, h2, theta2_deg)


    axes = []
    for corners in [c1, c2]:
        for i in range(4):
            xA, yA = corners[i]
            xB, yB = corners[(i+1)%4]
            edge = (xB - xA, yB - yA)
            normal = (-edge[1], edge[0])
            length = math.hypot(*normal)
            axes.append((normal[0]/length, normal[1]/length))


    for axis in axes:
        if not overlap_on_axis(axis, c1, c2):
            return False
    return True


baseWalls()
circ = testCirc()
for item in circ:
    if item.getWeapon()=="sword":
        objs.append(item.equip(Sword()))
    elif item.getWeapon()=="bow":
        objs.append(item.equip(Bow()))
    elif item.getWeapon()=="revolver":
        objs.append(item.equip(Revolver()))
    elif item.getWeapon()=="dagger":
        objs.append(item.equip(Dagger()))
    elif item.getWeapon()=="perfect":
        objs.append(item.equip(Perfect()))
    elif item.getWeapon()=="shotgun":
        objs.append(item.equip(Shotgun()))
    elif item.getWeapon()=="igneous":
        objs.append(item.equip(Igneous()))

#Score = turtle.Turtle()
#Score.penup()
#Score.hideturtle()
#Score.color("lightcyan4")



def tick():
    global xframe, prjs, objs, circ
    xframe+=1

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


    for circle in circ:
        for obj in objs:
            if circHit(obj, circle)==True:
                if not(circle.getTurt()[2]==obj.getTeam()) and circle.immunity(gt=True)==False and obj.getOwner().immunity(gt=True)==False and obj.getDamg()>0:
                    attr = obj.hit()

                    circle.takeDamg(attr[0])

                    [mm, mv, mt] = circle.getVel()
                    circle.setVel(mv*attr[1], mt)

                    circle.immunity(state=True)
                    circle.setCount(obj.getStun())

                    if circle.getWeapon().getType()=="perfect":
                        circle.getWeapon().reset()

        for prj in prjs:
            if circHit(prj, circle)==True:
                if not(circle.getTurt()[2]==prj.getTeam()) and circle.immunity(gt=True)==False and prj.getOwner().getOwner().immunity(gt=True)==False:

                    if prj.getType()=="pellet":
                        prj.getOwner().prhit(xframe)

                    elif prj.getType()=="beam":
                        pass
                    else:
                        prj.getOwner().prhit()
                    circle.takeDamg(prj.getDamg())

                    circle.immunity(state=True)
                    circle.setCount(prj.getStun())

                    if circle.getWeapon().getType()=="perfect":
                        circle.getWeapon().reset()


                    if not prj.getType()=="pellet" and not prj.getType()=="hcal" and not prj.getType()=="beam":
                        prj.hide()
                        prjs.remove(prj)


    for obj in objs:
        for item in objs:
            if not item==obj:
                if rectHit([obj, item])==True:
                    if not(item.getTeam()==obj.getTeam()) and obj.getOwner().immunity(gt=True)==False and item.getOwner().immunity(gt=True)==False:


                        [ax, ay] = obj.getCenter()
                        [bx, by] = item.getCenter()

                        dx = bx - ax
                        dy = by - ay
                        angle = math.degrees(math.atan2(dy, dx))

                        obj.getOwner().setVel(obj.getOwner().getVel()[1]*1, angle + 180)
                        item.getOwner().setVel(item.getOwner().getVel()[1]*1, angle)
                        obj.flipSp()

        for prj in prjs:
            if rectHit([obj, prj])==True:
                if not(prj.getTeam()==obj.getTeam()):
                    if not prj.getType()=="hcal" and not prj.getType()=="beam":
                        prj.hide()
                        prjs.remove(prj)


    st = ""
    for item in circ:
        if item.immunity(gt=True)==False:
            item.move()
        item.redu()
        st+=item.getWeapon().stats()

    for item in circ:
        if item.getDead()==True:
            circ.remove(item)

    for item in objs:
        if item.getDead()==True:
            objs.remove(item)


        prjs += item.shoot(xframe)


    for item in prjs:
        item.move()
        [ax, ay] = item.getCenter()
        if (ax>250 or ax<-250 or ay>250 or ay<-250):
            if not item.getType()=="hcal" and not item.getType()=="beam":
                item.hide()
                prjs.remove(item)

        if item.getType()=="pellet" or item.getType()=="hcal" or item.getType()=="beam":
            if item.lifetime()==True:
                item.hide()
                try:
                    prjs.remove(item)
                except:
                    pass

    turtle.update()

    sc.ontimer(tick, frame_delay_ms)





tick()


sc.mainloop()
