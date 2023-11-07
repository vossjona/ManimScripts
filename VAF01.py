from manim import *
import random

#Define Text, Tex and MathTex new with BLACK as default color
def myTex(*args, color=BLACK, **kwargs):
    return Tex(*args, color=color, **kwargs)
        
def myMathTex(*args, color=BLACK, **kwargs):
    return MathTex(*args, color=color, **kwargs)

def myText(*args, color=BLACK, **kwargs):
    return Text(*args, color=color, **kwargs)


class Particle(Dot):
    def __init__(self, radius=0.1, mass=1, velocity=np.ndarray([0,0,0]), horizontal_limit=5, vertical_limit=5, tracker=None, dissipation = 0, fire_limit=None, gravity=1, gas_type="air", **kwargs):
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
        pos = self.get_center() + (self.velocity  + np.random.uniform(low=-1,high=1)*RIGHT + np.random.uniform(low=-1,high=1)*UP - (9.81 / 2 * self.gravity * dt)) * dt * self.tracker.get_value()

         # Check for collisions with walls
        if (pos[0] >= self.horizontal_limit):
            pos[0] = self.horizontal_limit - (pos[0] - self.horizontal_limit)
            self.velocity[0] = -abs(self.velocity[0] - (self.dissipation * self.velocity[0]))
        elif (pos[0] <= -self.horizontal_limit):
            pos[0] = -self.horizontal_limit - (pos[0] + self.horizontal_limit)
            self.velocity[0] = +abs(self.velocity[0] - (self.dissipation * self.velocity[0]))
        if (pos[1] >= self.vertical_limit):
            pos[1] = self.vertical_limit - (pos[1] - self.vertical_limit)
            self.velocity[1] = -abs(self.velocity[1] - (self.dissipation * self.velocity[1]))
        elif (pos[1] <= -self.vertical_limit):
            pos[1] = -self.vertical_limit - (pos[1] + self.vertical_limit)
            self.velocity[1] = +abs(self.velocity[1] - (self.dissipation * self.velocity[1]))

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
                

def transformationUpdater(particles):
    for particle in particles:
        if particle.get_y() > particle.fire_limit.get_value() and particle.gas_type == "gas":
            if random.random() > 0.98:
                particle.set(fill_color=RED)
                particle.set(stroke_color = RED_D)
                particle.set(mass = 1)
                particle.set(gravity = -1)
                particle.scale(0.5)
                particle.set(gas_type="air")
                particle.set(velocity = particle.velocity * np.random.uniform(low=1,high=1.02))


