# Chicago Taxi Trips Streaming Analysis with Real Time Dashboard

In this project, we have analyzed the infamous 
[Chicago City Taxi Trips](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) 
dataset using Spark Structured Streaming, and also built a dashboard for reporting the metrics using Flask and HTML.
The dataset itself is open for public use and holds information since 2013, amounting to about 200 Million rows with 
each record being around 1024 bytes in size.

## Features
Here are some features of this implementation:
- Retrieves data from a folder and process them in a streaming fashion.
- A full-fledged dashboard built using Flask and Chart JS to visualize the metrics.
- Uses Spark to support big data analysis, tested on more than 100 million records.
- Uses Structured Streaming and therefore can easily be ported for any similar use case.

## Problem Statements
<ol>
<li> Rate of tipping over years? </li>
<li> Popular taxi trips days? </li>
<li> Mode of payment over years? </li>
<li> Total miles travelled across years? </li>
<li> Total time travelled across years? </li>
<li> Which company makes the most trips per year? </li>
</ol>

## Implementation
![High Level Design](Documents/Implementation%20HLD.png?raw=true "High Level Design")

## Folder Structure
    ├── Documents                                   # Holds info about the project
    ├── dashboard                                   # Code for the Flask application
    │   ├── static                                      # Holds static files associated with the dashboard
    │   │   ├── css                                         # Holds styling files for the dashboard
    │   │   └── js                                          # Holds javascript files used for the dashboard
    │   ├── templates                                   # Holds the HTML template used for the dashboard UI
    │   └── app.py                                      # Flask application which defines and triggers the endpoints; startpoint for the dashboard
    ├── source                                      # Source folder for the streaming application
    │   └── 1.csv                                       # A sample source file
    ├── README.md                                   # Read this first
    └── streaming.py                                # Streaming application which reads the files and executes operations in PySpark using Structured Streaming

## Output
![Dashboard Screenshot](Documents/Dashboard%20Image.png?raw=true "Dashboard Screenshot")

https://user-images.githubusercontent.com/21313710/137774469-e0ea2857-de4e-4256-bb38-7007ba338b37.mp4

## Contributors
- [Jacob Celestine](https://jacobcelestine.com/)
- [Harsh Patel](https://github.com/hkp98)
- [Pulak Raj](https://github.com/PulakRaj)
