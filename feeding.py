import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    return go, mo, np, pd


@app.cell
def _(pd):
    # -------------------------------
    # Load & preprocess
    # -------------------------------
    df = pd.read_csv("https://raw.githubusercontent.com/Yokie0105/data-visualization-project-1/refs/heads/master/data/feeding_data.csv")
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    df["date"] = df["start"].dt.date
    return (df,)


@app.cell
def _(mo):
    # Title of grahic 
    title = mo.md(f"#Visualizing Daily Feeding Patterns: A Spiral Approach")
    mo.vstack([title])
    return (title,)


@app.cell
def _(mo):
    # Display user information 
    info = mo.md("Explore the timeline of daily feeding sessions displayed on a spiral chart. Hover over the elements for detailed insights into each feeding moment.")

    # Interactive dropdowns station and pig 
    # Display reactive UI elements
    station_dropdown = mo.ui.dropdown(options=[str(i) for i in range(1, 11)], value="1", label="Select Feeding Station:")

    pig_dropdown = mo.ui.dropdown(
        options=[str(i) for i in range (0,11)], value="1", label="Select a Pig within the selected Feeding Station",
    )

    mo.vstack([info, station_dropdown, pig_dropdown])
    return info, pig_dropdown, station_dropdown


@app.cell
def _(df, pig_dropdown, station_dropdown):
    # Select data based on the dropdown boxes
    selected_station = station_dropdown.value
    selected_pig = pig_dropdown.value

    df_filtered = df[(df["station"] == int(selected_station)) & (df["pig_index"] == int(selected_pig))].copy()
    return df_filtered, selected_pig, selected_station


@app.cell
def _(selected_pig, selected_station):
    # To Control the dorpdown boxes 
    print(selected_pig)
    print(selected_station)
    return


@app.cell
def _(df_filtered):
    # -------------------------------
    # Group into feeding sessions
    # -------------------------------
    df_filtered_sessions = df_filtered.sort_values("start")
    df_filtered_sessions["time_diff"] = (df_filtered_sessions["start"] - df_filtered_sessions["end"].shift(1)).dt.total_seconds()
    threshold = 500  # 2.5 minutes
    df_filtered_sessions["feeding_group"] = (df_filtered_sessions["time_diff"] > threshold).cumsum()

    df_grouped = df_filtered_sessions.groupby(["feeding_group", "station", "pig_index"]).agg(
        start=("start", "first"), 
        end=("end", "last"), 
        total_intake=("intake", "sum")
    ).reset_index() 

    df_grouped["duration_min"] = (df_grouped["end"] - df_grouped["start"]).dt.total_seconds() / 60
    max_duration = df_grouped["duration_min"].max()


    df_grouped["date"] = df_grouped["start"].dt.date

    df_grouped["intake_ratio"] = df_grouped["total_intake"] / df_grouped["duration_min"]
    return df_filtered_sessions, df_grouped, max_duration, threshold


@app.cell
def _(df_grouped, go, np):
    # ------------
    # Spiral Setup
    # ------------
    all_dates = sorted(df_grouped["date"].unique())
    date_map = {date: i for i, date in enumerate(all_dates)}

    spiral_days = np.linspace(0, len(all_dates)-1, 1000)
    spiral_radius = 1 + 0.1 * spiral_days
    spiral_angle = spiral_days * 2 * np.pi / 50
    spiral_x = spiral_radius * np.cos(spiral_angle)
    spiral_y = spiral_radius * np.sin(spiral_angle)

    fig = go.Figure()

    # Spiral Line
    fig.add_trace(go.Scatter(
        x=spiral_x, y=spiral_y,
        mode="lines",
        line=dict(color="black", width=1),
        name="Spiral Path",
        hoverinfo="none"
    ))

    # Dot on spiral for each date
    for date in all_dates:
        day_idx = date_map[date]
        angle = day_idx * 2 * np.pi / 50
        radius = 1 + 0.1 * day_idx
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)


        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers",
            marker=dict(color="black", size=5),
            name=str(date),
            hovertext=str(date),
            hoverinfo="text",
            showlegend=False
        ))
    return (
        all_dates,
        angle,
        date,
        date_map,
        day_idx,
        fig,
        radius,
        spiral_angle,
        spiral_days,
        spiral_radius,
        spiral_x,
        spiral_y,
        x,
        y,
    )


