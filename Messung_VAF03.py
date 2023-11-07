from manim import *

#Define Text, Tex and MathTex new with BLACK as default color
def myTex(*args, color=BLACK, **kwargs):
    return Tex(*args, color=color, **kwargs)
        
def myMathTex(*args, color=BLACK, **kwargs):
    return MathTex(*args, color=color, **kwargs)

def myText(*args, color=BLACK, **kwargs):
    return Text(*args, color=color, **kwargs)

class Messung(Scene):
    def construct(self):
        self.camera.background_color = WHITE

    

        zeit = myTex(r"Zeit: ").shift(UP*3.5 + LEFT)
        start = myTex(r"Start: ").shift(UP*2.5 + LEFT)
        ende = myTex(r"Ende: ").shift(UP*1.5 + LEFT)

        self.play(Write(zeit))
        self.wait()
        self.play(Write(start))
        self.wait()
        self.play(Write(ende))
        self.wait()

        start_wert = myMathTex(r"0,570\,", "m^3").next_to(start, RIGHT, buff=0.2)
        start_wert[1].set_color(BLUE_C)

        zeit_wert = myMathTex(r"109\,", "s").next_to(zeit, RIGHT, buff=0.2)
        zeit_wert[1].set_color(BLUE_C)

        ende_wert = myMathTex(r"0,705\,", "m^3").next_to(ende, RIGHT, buff=0.2)
        ende_wert[1].set_color(BLUE_C)

        self.play(Write(start_wert))
        self.wait()
        self.play(Write(zeit_wert))
        self.wait()
        self.play(Write(ende_wert))
        self.wait()

        gasmenge = myTex(r"Gasmenge: ").shift(LEFT*1.5)
        start_wert_copy = myMathTex(r"0,570\,", "m^3").next_to(gasmenge, RIGHT, buff=0.2)
        start_wert_copy[1].set_color(BLUE_C)
        ende_wert_copy = myMathTex(r"0,705\,", "m^3").next_to(start_wert_copy, DOWN, buff=0.2)
        ende_wert_copy[1].set_color(BLUE_C)
        minus = myMathTex(r"-").next_to(ende_wert_copy, LEFT, buff=0.2)

        ergebnis_strich = Line(start=[gasmenge.get_corner(DR) + 0.9*DOWN + LEFT*0.3], end=[gasmenge.get_corner(DR) + 0.9*DOWN + 2.2*RIGHT], color=BLACK)
        ergebnis = myMathTex(r"0,135\,", "m^3").next_to(ende_wert_copy, DOWN, buff=0.2)
        ergebnis[1].set_color(BLUE_C)
        gleich = myMathTex(r"=").next_to(ergebnis, LEFT, buff=0.2)

        self.play(Write(gasmenge))
        self.wait()
        self.play(Write(start_wert_copy))
        self.wait()
        self.play(Write(minus), Write(ende_wert_copy))
        self.play(Create(ergebnis_strich))
        self.play(Write(gleich), Write(ergebnis))
        self.wait()

        kringel = Ellipse(width=1.5, height=3, color=RED_C).move_to([0.5, -1.5, 0]).rotate(PI/2)
        self.play(Create(kringel, rate_func=there_and_back_with_pause))
        self.wait()


        
