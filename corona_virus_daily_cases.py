
import requests
import urllib
import csv
import os
import time
import datetime



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
            print("The most recent available data has been downloaded")
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
        print("The new data has been downloaded")




def country_choice_and_cumulative_or_daily_cases():
    """ 
    Ask the user what country to see the data from
    Ask the user if they would like to see cumulative/daily cases
    """
    
    # Open the CSV, obtain headers
    filename = 'coronavirus_data.csv'
    with open(filename) as f:
        reader = csv.reader(f)
    
        # Ask the user what country they would like to see
        user_input_country = input(
            "Which country would you like to see data about? - "
        )

        header_row = next(reader)
        # Print out header rows
        for index, column_header in enumerate(header_row):
            print(f"{index} - {column_header.title().replace('_', ' ')}")

        user_input_statistic = input(
        "Which statistic would you like to see data about? "
            "(See above, type the appropriate number) - "
        )


    



def create_x_and_y_values():
    """ Generate x, y lists from CSV data """

def plot_graph():
    """ Plot the graph """

get_covid_data()
country_choice_and_cumulative_or_daily_cases()