@app.cell
def time_of_day_color():
    # -------------------------------
    # Color Mapping Function
    # -------------------------------
    def time_of_day_color(hour):
        if 0 <= hour < 6:
            return "#e41a1c"  # Red (night)
        elif 6 <= hour < 12:
            return "#ffdf00"  # Yellow (morning)
        elif 12 <= hour < 18:
            return "#4daf4a"  # Green (afternoon)
        else:
            return "#377eb8"  # Blue (evening)
    return (time_of_day_color,)


@app.cell
def _(go, np, time_of_day_color):
    # ----------------------
    # Feeding bars function
    # ----------------------
    def add_feeding_bars(fig, df_grouped, all_dates, date_map, max_duration):
        for date in all_dates:
            sessions = df_grouped[df_grouped["date"] == date].sort_values("start")
            day_idx = date_map[date]
            angle = day_idx * 2 * np.pi / 50
            base_radius = 1 + 0.1 * day_idx
            current_radius = base_radius

            for _, row in sessions.iterrows():
                length = (row["duration_min"] / max_duration) * 0.8
                x_start = current_radius * np.cos(angle)
                y_start = current_radius * np.sin(angle)
                x_end = (current_radius + length) * np.cos(angle)
                y_end = (current_radius + length) * np.sin(angle)

                start_hour = row["start"].hour
                color = time_of_day_color(start_hour)

                fig.add_trace(go.Scatter(
                    x=[x_start, x_end],
                    y=[y_start, y_end],
                    mode="lines",
                    line=dict(color=color, width=5),
                    hovertext=(
                        f"{row['start'].time()} – {row['end'].time()}<br>"
                        f"Duration: {row['duration_min']:.1f} min<br>"
                        f"Intake: {row['total_intake']:.1f} g<br>"
                        f"Ratio: {row['intake_ratio']:.2f} g/min"
                    ),
                    hoverinfo="text",
                    showlegend=False
                ))
                current_radius += length + 0.05
        return fig
    return (add_feeding_bars,)


@app.cell
def _(
    add_feeding_bars,
    all_dates,
    date_map,
    df_grouped,
    fig,
    go,
    max_duration,
    mo,
    selected_pig,
    selected_station,
):
    # Add Feeding Bars
    fig1 = add_feeding_bars(fig, df_grouped, all_dates, date_map, max_duration)

    # Layout
    legend_items = [
        {"color": "#e41a1c", "name": "00:00–06:00 (Night)"},
        {"color": "#ffdf00", "name": "06:00–12:00 (Morning)"},
        {"color": "#4daf4a", "name": "12:00–18:00 (Afternoon)"},
        {"color": "#377eb8", "name": "18:00–24:00 (Evening)"},
        {"color": "black", "name": "Date Marker (Dot)", "mode": "markers"},
        {"color": "black", "name": "Feeding Duration (Line)", "mode": "lines"},
    ]

    for item in legend_items:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode=item.get("mode", "lines"),
            line=dict(color=item["color"], width=3) if item.get("mode", "lines") == "lines" else None,
            marker=dict(color=item["color"], size=8) if item.get("mode", "lines") == "markers" else None,
            name=item["name"],
            showlegend=True
        ))

    fig.update_layout(
        title=f"Currently selected: Pig {selected_pig} in Feeding Station {selected_station}",    
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=800,
        width=900,
        plot_bgcolor="white",
        legend=dict(
            title="Legend",
            orientation="v",
            x=1.05,
            y=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        )
    )

    fig.show()
    mo.output.append(fig)
    return fig1, item, legend_items


if __name__ == "__main__":
    app.run()
