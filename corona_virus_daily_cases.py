
import requests
import urllib
import csv
import os
import time
import datetime

import plotly.express as px
import plotly as py
import plotly.graph_objs as go

rows = []
header_row = []

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

def convert_csv_into_lists():
    """ 
    Convert CSV file into a into to quit out the reading loop
    """
    # Import global variables
    global rows, header_row
    
    # Open the CSV, obtain headers
    filename = 'coronavirus_data.csv'
    with open(filename) as f:
        reader = csv.reader(f)

        # Obtain column headers
        header_row = next(reader)
        
        # Append data to global list, making it accessible outside the function
        for row in reader:
            rows.append(row)
    return
    
def get_countries_and_stats_requested():
    """ 
    Ask the user which countries/statistics they would like to compare
    """
    convert_csv_into_lists()
    # Import global variables
    global rows, header_row

    # Print out the potential statistics to compare
    for index, column_header in enumerate(header_row):
            print(f"{index} - {column_header.title().replace('_', ' ')}")
    # Ask what statistic they would like to see data for
    user_input_stat = input(
        "Which statistic would you like to see data about? "
        "(See above, type the appropriate number) - "
    )
    # Ask the user how many countries they would like to compare
    user_number_of_countries = input(
        "How many countries would you like to compare? (Maximum 5) - "
    )
    # Create dict to store countries data, and a list for corresponding dates
    dict_countries_data = {}
    stat_dates = []
    for dates in rows:
        stat_dates.append(dates[3])

    # Loop over data x amount of the times the user requires
    for num_countries in range(int(user_number_of_countries)):
        # Ask the user which countries they would like to see
        user_input_country = input(
            "Which region would you like to see data about? "
        )
        # Append region's data to a new list
        selected_region = []
        for row in rows:
            if user_input_country.title() in row:
                selected_region.append(row)

        # Append the users chosen dataset to a new list
        stat_data = []
        for chosen_statistic in selected_region:
            stat_data.append(chosen_statistic[int(user_input_stat)])
        
        dict_countries_data[user_input_country.title()] = stat_data
        
    return stat_dates, dict_countries_data

def plot_graph():
    """ Plot the graph """
    dataset = get_countries_and_stats_requested()
    
    # Append data to lists to make them accessible for plotting
    countries = []
    countries_data = []
    for country, data in dataset[1].items():
        countries.append(country)
        countries_data.append(data)

    # for country, data in dataset[1].items():
    for num_countries in range(len(dataset[1])): 
        "x": dataset[0],
        "y": data,
        "line": {
            "color": "#385965", 
            "width": 1.5,
        },
        "mode": "lines",
        "name": country,
        "type": "scatter",
    }

    

    
        


    #     traces.append(x)
    
    # trace_1 = {
    #     "x": dataset[0],
    #     "y": dataset[1],
    #     "line": {
    #         "color": "#385965", 
    #         "width": 1.5,
    #     },
    #     "mode": "lines",
    #     "name": "France",
    #     "type": "scatter",
    # }
    # layout = {
    #     "showlegend": True,
    #     "title": {"text": "New Daily Cases of COVID-19 in France"},
    #     "xaxis": {
    #         "rangeslider": {"visible": True},
    #         "title": {"text": "Date"},
    #         "zeroline": False,
    #     },
    #     "yaxis": {
    #         "title":{"text": "Number of new cases per day"},
    #         "zeroline": False,
    #     },
    # }
    
    # fig = go.Figure(data = data, layout = layout)
    # py.offline.plot(fig, filename="test.html")


# plot_graph()

plot_graph()