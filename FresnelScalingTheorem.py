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

#Global parameters
focal_spot = [-6,0,0]
length = 11

class FresnelScalingTheoremCone(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        frame = FullScreenRectangle(color=BLACK)
        # self.add(frame)
        a = myTex("a)").to_corner(UL)

        focal_spot_dot = Dot(focal_spot, radius=0.1, color=YELLOW_C)
        axis = DashedLine(start=focal_spot, end=focal_spot + RIGHT*length, color=BLACK)
        oben = Line(start=focal_spot, end=axis.get_end() + 2*UP, color=YELLOW_C)
        unten = DashedLine(start=focal_spot, end=axis.get_end() + 2*DOWN, color=BLACK)
        probe = Line(start=oben.get_end(), end=unten.get_end(), color=YELLOW_C)

        cone = Polygon(focal_spot, axis.get_end() + 2*UP, axis.get_end() + 2*DOWN, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1)
        cone.set_z_index(-5)


        sample = DashedLine(start=focal_spot + length/3*RIGHT + 2*UP, end=focal_spot + length/3*RIGHT + 2*DOWN, color=BLACK, dash_length=0.15, dashed_ratio=0.3)
        sample_text = myTex("Sample").next_to(sample, DOWN, buff=0.01).shift(0.5*DOWN)
        
        focus = DashedLine(start=focal_spot + 2*UP, end=focal_spot + 2*DOWN, color=BLACK, dash_length=0.15, dashed_ratio=0.3)
        focus_text = myTex("Focus").next_to(focus, DOWN, buff=0.01)
        focus_text.set_y(sample_text.get_y())

        detector = Rectangle(height=4, width=0.5, stroke_color=BLACK).next_to(cone, RIGHT, buff=0.01)
        detector.set_fill(color=BLACK, opacity=0.7)
        detector_text = myTex("Detector").next_to(detector, DOWN, buff=0.01)
        detector_text.set_y(sample_text.get_y())

        z1 = DoubleArrow(start=focus.get_end(), end=sample.get_end(), buff=0, stroke_width=axis.get_stroke_width() ,color=BLACK)
        z1_text = myMathTex(r"z_1").next_to(z1, DOWN, buff=0.01)
        z2 = DoubleArrow(start=sample.get_end(), end=detector.get_corner(DL), buff=0, stroke_width=axis.get_stroke_width() ,color=BLACK)
        z2_text = myMathTex(r"z_2").next_to(z2, DOWN, buff=0.01)

        

        self.add(focal_spot_dot, axis)
        self.add(cone)

        self.add(detector, sample, focus)
        self.add(sample_text, focus_text, detector_text)
        self.add(z1, z1_text, z2_text, z2)
        
        self.add(a)


#Parallel
class FresnelScalingTheoremParallel(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        frame = FullScreenRectangle(color=BLACK)
        # self.add(frame)

        b = myTex("b)").to_corner(UL)

        axis = DashedLine(start=focal_spot, end=focal_spot + RIGHT*length, color=BLACK)

        beam = Polygon(focal_spot+UP, focal_spot+DOWN, axis.get_end() + DOWN, axis.get_end() + UP, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1)


        sample = DashedLine(start=focal_spot + length/3*RIGHT + 2*UP, end=focal_spot + length/3*RIGHT + 2*DOWN, color=BLACK, dash_length=0.15, dashed_ratio=0.3)
        sample.shift(RIGHT)
        sample_text = myTex("Sample").next_to(sample, DOWN, buff=0.01).shift(0.5*DOWN)

        detector = Rectangle(height=4, width=0.5, stroke_color=BLACK).next_to(axis, RIGHT, buff=0.01)
        detector.set_fill(color=BLACK, opacity=0.7)
        detector_text = myTex("Detector").next_to(detector, DOWN, buff=0.01)
        detector_text.set_y(sample_text.get_y())
    
        vg = VGroup(detector, detector_text, beam, axis)
        vg.shift(length/4*LEFT)
        

        zeff = DoubleArrow(start=sample.get_end(), end=detector.get_corner(DL), buff=0, stroke_width=axis.get_stroke_width() ,color=BLACK)
        zeff_text = myMathTex(r"z_\text{eff}").next_to(zeff, DOWN, buff=0.01)

        self.add(axis)
        self.add(beam)
        self.add(sample, sample_text)
        self.add(detector, detector_text)
        self.add(zeff, zeff_text)
        
        self.add(b)