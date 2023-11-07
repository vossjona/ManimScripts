from manim import *
import numpy as np

#Define Text, Tex and MathTex new with BLACK as default color
def myTex(*args, color=BLACK, **kwargs):
    return Tex(*args, color=color, **kwargs)
        
def myMathTex(*args, color=BLACK, **kwargs):
    return MathTex(*args, color=color, **kwargs)

def myText(*args, color=BLACK, **kwargs):
    return Text(*args, color=color, **kwargs)

#Global parameters



class Ptychography(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        tracker = ValueTracker(-2)
        size_tracker = ValueTracker(0.5)
        focal_spot = [tracker.get_value(), 0, 0]
        focal_spot_dot = Dot([tracker.get_value(), 0, 0], radius=0.1, color=YELLOW_C)
        focal_spot_dot.add_updater(lambda m: m.set_x([tracker.get_value(), 0, 0][0]))

        detector = Rectangle(height=4, width=0.5, stroke_color=BLACK).move_to([6, 0, 0])
        detector.set_fill(color=BLACK, opacity=0.7)
        detector_text = myTex("Detector").next_to(detector, DOWN, buff=0.01).shift(0.5*DOWN)

        lens1 = Ellipse(width=1.0, height=3.0, color=BLACK)
        lens2 = Ellipse(width=0.8, height=2.6, color=BLACK)
        lens3 = Ellipse(width=0.6, height=2.2, color=BLACK)
        lens4 = Ellipse(width=0.4, height=1.8, color=BLACK)
        lens5 = Ellipse(width=0.2, height=1.4, color=BLACK)
        lens = always_redraw(lambda: VGroup(lens1, lens2, lens3, lens4, lens5).move_to([tracker.get_value(), 0, 0] + 4*LEFT))
        lens_text = always_redraw(lambda: myTex("X-ray lens").next_to(lens, DOWN, buff=0.01).set_y(detector_text.get_y()))

        length = detector.get_left()[0] - tracker.get_value()
        axis = always_redraw(lambda: DashedLine(start=[-6, 0, 0], end=detector.get_left(), color=BLACK))

        cone = always_redraw(lambda: Polygon([tracker.get_value(), 0, 0], axis.get_end() + 2*UP, axis.get_end() + 2*DOWN, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1))
        cone.set_z_index(-5)
        cone2 = always_redraw(lambda: Polygon(lens1.get_top() + 3*LEFT, lens1.get_top(), [tracker.get_value(), 0, 0], lens1.get_bottom(), lens1.get_bottom() + 3*LEFT, fill_color=YELLOW_C, stroke_color=BLACK, fill_opacity=0.5, stroke_opacity=0.1))
        cone2.set_z_index(-5)

        sample = Polygon([tracker.get_value(), 0, 0] + length/4*RIGHT + 2*UP + 0.1*LEFT, [tracker.get_value(), 0, 0] + length/4*RIGHT + 2*UP + 0.1*RIGHT, [tracker.get_value(), 0, 0] + length/4*RIGHT + 2*DOWN + 0.1*RIGHT, [tracker.get_value(), 0, 0] + length/4*RIGHT + 2*DOWN + 0.1*LEFT,
                                               stroke_color=BLACK).set_fill(color=BLACK, opacity=0.7)
        sample_text = always_redraw(lambda: myTex("Sample").next_to(sample, DOWN, buff=0.01).set_y(detector_text.get_y()))

        
        focus = always_redraw(lambda: DashedLine(start=[tracker.get_value(), 0, 0], end=[tracker.get_value(), 0, 0] + 2*DOWN, color=BLACK, dash_length=0.1, dashed_ratio=0.5))
        focus.set_z_index(-5)
        focus_text = always_redraw(lambda: myTex("Focus").next_to(focus, DOWN, buff=0.01).set_y(detector_text.get_y()))

        self.wait()
        self.add(focal_spot_dot)
        self.add(cone)
        self.add(lens, lens_text)
        self.add(cone2)
        self.add(detector, sample, focus)
        self.add(sample_text, focus_text, detector_text)
        self.add(tracker)

        #Scanning
        self.wait()
        self.play(sample.animate.shift(0.2*UP), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*UP), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*UP), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*UP), run_time=0.3)
        self.wait(0.4)
        self.play(sample.animate.shift(0.2*DOWN), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*DOWN), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*DOWN), run_time=0.3)
        self.wait(0.1)
        self.play(sample.animate.shift(0.2*DOWN), run_time=0.3)
        self.wait(0.1)

        #Move lens out of view
        self.wait()
        sample.add_updater(lambda m: sample.move_to([tracker.get_value(), 0, 0] + length/4*RIGHT))
        self.play(tracker.animate.set_value(-6))
        self.wait()

        #Sample to the right
        self.play(sample.animate.shift(4*RIGHT), run_time=3)

        self.wait()