class ParticleSimulation(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        tracker = ValueTracker(1)
        fire_limit = ValueTracker(4)
        particles = VGroup()
        horizontal_limit = 6.5
        vertical_limit = 3.5
        velocity_limit = 0.2

        particles.add_updater(collisionUpdater) 
        particles.add_updater(transformationUpdater)


        for i in range(70):
            particle = Particle(
                    stroke_color=BLUE_D, fill_color=BLUE,
                    point    = np.random.uniform(low=-(horizontal_limit - 0.2),high=(horizontal_limit - 0.2))*RIGHT+np.random.uniform(low=-(vertical_limit - 0.2),high=(vertical_limit - 0.2))*UP,
                    velocity = np.random.uniform(low=-velocity_limit,high=velocity_limit)*RIGHT,
                    tracker = tracker,
                    mass = 5,
                    gravity = 0.05,
                    gas_type="air",
                    fire_limit = fire_limit,
                    horizontal_limit = horizontal_limit,
                    vertical_limit = vertical_limit
            )
            particles += particle
        
        
        for i in range(50):
            particle = Particle(
                    stroke_color=BLUE_D, fill_color=BLUE,
                    point    = np.random.uniform(low=-(horizontal_limit - 0.2),high=(horizontal_limit - 0.2))*RIGHT+np.random.uniform(low=-(vertical_limit - 0.2),high=(vertical_limit - 0.2))*UP,
                    velocity = np.random.uniform(low=-velocity_limit,high=velocity_limit)*RIGHT,
                    tracker = tracker,
                    mass = 5,
                    gravity = 0.05,
                    gas_type="gas",
                    fire_limit = fire_limit,
                    horizontal_limit = horizontal_limit,
                    vertical_limit = vertical_limit
            )
            particles += particle

        self.add(particles, Rectangle(width=13.2, height=7.2, stroke_width=5, color=BLACK))
        tracker.set_value(0)
        self.wait(1)
        tracker.set_value(1)
        self.wait(1)
        
        self.play(fire_limit.animate.set_value(-2), tracker.animate.set_value(1.3), run_time=2)
        self.wait(5)
  
        
        
        
        
class GasDichte(Scene):
    def construct(self):        
        self.camera.background_color = WHITE

        normalbedingung_T = myTex(r"Temperatur: $T = 0\, ^{\circ}$C")
        normalbedingung_P = myTex(r"Druck: $1013,25\, $mbar")
        dichte_Formel = myMathTex(r"\text{Dichte } \rho = \dfrac{\text{Masse}}{\text{Volumen}} = \dfrac{m}{V}")

        trenner = Line(start=[-5, 1.5, 0], end=[5, 1.5, 0], color=BLACK, stroke_width=0.5)

        normalbedingung = VGroup(normalbedingung_P, normalbedingung_T, dichte_Formel, trenner)


        dichte_Luft = myTex(r"Luft: $\rho = 1,29\, \dfrac{kg}{m^3}$")
        dichte_CO = myTex(r"Kohlenmonoxid: $\rho = 1,25\, \dfrac{kg}{m^3}$")
        dichte_H = myTex(r"Wasserstoff: $\rho = 0.09\, \dfrac{kg}{m^3}$")
        dichte_CH4 = myTex(r"Methan: $\rho = 0.71\, \dfrac{kg}{m^3}$")
        dichte_Propan = myTex(r"Propan: $\rho = 2.00\, \dfrac{kg}{m^3}$")
        dichte_Erdgas = myTex(r"Erdgas: $\rho = 0.80\, \dfrac{kg}{m^3}$")

        dichten = VGroup(dichte_Luft, dichte_CO, dichte_H, dichte_CH4, dichte_Propan, dichte_Erdgas,).shift(DOWN)
        dichten.arrange_in_grid(cols=2, buff=(1, 0.25), col_alignments="ll", flow_order="dr")

        self.play(Write(normalbedingung_T))
        self.wait(1)
        self.play(normalbedingung_T.animate.to_edge(LEFT).shift(3.5*UP))
        self.wait(1)
        self.play(Write(normalbedingung_P))
        self.wait(1)
        self.play(normalbedingung_P.animate.to_edge(LEFT).shift(2.5*UP))
        self.wait(1)
        self.play(Write(dichte_Formel))
        self.wait(1)
        self.play(dichte_Formel.animate.to_edge(RIGHT).shift(3*UP))
        self.wait(1)

        self.play(Create(trenner))
        self.wait(1)
    
        self.play(Write(dichte_Luft))
        self.wait(1)
        self.play(Write(dichte_CO))
        self.play(dichte_CO.animate.shift(UP*0.2).set_color(BLUE), rate_func=rate_functions.there_and_back, run_time=0.5)
        self.wait(1)
        self.play(Write(dichte_H))
        self.play(dichte_H.animate.shift(UP*0.2).set_color(BLUE), rate_func=rate_functions.there_and_back, run_time=0.5)
        self.wait(1)
        self.play(Write(dichte_CH4))
        self.play(dichte_CH4.animate.shift(UP*0.2).set_color(BLUE), rate_func=rate_functions.there_and_back, run_time=0.5)
        self.wait(1)
        self.play(Write(dichte_Propan))
        self.play(dichte_Propan.animate.shift(DOWN*0.2).set_color(RED), rate_func=rate_functions.there_and_back, run_time=1.5)
        self.wait(1)
        self.play(Write(dichte_Erdgas))
        self.play(dichte_Erdgas.animate.shift(UP*0.2).set_color(BLUE), rate_func=rate_functions.there_and_back, run_time=0.5)
        self.wait(3)

        self.play(FadeOut(dichten, shift=DOWN, scale=3), run_time=0.5)
        self.wait(0.5)
        self.play(normalbedingung.animate.shift(UP*5), run_time=0.5)
        self.play(FadeOut(normalbedingung), run_time=1) # = self.wait(1)



class Brennwert(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        heizwert = myTex(r"Heizwert", font_size=98)
        heizwert_superior = myTex(r"oberer Heizwert ", r"H", r"$_{\text{superior}}$").to_edge(RIGHT).shift(UP)
        heizwert_s = myTex(r"oberer Heizwert ", r"H", r"$_{s}$").to_edge(RIGHT).shift(UP)
        brennwert = myTex(r"Brennwert B").to_edge(RIGHT).shift(UP)
        heizwert_inferior = myTex(r"unterer Heizwert ", r"H", r"$_{\text{inferior}}$").to_edge(LEFT).shift(UP)
        heizwert_i = myTex(r"unterer Heizwert ", r"H", r"$_{i}$").to_edge(LEFT).shift(UP)
        heizwert_pur = myTex(r"Heizwert H").to_edge(LEFT).shift(UP)

        elf_prozent = myMathTex(r"11\,\%")
        kondensation = myTex(r"Kondensationswärme")
        pfeil = Arrow(start=0.3*DOWN + 1.5*LEFT, end=0.3*UP + 1.5*RIGHT, color=BLACK, stroke_width=2).shift(UP) # zeigt nach schräg oben und trägt elf_prozent
        elf_prozent.rotate(pfeil.get_angle()).shift(UP*1.25)

        einheit = myTex(r"Einheit: ").shift(DL)
        kwh = myMathTex(r"1\,", r"\dfrac{\text{kWh}}{\text{m}^3}").next_to(einheit)
        MJ = myMathTex(r"3.6\, \dfrac{\text{MJ}}{\text{m}^3}").next_to(einheit)

        
        


        self.play(Write(heizwert))
        self.wait(1)
        self.play(heizwert.animate.set_font_size(72).shift(UP*3))
        self.wait(1)
        # Mind map
        self.play(Write(heizwert_inferior), Write(heizwert_superior))
        self.wait(1)
        self.play(ReplacementTransform(heizwert_inferior, heizwert_i))
        self.play(ReplacementTransform(heizwert_superior, heizwert_s))
        self.wait(1)
        
        # self.play(Create(pfeil))
        
        self.play(heizwert_i.animate.scale(0.9), heizwert_s.animate.scale(1.1))
        self.wait(2)

        self.play(ReplacementTransform(heizwert_i, heizwert_pur))
        self.play(ReplacementTransform(heizwert_s, brennwert))
        self.wait(1)
        # self.play(Write(elf_prozent))
        self.wait(1)
        
        self.play(Write(einheit))
        self.wait()
        self.play(Write(kwh))
        self.wait()
        self.play(TransformMatchingShapes(kwh, MJ))
        self.wait(0.3)
        self.play(TransformMatchingShapes(MJ, kwh))
        self.wait(0.3)
        self.play(TransformMatchingShapes(kwh, MJ))
        self.wait(0.3)
        self.play(TransformMatchingShapes(MJ, kwh))
        self.wait()
        self.play(FadeOut(kwh[0]), kwh[1].animate.next_to(heizwert, buff=0.2), FadeOut(einheit))
        backgroundRectangle1 = BackgroundRectangle(kwh[1], color=BLACK, fill_opacity=0.2, buff=0.1)
        self.play(Create(backgroundRectangle1))
        self.wait()

        # Beispiel-Rechnung
        bruchstrich1 = Line(start=LEFT, end=LEFT + brennwert.get_right() - brennwert.get_left(), color=BLACK)
        minus_1 = myMathTex(r"\, -1").next_to(bruchstrich1, RIGHT)
        

        self.play(Create(bruchstrich1), brennwert.animate.next_to(bruchstrich1, UP), heizwert_pur.animate.next_to(bruchstrich1, DOWN))
        self.play(Write(minus_1))
        self.wait()
        bruch1 = VGroup(minus_1, bruchstrich1, heizwert_pur, brennwert)
        self.play(bruch1.animate.shift(LEFT*3))
        self.wait()

        
        equals1 = myMathTex(r"\,=\,").next_to(minus_1)
        heizwert_zahl = myMathTex(r"10,3\,", r"\dfrac{\text{kWh}}{\text{m}^3}")
        brennwert_zahl = myMathTex(r"11,4\,", r"\dfrac{\text{kWh}}{\text{m}^3}")
        bruchstrich2 = Line(start=LEFT, end=RIGHT, color=BLACK)
        bruchstrich2.set_length(heizwert_zahl.get_right() - heizwert_zahl.get_left())
        bruchstrich2.next_to(equals1, RIGHT, buff=0.2)
        heizwert_zahl.next_to(bruchstrich2, DOWN)
        brennwert_zahl.next_to(bruchstrich2, UP)
        minus_1_2 = always_redraw(lambda: myMathTex(r"\, -1").next_to(bruchstrich2))
        
        self.play(Write(equals1))
        self.play(Create(bruchstrich2), Write(heizwert_zahl), Write(brennwert_zahl))
        self.play(Write(minus_1_2))
        self.wait()

        cross_oben = Cross(brennwert_zahl[1], color=RED_C)
        cross_unten = Cross(heizwert_zahl[1], color=RED_C)
        
        self.play(Create(cross_oben), Create(cross_unten))
        self.wait()
        self.play(FadeOut(brennwert_zahl[1]), FadeOut(heizwert_zahl[1]), FadeOut(cross_oben), FadeOut(cross_unten),
                  bruchstrich2.animate.set_length(heizwert_zahl[0].get_right() - heizwert_zahl[0].get_left()),
                  heizwert_zahl[0].animate.next_to(bruchstrich2, DOWN),
                  brennwert_zahl[0].animate.next_to(bruchstrich2, UP)
                  )
        bruch2 = VGroup(bruchstrich2, heizwert_zahl[0], brennwert_zahl[0], minus_1_2)
        self.play(bruch2.animate.next_to(equals1))
        self.wait()

        
        equals2 = myMathTex(r"\,=\,").next_to(minus_1_2)
        ergebnis1 = myMathTex(r"0,107").next_to(equals2)
        ergebnis2 = myMathTex(r"10,7\,\%").next_to(equals2)
        underline1 = Underline(ergebnis2, color=RED_C)

        self.play(Write(equals2))
        self.play(Write(ergebnis1))
        self.wait()
        self.play(ReplacementTransform(ergebnis1, ergebnis2))
        self.wait()
        self.play(Create(underline1))
        self.wait()


        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        