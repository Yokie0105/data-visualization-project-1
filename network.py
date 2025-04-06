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
    import polars as pl
    import pandas as pd
    import numpy as np
    from svg import SVG, G, Line, Text, Rect
    import datetime as dt
    return G, Line, Rect, SVG, Text, dt, mo, np, pd, pl


@app.cell
def _(mo, pd):
    ## LOAD DATA

    # Load feeding data 
    feeding_path = mo.notebook_location() / "public" / "feeding_data.csv"
    feeding_data = pd.read_csv(str(feeding_path))
    print(feeding_path)

    # Ensure date, start and end columns are in datetime format
    feeding_data['date'] = pd.to_datetime(feeding_data['date'])
    feeding_data['start'] = pd.to_datetime(feeding_data['start'])
    feeding_data['end'] = pd.to_datetime(feeding_data['end'])

    # Load pigs data
    pigs_path = mo.notebook_location() / "public" / "Exp1 - Pig registration all info combined.csv"
    pigs_data = pd.read_csv(str(pigs_path))
    return feeding_data, feeding_path, pigs_data, pigs_path


@app.cell
def _(feeding_data):
    ## SET-UP

    # Define function for rescaling
    def rescale(value, domain_min, domain_max, new_min, new_max):
        return ((value - domain_min) / (domain_max - domain_min)) * (new_max - new_min) + new_min

    # Find minimum and maximum for intake per pig
    min_intake = round(float(feeding_data['tot_intake_day_pig'].min()), 2)
    max_intake = round(float(feeding_data['tot_intake_day_pig'].max()), 2)

    # Set new minimum and maximum for intake per pig
    new_min_intake = 20
    new_max_intake = 80

    # Find minimum and maximum for relation per pig
    min_relation = 0
    max_relation = 20

    # Set new minimum and maximum for relation 
    new_min_relation = 1.0
    new_max_relation = 15.0

    # Find minimum and maximum for intake per station
    min_intake_st = round(float(feeding_data['tot_intake_day_station'].min()), 2)
    max_intake_st = round(float(feeding_data['tot_intake_day_station'].max()), 2)

    # Find minimum and maximum for average rate per station
    min_rate_st = round(float(feeding_data['avg_rate_day_station'].min()), 2)
    max_rate_st = round(float(feeding_data['avg_rate_day_station'].max()), 2)

    # Find minimum and maximum for average duration per station
    min_duration_st = round(float(feeding_data['avg_duration_day_station'].min()), 2)
    max_duration_st = round(float(feeding_data['avg_duration_day_station'].max()), 2)

    # Fill domains dictionary
    domains_bar = {0: [min_intake_st, max_intake_st],
                  1: [min_rate_st, max_rate_st],
                  2: [min_duration_st, max_duration_st]}

    # Set new minimum and maximum for average duration per station
    new_min_bar = 0
    new_max_bar = 400
    return (
        domains_bar,
        max_duration_st,
        max_intake,
        max_intake_st,
        max_rate_st,
        max_relation,
        min_duration_st,
        min_intake,
        min_intake_st,
        min_rate_st,
        min_relation,
        new_max_bar,
        new_max_intake,
        new_max_relation,
        new_min_bar,
        new_min_intake,
        new_min_relation,
        rescale,
    )


@app.cell
def _():
    ## SVG (NON-INTERACTIVE)

    # Set SVG size
    svg_width = 550
    svg_height = 550
    margin = 100

    # Set node coordinates
    coords = {0: [1.00000000e+00, 2.70930202e-09], 
              1: [0.84125352, 0.54064077], 
              2: [0.41541508, 0.90963197], 
              3: [-0.14231483,  0.98982143],
              4: [-0.65486067,  0.75574964], 
              5: [-0.95949297,  0.28173259], 
              6: [-0.95949297, -0.28173255], 
              7: [-0.65486073, -0.75574958], 
              8: [-0.14231501, -0.98982143], 
              9: [ 0.41541511, -0.90963196], 
              10: [ 0.84125346, -0.54064088]
             }

    # Define connections between node coordinates
    connections = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (6, 7), (6, 8), (6, 9), (6, 10), (7, 8), (7, 9), (7, 10), (8, 9), (8, 10), (9, 10)]

    # Rescale node coordinates
    for key in coords:
        coords[key][0] *= svg_width/3
        coords[key][1] *= svg_height/3

    # Set bar size
    bar_width = 100
    spacing = 50
    return (
        bar_width,
        connections,
        coords,
        key,
        margin,
        spacing,
        svg_height,
        svg_width,
    )


