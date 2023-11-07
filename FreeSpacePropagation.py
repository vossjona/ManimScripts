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


class Blob(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_points(self):
        # Generate the points that define the shape of the blob using Bézier curves
        self.set_points_smoothly([
            UP*0.1 + LEFT*0.3,
            DOWN*0.2 + LEFT*0.4,
            DOWN*0.6 + LEFT*0.5,
            DOWN*0.8 + LEFT*0.1,
            DOWN*0.7 + RIGHT*0.2,
            DOWN*0.3 + RIGHT*0.4,
            DOWN*0.1 + RIGHT*0.5,
            UP*0.1 + RIGHT*0.3,
            UP*0.3 + RIGHT*0.1,
            UP*0.4 + LEFT*0.1,
            UP*0.2 + LEFT*0.2,
            UP*0.1 + LEFT*0.3
        ])


class FreeSpacePropagation(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        #Origin Plane
        origin_1 = [-4, -1, 0]
        
        xaxis = Arrow(start=origin_1, end=origin_1 + 4*UP, color=BLACK, buff=0)
        xaxis_text = myMathTex("x").next_to(xaxis, UR, buff=0)
        yaxis = Arrow(start=origin_1, end=origin_1 + 2*RIGHT + 1*DOWN, color=BLACK, buff=0)
        yaxis_text = myMathTex("y").next_to(yaxis, DR, buff=0.05)
        zaxis = Arrow(start=origin_1, end=origin_1 + 8*RIGHT + 2*UP, color=BLACK, buff=0)
        zaxis_text = myMathTex("z").next_to(zaxis, UR, buff=0.05)

        blob = Blob(stroke_color=BLACK, fill_color="#009ADE", fill_opacity=0.5).move_to(origin_1).set_z_index(-5).scale(2).shift(UP*0.5) 
        A = myTex(r"\textbf{A}").next_to(blob, DOWN, buff=0.1)
        a = myMathTex(r"\textbf{a}").next_to(blob)

        plane_1 = Polygon([-5, -1.5, 0], [-3, -2.5, 0], [-3, 0.5, 0], [-5, 1.5, 0],
                          stroke_color=BLACK, fill_color=BLACK, fill_opacity=0).scale(1.5)
        
        starting_point = [-4.2, 0, 0]
        starting_point_marker = Dot(starting_point, color="#FF1F5B")
        

        #Propagated Plane
        origin_2 = [3, 0.75, 0]
        xaxis_prop = Arrow(start=origin_2, end=origin_2 + 3*UP, color=BLACK, buff=0)
        xaxis_text_prop = myMathTex("x").next_to(xaxis_prop, UR, buff=0)
        yaxis_prop = Arrow(start=origin_2, end=origin_2 + 1.5*RIGHT + 0.75*DOWN, color=BLACK, buff=0)
        yaxis_text_prop = myMathTex("y").next_to(yaxis_prop, DR, buff=0.05)
        
        plane_2 = Polygon([2, 0.25, 0], [4, -0.75, 0], [4, 2, 0], [2, 2.75, 0],
                          stroke_color=BLACK, fill_color=BLACK, fill_opacity=0).scale(1)
        
        observation_point = [2.7, 2.15, 0]
        observation_marker = Dot(observation_point, color="#FF1F5B")
        
        #Connection        
        shifted_zaxis = DashedLine(start=starting_point, end=[2.7, 1.75, 0], color=BLACK).set_z_index(-4)
        propagation_arrow = Arrow(start=starting_point, end=observation_point, color="#FF1F5B", buff=0.05)
        r = myMathTex(r"\vec{\textbf{r}}", color="#FF1F5B").move_to([-0.1, 1.6, 0])
        delta_z = myMathTex(r"\Delta z").move_to([-0.1, 0.7, 0])

        xy = myMathTex(r"\textbf{r}_0", color="#FF1F5B").next_to(starting_point, DOWN, buff=0.1).shift(LEFT*0.2)
        xy_prop = myMathTex(r"\textbf{r}'", color="#FF1F5B").next_to(observation_point, DOWN, buff=0.01).shift(RIGHT*0.1)

        theta = Angle(shifted_zaxis, propagation_arrow, radius=6, color=BLACK).set_z_index(-4)
        theta_pointer = CubicBezier(start_anchor=[1, 2, 0], start_handle=[1.3, 1.8, 0], end_handle=[1, 1.8, 0], end_anchor=[1.4, 1.55, 0], color=BLACK)
        theta_text = myMathTex(r"\theta").next_to(theta_pointer.get_start(), UL, buff=0.01)
        

        # 
        axises = VGroup(xaxis, yaxis, zaxis, xaxis_prop, yaxis_prop)
        axises.set_opacity(0.75)

        axis_text = VGroup(xaxis_text, yaxis_text, zaxis_text, xaxis_text_prop, yaxis_text_prop)
        axis_text.set_opacity(0.85)

        self.add(axises)
        self.add(axis_text)
        self.add(blob, A)
        self.add(plane_1, plane_2)
        self.add(starting_point_marker, observation_marker)

        self.add(propagation_arrow, shifted_zaxis)
        self.add(theta, theta_pointer, theta_text)
        self.add(xy_prop, xy, r, delta_z)
        self.wait()