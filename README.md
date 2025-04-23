# [G0R72a] Data Visualization for Data Science: <br> Project 1 - Data visualization for "exploration"

## Overview
This project is part of the course **"[G0R72a] Data Visualization for Data Science"** at KU Leuven. This first project focuses on data visualization for "exploration".

## Tools and Technologies
The repository has three [Marimo](https://marimo.io/) notebooks that contain the visualizations for the project. Visualizations were made using Python, HTML, CSS and JavaScript.
1. pigplot.py
2. network.py
3. feeding.py

## Dataset
We use the [Pig Feed Data](https://data.mendeley.com/datasets/2mbw72m3g8/1): *“Exp1 (dec2020-feb2021)/Exp1 - Feeding data.csv”*. These data were collected as part of the [ClearFarm](https://www.clearfarm.eu/) project and monitored the eating behaviors of growing-finishing pigs using electronic feeding stations. The feeding data contain the following features:
- **date**: The date of the feeder visit (day/month/year)
- **pig**: The pig ID of the pig visiting the feeder (12 digits)
- **station**: The station ID of the station that recorded the visit (1-10)
- **weight_start**: The weight of the food in the feeder at the start of the visit (kg)
- **weight_end**: The weight of the food in the feeder at the end of the visit (kg)
- **intake**: The difference between ‘weight_end’ and ‘weight_start’ (kg)
- **start**: The time when the visit started (day/month/year hour:minute:second)
- **end**: The time when the visit ended (day/month/year hour:minute:second)
- **hour**: The hour within which the visit started (0-23)
- **duration**: The time difference between ‘end’ and ‘start’ (s)
- **rate**: The ‘intake’ divided by ‘duration’, multiplied by 1000 (kg/s)

Note that each station (1-10) serves 11 pigs. Each pig is expected to eat at the same station every time.

## Visualizations
1. [pigplot.html](https://yokie0105.github.io/data-visualization-project-1/apps/pigplot.html)
2. [network.html](https://yokie0105.github.io/data-visualization-project-1/apps/network.html)
3. [spiral.html](https://yokie0105.github.io/data-visualization-project-1/apps/spiral.html)

## Contributors
- Oscar
- Sarah 
- Marte