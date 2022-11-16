'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from time import strptime
from multiprocessing.sharedctypes import Value
from datetime import datetime
from datetime import date
import pygal
import json

#NOTE: API KEY = 4NJ262WL2WQKBMQ1

# Set Default Values
# symbol = "IBM"
# chart_type = "Bar"
# time_series = "TIME_SERIES_INTRADAY"
date_format = "%Y-%m-%d"
# time_format = "%Y-%m-%d %H:%M:%S"
# start_date = "2020-01-01"
# end_date = "2020-01-10"
datetime_start_date = 1
datetime_end_date = 1
# keystring = ""

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def Get_Info(symbol, chart_type, time_series, start_date, end_date):
    if time_series[0] == "1":
        keystring = "Time Series (60min)"
    elif time_series[0] == "2":
        keystring = "Time Series (Daily)"
    elif time_series[0] == "3":
        keystring = "Weekly Time Series"
    elif time_series[0] == "4":
        keystring = "Monthly Time Series"
    url = 'https://www.alphavantage.co/query?function=' + time_series + '&symbol=' + symbol[0] + '&interval=60min&apikey=4NJ262WL2WQKBMQ1'
    # Return information from url
    r = requests.get(url)
    data = r.json()
    # Iterate through dictionary, generate lists for each graph value
    x_axis_values = []
    open_values = []
    high_values = []
    low_values = []
    close_values = []
    for value in data[keystring]:
        if(datetime.strptime(value[0:10], date_format) >= datetime_start_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            # This is only needed for one data category to populate the x-axis labels
            x_axis_values.append(value)
            open_values.append(float(data[keystring][value]['1. open']))
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_start_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            high_values.append(float(data[keystring][value]['2. high']))
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_start_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            low_values.append(float(data[keystring][value]['3. low']))
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_start_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            close_values.append(float(data[keystring][value]['4. close']))
    
    # Bar Graph
    if chart_type[0] == "1":
        api_chart = pygal.Bar()
        api_chart.title = "Stock data for " + symbol[0] + ": " + start_date + " - " + end_date
        api_chart.x_labels = x_axis_values
    # Line Graph
    if chart_type[0] == "2":
        api_chart = pygal.Line()
        api_chart.title = "Stock data for " + symbol[0] + ": " + start_date + " - " + end_date
        api_chart.x_labels = x_axis_values
            
    api_chart.add("Open", open_values)
    api_chart.add("High", high_values)
    api_chart.add("Low", low_values)
    api_chart.add("Close", close_values)
    # Return the chart to routes.py
    return api_chart.render_data_uri()





