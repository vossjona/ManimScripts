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


class Wave(FunctionGraph):
    def __init__(self, period_factor, amp, range_factor=1, color=BLACK, **kwargs):
        super().__init__(function = lambda x: np.sin((2*np.pi * x * period_factor )) * amp, x_range =[0, 12 * range_factor], **kwargs)
        self.period_factor=period_factor
        self.amp=amp
        self.range_factor=range_factor
        self.color=color


# Longitudinal Coherence
class Longitudinal(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        

        wave1 = Wave(period_factor=1, amp=2, color="#FF1F5B").shift(6*LEFT + UP)
        wave2 = Wave(period_factor=1.1, amp=2, color="#009ADE").shift(6*LEFT + UP)

        axis = Arrow(start=[-6,0,0], end=[7,0,0], color=BLACK, buff=0).shift(UP)
        axis.set_opacity(1)
        coherence_length = Arrow(start=[-6, -3, 0], end=[-6 + 5, -3, 0], color=BLACK, buff=0).shift(UP)
        twice_coherence_length = Arrow(start=[-6, -4, 0], end=[-6 + 10, -4, 0],  color=BLACK, buff=0).shift(UP)
        text_coherence_length = myMathTex(r"\ell_L").next_to(coherence_length, DOWN, buff=0.05)
        text_twice_coherence_length = myMathTex(r"2 \ell_L").next_to(twice_coherence_length, DOWN, buff=0.05)

        vert1 = Line(start=[-1,-2.1,0], end=[-1,2,0], color=BLACK)
        vert2 = Line(start=[4,-3.1,0], end=[4,2,0], color=BLACK)


        self.add(wave1, wave2)
        self.add(coherence_length, twice_coherence_length)
        self.add(vert1, vert2)
        self.add(text_coherence_length, text_twice_coherence_length)
        self.add(axis)

        self.wait()

# Transverse Coherence doesn't make sense like this
class Transverse(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        source = Ellipse(height=2, width=0.6, color=BLACK)
        source.move_to([-6,-2,0])

        propagation_distance = 10
        period = 1
        amplitude = 0.2

        angle_axis2 = 0.2# 0.16514867741462683

        axis1 = Line(start=source.get_top(), end=source.get_top() + propagation_distance*RIGHT, color=BLACK)
        axis2 = Line(start=source.get_bottom(), end=source.get_bottom() + propagation_distance * (np.cos(angle_axis2)*RIGHT + np.sin(angle_axis2)*UP), color=BLACK)

        wave1 = get_sine_wave(period_factor=period, amp=amplitude, range_factor=propagation_distance/12, color="#FF1F5B").set_stroke_opacity(0.6)
        wave1.move_to(axis1)
        wave2 = get_sine_wave(period_factor=period, amp=amplitude, range_factor=1 * propagation_distance/12, color="#009ADE").set_stroke_opacity(0.6)
        wave2.move_to(axis2)
        wave2.rotate(angle_axis2)

        wavefront_length = 4
        wavefront1_1 = Line(start=axis1.get_end() + wavefront_length*UP,
                            end=axis1.get_end() + DOWN,
                            color="#FF1F5B")
        wavefront1_2 = DashedLine(start=axis1.get_end() + wavefront_length*UP + (1/period)*LEFT,
                                  end=axis1.get_end() + DOWN + (1/period)*LEFT,
                                  color="#FF1F5B")
        wavefront1_3 = DashedLine(start=axis1.get_end() + wavefront_length*UP + (2/period)*LEFT,
                                  end=axis1.get_end() + DOWN + (2/period)*LEFT,
                                  color="#FF1F5B")

        wavefront2_1 = Line(start=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*wavefront_length*UP + np.cos(np.pi/2 - angle_axis2)*wavefront_length*LEFT),
                            end=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*DOWN + np.cos(np.pi/2 - angle_axis2)*RIGHT),
                            color="#009ADE")
        wavefront2_2 = DashedLine(start=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*wavefront_length*UP + np.cos(np.pi/2 - angle_axis2)*wavefront_length*LEFT) + (1/period)*(np.sin(angle_axis2)*DOWN + np.cos(angle_axis2)*LEFT),
                             end=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*DOWN + np.cos(np.pi/2 - angle_axis2)*RIGHT) + (1/period)*(np.sin(angle_axis2)*DOWN + np.cos(angle_axis2)*LEFT),
                             color="#009ADE")
        wavefront2_3 = DashedLine(start=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*wavefront_length*UP + np.cos(np.pi/2 - angle_axis2)*wavefront_length*LEFT) + (2/period)*(np.sin(angle_axis2)*DOWN + np.cos(angle_axis2)*LEFT),
                             end=axis2.get_end() + (np.sin(np.pi/2 - angle_axis2)*wavefront_length*DOWN + np.cos(np.pi/2 - angle_axis2)*wavefront_length*RIGHT) + (2/period)*(np.sin(angle_axis2)*DOWN + np.cos(angle_axis2)*LEFT),
                             color="#009ADE")
        
        red_waves = VGroup()
        for i in range(5):
            wave = Wave(
                period_factor=period,
                amp=amplitude,
                range_factor=propagation_distance/12,
                color="#FF1F5B"
            )
            wave.move_to(axis1)
            wave.shift(i*UP*0.4)
            red_waves += wave

        blue_waves = VGroup()
        for i in range(5):
            wave = Wave(
                period_factor=period,
                amp=amplitude,
                range_factor=1 * propagation_distance/12,
                color="#009ADE"
            )
            wave.move_to(axis2)
            wave.rotate(angle_axis2)
            wave.shift(i*UP*0.4)
            wave.set_opacity(0.6)
            blue_waves += wave

        
        

        self.add(source)
        self.add(axis1, axis2)
        # self.add(vert1)
        # self.add(wave1, wave2)

        self.add(wavefront1_1, wavefront1_2)
        self.add(wavefront2_1, wavefront2_2)


        P = Dot(wavefront1_1.get_end(), radius=0.1, color=BLACK)
        P_text = myTex(r"P").next_to(P, RIGHT, buff=0.1)
        self.add(P, P_text)

        wavelength = DoubleArrow(start=wavefront1_2.get_end() + DOWN*0.1, end=wavefront1_1.get_end() + DOWN*0.1, buff=0, color=BLACK)
        wavelength_text = myMathTex(r"\lambda").next_to(wavelength, DOWN, buff=0.05)
        self.add(wavelength, wavelength_text)


        self.wait()