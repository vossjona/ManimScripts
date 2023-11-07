from manim import *
import numpy as np
from manim.mobject.geometry.tips import ArrowTriangleTip,\
                                        ArrowSquareTip, ArrowSquareFilledTip,\
                                        ArrowCircleTip, ArrowCircleFilledTip

#Define Text, Tex and MathTex new with BLACK as default color
def myTex(*args, color=BLACK, **kwargs):
    return Tex(*args, color=color, **kwargs)
        
def myMathTex(*args, color=BLACK, **kwargs):
    return MathTex(*args, color=color, **kwargs)

def myText(*args, color=BLACK, **kwargs):
    return Text(*args, color=color, **kwargs)

class NumericalAperture(Scene):
    def construct(self):
        self.camera.background_color = WHITE


        focal_spot = [-6,0,0]
        length = 11
        focal_spot_dot = Dot(focal_spot, radius=0.1, color=YELLOW_C)
        axis = DashedLine(start=focal_spot, end=focal_spot + RIGHT*length, color=BLACK)
        oben = Line(start=focal_spot, end=axis.get_end() + 2*UP, color=YELLOW_C)
        unten = DashedLine(start=focal_spot, end=axis.get_end() + 2*DOWN, color=BLACK)
        probe = Line(start=oben.get_end(), end=unten.get_end(), color=YELLOW_C)

        cone = Polygon(focal_spot, axis.get_end() + 2*UP, axis.get_end() + 2*DOWN, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1)
        cone.set_z_index(-5)

        z = myMathTex(r"z_1").next_to(axis, UP, buff=0.1)

        arrow_dp = DoubleArrow(start=unten.get_end(), end=axis.get_end(), buff=0, stroke_width=probe.get_stroke_width() ,color=BLACK).next_to(probe, RIGHT, buff=0.1).shift(DOWN)
        dp = myMathTex(r"\dfrac{d_P}{2}").next_to(arrow_dp, RIGHT, buff=0.1)

        
        hypo = myMathTex(r"\sqrt{z_1^2 + \left(d_P/2 \right)^2}")
        hypo.rotate(unten.get_angle())
        hypo.next_to(unten, DOWN, aligned_edge=UP, buff=0.01)


        angle = Angle(unten, axis, radius=length//2, color=BLACK)
        theta = myMathTex(r"\theta").next_to(angle, LEFT, buff=0.1).shift(UP*0.07)



        self.add(focal_spot_dot, axis, unten)
        # self.add(oben, unten, probe)
        self.add(z, arrow_dp, dp, angle, theta)
        # self.add(arrow_hypo)
        self.add(cone)
        self.add(hypo)
        self.wait()
        