import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from svg import SVG, G, Circle, Path, Title, Ellipse, Text
    import random
    import string
    import math
    return (
        Circle,
        Ellipse,
        G,
        Path,
        SVG,
        Text,
        Title,
        math,
        mo,
        pd,
        random,
        string,
    )


@app.cell
def _(pd):

    test1 = pd.read_csv("./data/feeding_data.csv")


    Pig_data = test1.groupby("pig").mean(numeric_only=True)

    print(test1.head)
    print(Pig_data.head)
    return Pig_data, test1


@app.cell
def _(Circle, Ellipse, G, Path, Title, math, my_slider):
    #create function for custom visual 
    class Pig:
        def __init__(
            self, duration, rate, intake, station, pig, index, class_
        ):
            self.duration =  round(duration, 1)
            self.rate =  round(intake/duration, 3)
            self.intake =  round(intake, 1)
            self.station = (station -7) *7 *math.log(my_slider.value,10)
            self.pig = pig
            self.index = index
            self.class_ = class_ + " brushable"
            self.du = str(duration * 5)
            self.ra = str(rate * 60)

            self.lra = str( 80 + math.log(self.rate) * 50)
            self.rra = str(280 - math.log(self.rate) * 50)

            self.int = str(intake)
            self.st = round(station,2)

            self.learns = f"transform:rotate({self.lra}deg)"

            self.rears = f"transform:rotate({self.rra}deg)"


        def ears(self):
            return(f"M {- self.station/2},{self.station*0.8} L 0,{self.station*1.5} L {self.station/2},{self.station*0.8}")

        def bears(self):
            return(f"M {- self.station/2},{self.station*0.8} Q 0,{self.station*2} {self.station/2},{self.station*0.8}")


        def draw(self):
            return G(
                elements=[
                    Title(elements=[f"Station:{self.pig}, Pig_index:{self.index}, duration:{self.duration}, rate:{self.rate}, intake:{self.intake}, Weight of station: {self.st}"]),
                    Circle(cx=0, cy=0, r=self.station, class_= self.class_ , style="fill:#ee90ae; fill-opacity:0.8"),
                    #Path(style=self.learns, d=self.ears(), class_=self.class_),  #the left ear
                    Path(style=self.learns, d=self.bears(), class_=self.class_),  #the left ear (bezier curve)
                    #Path(style=self.rears, d=self.ears(), class_=self.class_),  #the right ear
                    Path(style=self.rears, d=self.bears(), class_=self.class_),  #the right ear (bezier curve)
                    # Snout
                    Ellipse(cx=0, cy=0, rx=self.station/2, ry=self.station/3, style="fill:#ee90ae; stroke:black"),
                    Circle(cx=-self.station/8, cy=0, r=self.station/7, style="fill:#000000"), # Left nostril
                    Circle(cx=self.station/8, cy=0, r=self.station/7, style="fill:#000000"),  # Right nostril

                    # Eyes
                    Ellipse(cx=-self.station/1.5, cy=-self.station/2, rx=self.station/5, ry=self.station/6, style="fill:#000000"),  
                    # Left eye
                    Ellipse(cx=self.station/1.5, cy=-self.station/2, rx=self.station/5, ry=self.station/6, style="fill:#000000")  
                    # Right eye

                    #brand (cannot get this to work)
                    # , Text(f"{self.pig}", x=self.intake , y=400-self.duration, fill='black', font_size=30)
                ],
            )
    return (Pig,)


@app.cell
def _(mo):
    mo.md(
        r"""
        <style>
            path.cmmk6 {
                fill: #ed5b8c;
                fill-opacity: 0.9;
            }
            }
            circle.cmmk6 {
                fill: #ff007f;
                fill-opacity: 0.5;
            }
        </style>
        """
    )
    return


@app.cell
def _(Pig, Pig_data):
    #all pigs as array 
    pigs = []
    for idx,row in Pig_data.iterrows():
        pigs.append(Pig(row[5], row[6], row[7], row[1], row[0], row[29], "cmmk6"))
    return idx, pigs, row


@app.cell
def _(pigs):
    wtf = pigs[1:5]
    print(dir(wtf))
    return (wtf,)


@app.cell
def translate_xy():
    # a glyph function that translates the pigs (moving them to the correct position )
    def translate_xy(pig):
        x = pig.intake
        y = 400 - pig.duration 
        #return f"translate({x},{y})"
        return f"translate({x},{y})"
    return (translate_xy,)


@app.cell
def translate_y():
    def translate_y(pig): 
        y = pig.duration
        return f"transform:rotate({y}deg)"
    return (translate_y,)


@app.cell
def _(mo):
    my_slider = mo.ui.slider(start=4, stop=40, value=10, step=2, label="Size")
    [my_slider]
    return (my_slider,)


@app.cell
def _(G, SVG, mo, pigs, translate_xy):
    # making the plot 
    svg_elements = []
    for pig in pigs:
        svg_elements.append(G(elements=[pig.draw()], transform=translate_xy(pig)))

    svg = SVG(width=400, height=400, class_="cmmk6", elements=svg_elements)

    mo.Html(svg.as_str())
    return pig, svg, svg_elements


@app.cell
def _(mo, my_slider, svg):
    mo.vstack([my_slider,mo.Html(svg.as_str())])
    return


if __name__ == "__main__":
    app.run()