@app.cell
def _():
    ## SCRIPT (NON-INTERACTIVE)

    script = """
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            let tooltip_text = document.getElementById("tooltip_text");
            let tooltip_rect = document.getElementById("tooltip_rect");
            let pigs = document.querySelectorAll("text");

            pigs.forEach(text => {
                text.addEventListener("mousemove", function (event) {
                    let textContent = this.getAttribute("data-pig_info");

                    tooltip_text.style.opacity = 1;
                    tooltip_text.textContent = textContent;
                    tooltip_rect.style.opacity = 0.5;

                    let textLength = textContent.length * 8;  
                    tooltip_rect.setAttribute("width", textLength);
                    tooltip_rect.setAttribute("height", 30); 

                    let svgRect = this.ownerSVGElement.getBoundingClientRect();
                    let x = event.clientX - svgRect.left + 10;
                    let y = event.clientY - svgRect.top - 10;

                    let maxX = svgRect.width - textLength - 10;  
                    let maxY = svgRect.height - 40;  
                    let minX = 10;  
                    let minY = 10;  

                    if (x > maxX) x = maxX;
                    if (x < minX) x = minX;
                    if (y > maxY) y = maxY;
                    if (y < minY) y = minY;

                    let transform = `translate(${x}, ${y})`;

                    tooltip_text.setAttribute("transform", transform);
                    tooltip_rect.setAttribute("transform", transform);
                });

                text.addEventListener("mouseleave", function () {
                    tooltip_text.style.opacity = 0;
                    tooltip_rect.style.opacity = 0;
                });
            });
        });
    </script>
    """
    return (script,)


@app.cell
def _(date, mo, station):
    # Display title
    title = mo.md(f"""# 🌽 Feeding network""")
    formatted_date = date.value.strftime("%d-%m-%Y")
    subtitle = mo.md(f"## Current network: station {station.value} on {formatted_date}")
    mo.vstack([title, subtitle])
    return formatted_date, subtitle, title


@app.cell
def _(mo):
    ## REACTIVE ELEMENTS 

    # Display user info
    info = mo.md("The feeding network visualizes the food intake of all pigs at one feeding station on a given day. Pigs who ate more frequently before or after each other have stronger connections. Select a station and a date below. Hover over a pig to get more information.")

    # Display reactive UI elements
    station = mo.ui.dropdown(options=[str(i) for i in range(1, 11)], value="1", label="Select station:")
    date = mo.ui.date(value="2020-12-04", start="2020-12-04", stop="2021-03-08", label="Select date:")
    mo.vstack([info, station, date])
    return date, info, station


