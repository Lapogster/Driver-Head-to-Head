# Teammate Head-to-Head Comparison

## Program Overview
An analysis tool for comparing the seasons of all drivers on a team over a season, comparing points scored over the season for insights into teammate competitiveness.

## Setup
It is recommended to use a virtual environment when running the program, to set this up run <br>
`python3 -m venv .venv` <br>then <br>`source .venv/bin/activate` <br>(`.venv\scripts\activate` on windows)
<br>
### To install the required dependencies run <br>
`pip install -r requirements.txt`

## Usage
To run the program use a terminal in the root folder and run<br>
### `streamlit run app.py`<br>
Use the dropdown to select a season and then choose a team, the data for all drivers who raced for them that year will be displayed.<br>
Note: the first load of any season or team may take a few moments, all subsequent loads will be faster
