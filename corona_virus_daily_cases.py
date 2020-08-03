
import requests
import urllib
import csv
import os
import time
import datetime

import plotly.express as px
import plotly as py
import plotly.graph_objs as go


def get_covid_data():
    """ Obtain newest CSV of Covid-19 Data """
    # Assign URL for the data, and the filename once downloaded
    url = ("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    filename = 'coronavirus_data.csv'

    # Check if file exists
    if os.path.exists('coronavirus_data.csv'):
        # Check if file is up to date (Not modified within 6 hours)
        statbuf = os.stat(filename)
        modified_time = statbuf.st_mtime
        current_time = int(time.time())
        time_since_modification = (((current_time-modified_time)/60)/60)

        # Download fresh data
        if time_since_modification > 6:
            urllib.request.urlretrieve(url, 'coronavirus_data.csv')
            print("The most recent available data has been downloaded.")
        else:
            # Convert unix timestamp of modified file to readable format
            formatted_m_time = datetime.datetime.fromtimestamp(
                modified_time).strftime(
                    '%Y-%m-%d %H:%M:%S'
                )
            print(f"The data is up to date as of {formatted_m_time}")
    else:
        # Obtain data for the first time
        urllib.request.urlretrieve(url, 'coronavirus_data.csv')
        print("Your data has been downloaded.")

def country_choice_and_cumulative_or_daily_cases():
    """ 
    Ask the user what country to see the data from
    Ask the user if they would like to see cumulative/daily cases
    """

    # Ask the user what country they would like to see
    user_input_country = input(
        "Which region would you like to see data about?"
        " (world statistics are also available)  - "
    )

    # Open the CSV, obtain headers
    filename = 'coronavirus_data.csv'
    with open(filename) as f:
        reader = csv.reader(f)

        # Print out header rows
        header_row = next(reader)
        for index, column_header in enumerate(header_row):
            print(f"{index} - {column_header.title().replace('_', ' ')}")

        # Ask what statistic they would like to see data for
        user_input_stat = input(
            "Which statistic would you like to see data about? "
            "(See above, type the appropriate number) - "
        )

        # Append region's data to a new list
        selected_region = []
        for row in reader:
            if user_input_country.title() in row:
                selected_region.append(row)

        # Append the users chosen dataset to a new list
        stat_data = []
        for chosen_statistic in selected_region:
            stat_data.append(chosen_statistic[int(user_input_stat)])
        
        # Append the corresponding dates to the data
        stat_dates = []
        for dates in selected_region:
            stat_dates.append(dates[3])
        
    return stat_dates, stat_data

def plot_graph():
    """ Plot the graph """

    dataset = country_choice_and_cumulative_or_daily_cases()
    trace_1 = {
        "x": dataset[0],
        "y": dataset[1],
        "line": {
            "color": "#385965", 
            "width": 1.5,
        },
        "mode": "lines",
        "name": "France",
        "type": "scatter",
    }
    layout = {
        "showlegend": True,
        "title": {"text": "New Daily Cases of COVID-19 in France"},
        "xaxis": {
            "rangeslider": {"visible": True},
            "title": {"text": "Date"},
            "zeroline": False,
        },
        "yaxis": {
            "title":{"text": "Number of new cases per day"},
            "zeroline": False,
        },
    }
    
    fig = go.Figure(data = trace_1, layout = layout)
    py.offline.plot(fig, filename="test.html")


plot_graph()