@app.cell
def _(date, station):
    ## INTERACTIVE SET-UP

    def selected_station():
        return int(station.value) - 1

    def selected_date():
        return str(date.value)

    def compute_intake(filtered_data):
        intake = {}
        # Fill intake dictionary
        for station_index in range(10):
            intake[station_index] = {}
            for pig_index in range(11):
                subset = filtered_data[
                    (filtered_data['station'] == station_index + 1) &
                    (filtered_data['pig_index'] == pig_index)]
                if not subset.empty:
                    pig = int(subset['pig'].values[0])
                    total_intake = round(float(subset['tot_intake_day_pig'].values[0]), 2)
                else:
                    pig = int(filtered_data[(filtered_data['pig_index'] == pig_index)]['pig'].values[0])
                    total_intake = 0.0  
                intake[station_index][pig_index] = {'Pig': pig, 'Total intake': total_intake}
        return intake

    def compute_relations(filtered_data):
        relations = {}
        # Fill relations dictionary
        for station_index in range(10):
            relations[station_index] = {}
            index = 0
            for pig_index in range(11):
                for count_index in range(pig_index + 1, 11):
                    total_count = filtered_data[
                        (filtered_data['station'] == station_index + 1) &
                        (filtered_data['pig_index'] == pig_index) &
                        ((filtered_data['pig_before_index'] == count_index) | (filtered_data['pig_after_index'] == count_index))
                    ].shape[0]
                    relations[station_index][index] = total_count
                    index += 1
        return relations

    def compute_bar_values(filtered_data):
        bar_values = {}
        # Fill values dictionary
        for station_index in range(10):
            bar_values[station_index] = []
            subset = filtered_data[filtered_data['station'] == station_index + 1]
            if not subset.empty:
                bar_values[station_index].append(round(float(subset['tot_intake_day_station'].values[0]), 2))
                bar_values[station_index].append(round(float(subset['avg_rate_day_station'].values[0]), 2))
                bar_values[station_index].append(round(float(subset['avg_duration_day_station'].values[0]), 2))
            else:
                bar_values[station_index].append(0)  
                bar_values[station_index].append(0)
                bar_values[station_index].append(0)
        return bar_values
    return (
        compute_bar_values,
        compute_intake,
        compute_relations,
        selected_date,
        selected_station,
    )


@app.cell
def _(
    G,
    Line,
    Rect,
    SVG,
    Text,
    max_intake,
    max_relation,
    min_intake,
    min_relation,
    new_max_intake,
    new_max_relation,
    new_min_intake,
    new_min_relation,
    rescale,
):
    ## SVG (INTERACTIVE)

    def write_SVG_network(coords, connections, svg_width, svg_height, intake, station):
        # Create a title
        title = Text(
                x=(svg_width / 2), 
                y=22,  
                text="Feeding network",  
                text_anchor="middle",  
                dominant_baseline="middle",
                font_size="24px",  
                font_family="Georgia"
            )

        # Create nodes
        nodes = []
        for node in range(11):
            # Get node data based on intake
            node_data = intake[station][node]

            # Format node info displayed in tooltip
            node_info = " - ".join(f"{k}: {v}" for k, v in node_data.items())
            node_info_parts = node_info.split(" - ")
            node_info_parts[-1] += " kg"  # Add 'kg' to the last value
            node_info = " - ".join(node_info_parts)

            # Append node with formatted data
            nodes.append(
                Text(x=coords[node][0] + svg_width / 2,
                     y=coords[node][1] + svg_height / 2,
                     elements="\U0001F437",
                     text_anchor="middle",
                     dominant_baseline="middle",
                     class_=f"pig{node}",
                     data={"pig_info": node_info}
                )
            )

        # Create edges
        edges = []
        for edge in range(55):
            edges.append(
                Line(x1=coords[connections[edge][0]][0] + svg_width / 2,
                     y1=coords[connections[edge][0]][1] + svg_height / 2,
                     x2=coords[connections[edge][1]][0] + svg_width / 2,
                     y2=coords[connections[edge][1]][1] + svg_height / 2,
                     stroke="lightsalmon",
                     stroke_opacity=0.5,
                     class_=f"edge{edge}"
                )
            )

        # Create tooltip
        tooltip = G(id = "tooltip",
                    elements= [
                        Rect(x=0, y=0, width=100, height=30, fill="wheat", id="tooltip_rect"),
                        Text(x=0, y=20, id="tooltip_text")
                    ]
                   )

        # Merge nodes and tooltip
        interactive_nodes = nodes + [tooltip]

        # Create plot
        plot = SVG(width=svg_width,
                   height=svg_height,
                   elements=[title] + edges + interactive_nodes,
                   class_="network"
                  )

        return plot

    def write_SVG_barplot(svg_width, svg_height, margin, bar_width, spacing, bar_values, domains_bar, new_min_bar, new_max_bar, station):
        # Set some extra variables
        x_start = (svg_width - (3 * bar_width)) / 2
        variables = ["Total intake (kg)", "Average rate (kg/s)", "Average duration (s)"]  

        # Create a title
        title = Text(
                x=(svg_width / 2) + 45, 
                y=30,  
                text="Station summary",  
                text_anchor="middle",  
                dominant_baseline="middle",
                font_size="24px",  
                font_family="Georgia"
            )

        # Create bars
        bars = []
        for bar in range(3):
            # Set some extra variables
            x_coord = x_start + bar * (bar_width + spacing) 
            bar_height = rescale(bar_values[station][bar], domains_bar[bar][0], domains_bar[bar][1], new_min_bar, new_max_bar)  

            # Create bar group
            bar_group = G(
                id=f"bar_group{bar}",
                elements=[
                    Rect(x=x_coord, 
                         y=svg_height - bar_height - margin,  
                         width=bar_width - 10,  
                         height=bar_height,
                         fill="wheat",  
                         class_=f"bar{bar}"),

                    Text(x=x_coord + (bar_width - 10) / 2,
                         y=svg_height - bar_height / 2 - margin,  
                         text=str(bar_values[station][bar]),
                         text_anchor="middle",
                         dominant_baseline="middle",
                         fill="#de6238",  
                         class_=f"value{bar}"),

                    Text(x=x_coord + (bar_width - 10) / 2,
                         y=svg_height - margin + 25,  
                         text=variables[bar],
                         text_anchor="middle",
                         dominant_baseline="middle",
                         font_family="Georgia",
                         class_=f"variable{bar}")
                ]
            )

            # Append bar group to bars list
            bars.append(bar_group)

        # Create plot
        plot = SVG(width=svg_width,
                   height=svg_height,
                   elements=[title] + bars,
                   class_="barplot"
                  )

        return plot

    ## CSS (INTERACTIVE)

    def write_css_network(intake, relations, station):
        css = "<style>"  
        # Set node styles based on intake
        for node in range(11):
            intake_value = intake[station][node]['Total intake']
            intake_value = rescale(intake_value, min_intake, max_intake, new_min_intake, new_max_intake)
            css += f" text.pig{node} {{ font-size: {intake_value:.1f}px; }}"

        # Set edge styles based on relations
        for edge in range(55):
            relation_value = relations[station][edge]
            relation_value = rescale(relation_value, min_relation, max_relation, new_min_relation, new_max_relation)
            css += f" line.edge{edge} {{ stroke-width: {relation_value:.1f}px; }}"

        css += "#tooltip_text { opacity: 0; position: absolute; pointer-events: none; font-family: Georgia; font-size: 15px; }"
        css += "#tooltip_rect { opacity: 0; position: absolute; pointer-events: none; }"
        css += "</style>"  
        return css
    return write_SVG_barplot, write_SVG_network, write_css_network


