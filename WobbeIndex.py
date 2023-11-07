from manim import *
import random

#Define Text, Tex and MathTex new with BLACK as default color
def myTex(*args, color=BLACK, **kwargs):
    return Tex(*args, color=color, **kwargs)
        
def myMathTex(*args, color=BLACK, **kwargs):
    return MathTex(*args, color=color, **kwargs)

def myText(*args, color=BLACK, **kwargs):
    return Text(*args, color=color, **kwargs)

narrow_position = 2.2
steigung = 0.25

class Particle(Dot):
    def __init__(self, radius=0.05, mass=1, velocity=np.ndarray([0,0,0]), horizontal_limit=5, vertical_limit=5, tracker=None, dissipation = 0, fire_limit=None, gravity=1, gas_type="air", **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.tracker = tracker
        self.dissipation = dissipation
        self.gravity = gravity
        self.gas_type = gas_type
        self.fire_limit = fire_limit
        self.horizontal_limit = horizontal_limit
        self.vertical_limit = vertical_limit

        self.add_updater(self.update_physics)

    @staticmethod 
    def update_physics(self, dt):
        pos = self.get_center() + (self.velocity  + np.random.uniform(low=-0.3,high=0.3)*RIGHT + np.random.uniform(low=-0.5,high=0.5)*UP - (9.81 / 2 * self.gravity * dt)) * dt * self.tracker.get_value()

         # Check for collisions with walls
        '''
        if (pos[0] < self.horizontal_limit):
            if (pos[1] >= self.vertical_limit):
                pos[1] = self.vertical_limit - (pos[1] - self.vertical_limit)
                self.velocity[1] = -abs(self.velocity[1] - (self.dissipation * self.velocity[1]))
            elif (pos[1] <= -self.vertical_limit):
                pos[1] = -self.vertical_limit - (pos[1] + self.vertical_limit)
                self.velocity[1] = +abs(self.velocity[1] - (self.dissipation * self.velocity[1]))
        elif (pos[0] > self.horizontal_limit):
            self.velocity[0] = 0.95*self.velocity[0]
            self.velocity[1] = 1.05*self.velocity[1]
        '''
        momentary_limit = self.vertical_limit - steigung*(pos[0]-narrow_position) # -0.25x + b

        if (pos[0] < narrow_position):
            if (pos[1] >= self.vertical_limit):
                pos[1] = self.vertical_limit - (pos[1] - self.vertical_limit)
                self.velocity[1] = -abs(self.velocity[1] - (self.dissipation * self.velocity[1]))
            elif (pos[1] <= -self.vertical_limit):
                pos[1] = -self.vertical_limit - (pos[1] + self.vertical_limit)
                self.velocity[1] = +abs(self.velocity[1] - (self.dissipation * self.velocity[1]))

        elif (pos[0] >= narrow_position and pos[0] <= self.horizontal_limit):
            if pos[1] >= momentary_limit:
                pos[1] = momentary_limit
                self.velocity[1] = -self.velocity[1]
            elif pos[1] <= -momentary_limit:
                pos[1] = -momentary_limit
                self.velocity[1] = -self.velocity[1]

        elif (pos[0] > self.horizontal_limit):
            self.velocity[0] = self.velocity[0] *0.99
            self.velocity[1] = self.velocity[1] *1.01

        self.move_to(pos)
              
    def collide_with(self, other):
        # Compute new velocities after collision assuming fully elastic collision
        v1, v2 = self.velocity, other.velocity
        m1, m2 = self.mass, other.mass
        v1_new = (m1*v1 + m2*(2*v2-v1))/(m1+m2)
        v2_new = (m2*v2 + m1*(2*v1-v2))/(m1+m2)
        self.velocity, other.velocity = v1_new, v2_new


def particles_intersect(particle1, particle2):
    """
    Checks if two circles intersect
    """
    distance = np.linalg.norm(particle1.get_center() - particle2.get_center())
    return distance < particle1.get_width() / 2 + particle2.get_width() / 2


def collisionUpdater(particles):
    for i in range(len(particles)):
        for j in range(i+1,len(particles)):
            if particles_intersect(particles[i],particles[j]):
                particles[i].collide_with(particles[j])



class WobbeSimulation1(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        background = ImageMobject("D:/Users/jonas/Desktop/Arbeit/V_AF_01/Assets/WobbeIndex/GasDuese.png") # instantiate the background image
        background.scale(2).rotate(PI/2).shift(0.65*UP + 0.9*RIGHT) # scale it to fill the scene
        # self.add(background)
        '''
        #Grid
        for x in range(-8,9):
            for y in range(-5,5):
                if not (x == 0 and y==0):
                    grid = Dot(point=[x, y, 0.], fill_opacity=0.2, color=BLACK)
                    coord = Text("(" + str(x) + "/" + str(y) + ")", font_size=15, fill_opacity=0.5, color=BLACK).next_to(grid, DR, buff=0.03)
                    self.add(grid, coord)
        origin = Dot(point=[0, 0, 0.], fill_opacity=0.5, color=BLACK, radius=0.12)
        origin_coord = Text("(0/0)", font_size=15, fill_opacity=0.8, color=BLACK).next_to(origin, DR, buff=0.03)
        self.add(origin, origin_coord)
        '''
        tracker = ValueTracker(1)
        fire_limit = ValueTracker(4)
        particles = VGroup()
        horizontal_limit = 4
        vertical_limit = 0.5
        velocity_limit = 3

        for i in range(500):
            particle = Particle(
                    stroke_color=BLUE_D, fill_color=BLUE,
                    point    = np.random.uniform(low=-(25),high=(-8))*RIGHT+np.random.uniform(low=-(vertical_limit - 0.1),high=(vertical_limit - 0.1))*UP,
                    velocity = np.random.uniform(low=0.5,high=velocity_limit)*RIGHT + np.random.uniform(low=-0.2,high=0.2)*UP,
                    tracker = tracker,
                    mass = 5,
                    gravity = 0.05,
                    gas_type="air",
                    fire_limit = fire_limit,
                    horizontal_limit = horizontal_limit,
                    vertical_limit = vertical_limit
            )
            particles += particle

        # Düse ohne Verengung
        '''
        A = [2,1,0]
        B = [-8,1,0]
        C = [-8,-1,0]
        D = [2,-1,0]
        corners = [A, B, C, D]
        '''
        # Düse mit Verengung
        A = [4, 0.2, 0]
        B = [2.2, 0.5, 0]
        C = [-8, 0.5, 0]
        D = [-8, -0.5, 0]
        E = [2.2, -0.5, 0]
        F = [4, -0.2, 0]
        corners = [A, B, C, D, E, F]

        OpenRect = Group()
        for i in range(5): # range(3)
            line = Line(
            start=corners[i],
            end=corners[i+1],
            color=BLACK,
            stroke_width=2
            )

            OpenRect.add(line)
        # self.add(OpenRect)

        narrow_position_marker = DashedLine(start=[1, 3, 0], end=[1, -3, 0], color=BLACK, stroke_width=2)
        # self.add(narrow_position_marker)        

        # Animation
        self.add(particles)
        tracker.set_value(0)
        self.wait(1)
        tracker.set_value(1)
        self.wait(10)


        # Modell für die Düse verbessern
        # Hintergrund in Blender?