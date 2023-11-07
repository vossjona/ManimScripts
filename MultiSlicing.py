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

def myCurvedArrow(*args, color=BLACK, angle=-1.5707963267948966, **kwargs):
    return CurvedArrow(*args, color=color, angle=angle, **kwargs)

#Global parameters
focal_spot = [-6,0,0]
length = 10.5

class MultiSlicing(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        focal_spot_dot = Dot(focal_spot, radius=0.1, color=YELLOW_C)
        focus = DashedLine(start=focal_spot + 2*UP, end=focal_spot + 2*DOWN, color=BLACK, dash_length=0.15, dashed_ratio=0.3)
        focus_text = myTex("Focus").next_to(focus, DOWN, buff=0.01)


        axis = DashedLine(start=focal_spot, end=focal_spot + RIGHT*length, color=BLACK)
        oben = Line(start=focal_spot, end=axis.get_end() + 2*UP, color=YELLOW_C)
        unten = DashedLine(start=focal_spot, end=axis.get_end() + 2*DOWN, color=BLACK)

        cone = Polygon(focal_spot, axis.get_end() + 2*UP, axis.get_end() + 2*DOWN, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1)
        cone.set_z_index(-5)

        sample1 = DashedLine(start=focal_spot + 2*RIGHT + 3*UP, end=focal_spot + 2*RIGHT + 3*DOWN, color=BLACK, dash_length=0.2, dashed_ratio=0.5)
        sample1_text = myMathTex(r"O_1").next_to(sample1, UP, buff=0.1)
        sample1_text_prime = myMathTex(r"O_1'").next_to(sample1, DOWN, buff=0.1)
        
        sample2 = DashedLine(start=focal_spot + 4*RIGHT + 3*UP, end=focal_spot + 4*RIGHT + 3*DOWN, color=BLACK, dash_length=0.2, dashed_ratio=0.5)
        sample2_text = myMathTex(r"O_2").next_to(sample2, UP, buff=0.1)
        sample2_text_prime = myMathTex(r"O_2'").next_to(sample2, DOWN, buff=0.1)
        
        sample3 = DashedLine(start=focal_spot + 6*RIGHT + 3*UP, end=focal_spot + 6*RIGHT + 3*DOWN, color=BLACK, dash_length=0.2, dashed_ratio=0.5)
        sample3_text = myMathTex(r"O_3").next_to(sample3, UP, buff=0.1)
        sample3_text_prime = myMathTex(r"O_3'").next_to(sample3, DOWN, buff=0.1)
        

        detector = Rectangle(height=4, width=0.5, stroke_color=BLACK).next_to(cone, RIGHT, buff=0.01)
        detector.set_fill(color=BLACK, opacity=0.8)
        detector_text = myTex("detector", color=WHITE).rotate(-PI/2).move_to(detector.get_center())

        # There
        prop1 = myCurvedArrow(start_point=sample1.get_start() + DOWN, end_point=sample2.get_start() + DOWN, color=BLACK)
        prop1_text = myMathTex(r"\mathcal{N}").next_to(prop1, UP, buff=0.1)
        wave_in_1 = myMathTex(r"\psi _{i,1}").next_to(sample1, LEFT, buff=0.1).shift(1.5*UP)
        wave_out_1 = myMathTex(r"\psi _{e,1}").next_to(sample1, RIGHT, buff=0.1).shift(1.5*UP)

        prop2 = myCurvedArrow(start_point=sample2.get_start() + DOWN, end_point=sample3.get_start() + DOWN, color=BLACK)
        prop2_text = myMathTex(r"\mathcal{N}").next_to(prop2, UP, buff=0.1)
        wave_in_2 = myMathTex(r"\psi _{i,2}").next_to(sample2, LEFT, buff=0.1).shift(0.8*UP)
        wave_out_2 = myMathTex(r"\psi _{e,2}").next_to(sample2, RIGHT, buff=0.1).shift(0.8*UP)

        prop3 = myCurvedArrow(start_point=sample3.get_start() + DOWN, end_point=detector.get_corner(UL), angle=-0.8, color=BLACK)
        prop3_text = myMathTex(r"\mathcal{F}").next_to(prop3, UP, buff=0.1)
        wave_in_3 = myMathTex(r"\psi _{i,3}").next_to(sample3, LEFT, buff=0.1).shift(1.5*UP)
        wave_out_3 = myMathTex(r"\psi _{e,3}").next_to(sample3, RIGHT, buff=0.1).shift(1.5*UP)


        # Back
        prop4 = myCurvedArrow(start_point=sample2.get_end() + UP, end_point=sample1.get_end() + UP, color=BLACK)
        prop4_text = myMathTex(r"\mathcal{N}^{-1}").next_to(prop4, DOWN, buff=0.1)
        wave_in_4 = myMathTex(r"\psi '_{i,3}").next_to(sample3, RIGHT, buff=0.1).shift(1.5*DOWN)
        wave_out_4 = myMathTex(r"\psi '_{e,3}").next_to(sample3, LEFT, buff=0.1).shift(1.5*DOWN)

        prop5 = myCurvedArrow(start_point=sample3.get_end() + UP, end_point=sample2.get_end() + UP, color=BLACK)
        prop5_text = myMathTex(r"\mathcal{N}^{-1}").next_to(prop5, DOWN, buff=0.1)
        wave_in_5 = myMathTex(r"\psi '_{i,2}").next_to(sample2, RIGHT, buff=0.1).shift(0.8*DOWN)
        wave_out_5 = myMathTex(r"\psi '_{e,2}").next_to(sample2, LEFT, buff=0.1).shift(0.8*DOWN)

        prop6 = myCurvedArrow(start_point=detector.get_corner(DL), end_point=sample3.get_end() + UP, angle=-0.8, color=BLACK)
        prop6_text = myMathTex(r"\mathcal{F}^{-1}").next_to(prop6, DOWN, buff=0.1)
        wave_in_6 = myMathTex(r"\psi '_{i,1}").next_to(sample1, RIGHT, buff=0.1).shift(1.5*DOWN)
        wave_out_6 = myMathTex(r"\psi '_{e,1}").next_to(sample1, LEFT, buff=0.1).shift(1.5*DOWN)

        # Updates
        update_arrow = myCurvedArrow(start_point=focal_spot + 2*DOWN, end_point=focal_spot + 2*UP, color=BLACK).shift(0.7*RIGHT)
        update_text = myTex(r"next position").rotate(PI/2).next_to(update_arrow, LEFT, buff=0.1)

        update_intensity = myCurvedArrow(start_point=detector.get_corner(UR), end_point=detector.get_corner(DR), color=BLACK).shift(0.2*RIGHT)
        intensity_text = myTex(r"update intensity").rotate(-PI/2).next_to(update_intensity, RIGHT, buff=0.1)


        

        # Adding everything
        self.add(focal_spot_dot)
        self.add(cone)

        self.add(detector, detector_text)
        self.add(sample1, sample2, sample3)
        self.add(sample1_text, sample2_text, sample3_text)
        self.add(sample1_text_prime, sample2_text_prime, sample3_text_prime)
        self.add(prop1, prop2, prop3)
        self.add(prop1_text, prop2_text, prop3_text)
        self.add(prop4, prop5, prop6)
        self.add(prop4_text, prop5_text, prop6_text)
        self.add(wave_in_1, wave_in_2, wave_in_3, wave_out_1, wave_out_2, wave_out_3)
        self.add(wave_in_4, wave_in_5, wave_in_6, wave_out_4, wave_out_5, wave_out_6)
        self.add(update_arrow)
        self.add(update_text)
        self.add(update_intensity, intensity_text)