@app.cell
def _(
    bar_width,
    compute_bar_values,
    compute_intake,
    compute_relations,
    connections,
    coords,
    domains_bar,
    feeding_data,
    margin,
    mo,
    new_max_bar,
    new_min_bar,
    script,
    selected_date,
    selected_station,
    spacing,
    svg_height,
    svg_width,
    write_SVG_barplot,
    write_SVG_network,
    write_css_network,
):
    ## PLOT

    def update_plot():
        # Filter feeding data for selected date
        filtered_data = feeding_data[feeding_data['date'] == selected_date()]

        # Compute intake and relations
        intake = compute_intake(filtered_data)
        relations = compute_relations(filtered_data)

        # Write SVG for current intake and relations
        network = write_SVG_network(coords, connections, svg_width, svg_height, intake, selected_station())

        # Write CSS for current intake and relations
        css = write_css_network(intake, relations, selected_station())

        # Compute bar values
        bar_values = compute_bar_values(filtered_data)

        # Write SVG for current bar_values
        barplot = write_SVG_barplot(svg_width, svg_height, margin, bar_width, spacing, bar_values, domains_bar, new_min_bar, new_max_bar,
                                    selected_station())

        # Update plot
        return mo.hstack([mo.iframe(network.as_str() + css + script, width=svg_width + 16, height=svg_height + 16),
                          mo.Html(barplot.as_str())])

    update_plot()
    return (update_plot,)


if __name__ == "__main__":
    app.run()
