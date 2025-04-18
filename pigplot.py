import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
async def _():
    try:
        import micropip
        await micropip.install('svg-py')
    except ImportError:
        pass  # Handle the error or provide an alternative solution
    return (micropip,)


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from svg import SVG, G, Circle, Path, Title, Ellipse, Text, Line
    import random
    import string
    import math
    return (
        Circle,
        Ellipse,
        G,
        Line,
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
    df = pd.read_csv("https://raw.githubusercontent.com/Yokie0105/data-visualization-project-1/refs/heads/master/data/feeding_data.csv")


    Pig_data = df.groupby("pig").mean(numeric_only=True)
    return Pig_data, df


@app.cell
def _(Circle, Ellipse, G, Path, Title, math, my_slider):
    #create function for custom visual 
    class Pig:
        def __init__(
            self, duration, rate, intake, station, pig, index, class_
        ):
            self.duration =  round(duration, 1)
            #self.rate =  round(intake/duration, 3)
            self.rate =  round(rate, 3)
            self.intake =  round(intake, 1)
            self.station = (station -7) *7 *math.log(my_slider.value,10)
            self.pig = pig
            self.index = index
            self.class_ = class_ + " brushable"
            self.du = str(duration * 5)
            self.ra = str(rate * 60)

            self.lra = str(140 + math.log(self.rate) * 100)
            self.rra = str(220 - math.log(self.rate) * 100)

            self.int = str(intake)
            self.st = round(station,2)

            self.learns = f"transform:rotate({self.lra}deg)"
            self.rears = f"transform:rotate({self.rra}deg)"



        def bears(self):
            return(f"M {- self.station/2},{self.station*0.8} Q 0,{self.station*2} {self.station/2},{self.station*0.8}")


        def draw(self):
            return G(
                elements=[
                    #adding the title here makes it so it is visible when hovering any element of the pig (eg. The ears, The eyes,...)
                    Title(elements=[f"Station:{self.pig}, Pig_id:{self.index}, duration:{self.duration}, rate:{self.rate}, intake:{self.intake}, Weight of station: {self.st}"]),
                    Circle(cx=0, cy=0, r=self.station, class_= self.class_ , style="fill:#ee90ae; fill-opacity:0.8"),
                    Path(style=self.learns, d=self.bears(), class_=self.class_),  #the left ear (bezier curve)
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

            circle.cmmk6 {
                fill: #ff007f;
                fill-opacity: 0.5;
        }
            svg.cmmk6 {
            border: 1px solid;
        }
            line.fhds6 {
                stroke: black;
                stroke-width: 0.5;
                stroke-opacity: 0.8;
            }
            text.cmmk6 {
                font: bold 30px sans-serif;
                fill: black;

            }
            line.ggwp {
                stroke: black;
                stroke-width: 1;
                stroke-opacity: 1;
            }
            text.ggwp {
                font: 8px sans-serif;
                fill: black;

            }
             text.ggwp2 {
                font: 12px sans-serif;
                fill: black;

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
        pigs.append(Pig(row[5], row[6], row[7], row[1], row[0], idx, "cmmk6"))
    return idx, pigs, row


@app.cell
def translate_xy():
    # a glyph function that translates the pigs (moving them to the correct position )
    def translate_xy(pig):
        x = pig.intake *2
        y = 800 - pig.duration *2
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
    return (my_slider,)


@app.cell
def _(G, pigs, translate_xy):
    # making the plot 
    svg_elements = []
    for pig in pigs:
        svg_elements.append(G(elements=[pig.draw()], transform=translate_xy(pig)))
    return pig, svg_elements


@app.cell
def _(Circle, Ellipse, G, Line, Path, SVG, Text, math, svg_elements):
    #creating an svg elements list for the x-axis
    _x_axis = []
    for _d in [0,100,200,300,400]:
        _x_axis.append(Text(x=_d*1.93, y=780, elements=[_d], class_="fhds6"))
        _x_axis.append(Line(x1=_d*2, x2=_d*2, y1=800, y2=780, class_="fhds6"))

    #creating an svg elements list for the y-axis
    _y_axis = []
    for _d in [0,50,100,150,200,250,300,350,400]:
        _y_axis.append(Text(x=20, y=795-_d*1.94, elements=[_d], class_="fhds6"))
        _y_axis.append(Line(x1=0, x2=20, y1=800-_d*2, y2=800-_d*2, class_="fhds6"))



    #ears explenation (+title+explenation size)
    size= 40
    expl = []
    expl.append(Text(x=30, y=60, text="Plot of intake(x) against duration(y)", id="Titletext", class_="cmmk6"))
    expl.append(Text(x=610, y=20, text="The ears of the pigs is the rate at wich they eat", class_="ggwp"))
    expl.append(Text(x=30, y=80, text="The size of the pig is the weight of the feed when they start eating", class_="ggwp2"))
    expl.append(Line(x1=600, x2=800, y1=200, y2=200, class_="ggwp"))
    expl.append(Line(x1=600, x2=600, y1=200, y2=0, class_="ggwp"))
    expl.append(G(                 
                    elements= [

                        #lower ears
                    Path(style="transform:rotate(60deg)", d=f"M {- size/2},{size*0.8} Q 0,{size*2} {size/2},{size*0.8}", class_="cmmk6"),  #the left ear (bezier curve)
                    Path(style="transform:rotate(300deg)", d=f"M {- size/2},{size*0.8} Q 0,{size*2} {size/2},{size*0.8}", class_="cmmk6"),  #the right ear (bezier curve)

                        #higher ears
                    Path(style="transform:rotate(120deg)", d=f"M {- size/2},{size*0.8} Q 0,{size*2} {size/2},{size*0.8}", class_="cmmk6"),  #the left ear (bezier curve)
                    Path(style="transform:rotate(240deg)", d=f"M {- size/2},{size*0.8} Q 0,{size*2} {size/2},{size*0.8}", class_="cmmk6"),  #the right ear (bezier curve)


                    Circle(cx=0, cy=0, r=size, style="fill:#ee90ae; fill-opacity:1"),

                    # Snout
                    Ellipse(cx=0, cy=0, rx=size/2, ry=size/3, style="fill:#ee90ae; stroke:black"),
                    Circle(cx=-size/8, cy=0, r=size/7, style="fill:#000000"), # Left nostril
                    Circle(cx=size/8, cy=0, r=size/7, style="fill:#000000"),  # Right nostril

                    # Eyes
                    Ellipse(cx=-size/1.5, cy=-size/2, rx=size/5, ry=size/6, style="fill:#000000"),  
                    # Left eye
                    Ellipse(cx=size/1.5, cy=-size/2, rx=size/5, ry=size/6, style="fill:#000000")  
                    # Right eye)

                                ], transform="translate(700,110)"
                    ))

    #adding an axis to the ears
    _rate_axis = []
    for _d in [0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.2]:
        _rate_axis.append(Text(x=size*1.75, y=0, elements=[_d], class_="fhds6", style=f"transform:rotate({(-50 - math.log(_d) * 100)}deg)"))
        _rate_axis.append(Line(x1=size*1.5, x2=size*1.75, y1=0, y2=0, class_="fhds6", style=f"transform:rotate({(-50 - math.log(_d) * 100)}deg)"))


    #the axis for the pig
    expl.append(G(
                    elements= [ 
                            Circle(cx=0, cy=0, r=size*1.5,style="stroke:black; stroke-width:1; fill-opacity:0" ), _rate_axis

                                ], transform="translate(700,110)"
                ))


    svg2 = SVG(
        width=800,
        height=800,
        class_="cmmk6",
        elements=[svg_elements,_x_axis, _y_axis, expl] )
    return expl, size, svg2


@app.cell
def _(mo):
    # Display title
    title = mo.md(f"""#Custom visual scatterplot (overview graph)""")
    mo.vstack([title])
    return (title,)


@app.cell
def _(mo):
    info = mo.md("The graphs shows for all the pigs their intake, on the x axis, against the duration, on the y axis.")

    mo.vstack([info])
    return (info,)


@app.cell
def _(mo, svg2):
    mo.Html(svg2.as_str())
    return


@app.cell
def _(SVG, mo, my_slider, svg_elements):
    svg = SVG(width=800, height=800, class_="cmmk6", elements=svg_elements)

    mo.vstack([my_slider])
    return (svg,)


if __name__ == "__main__":
    app.run()
