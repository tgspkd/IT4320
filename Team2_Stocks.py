from multiprocessing.sharedctypes import Value
from time import strptime
import requests
# import alpha_vantage
from datetime import datetime
import pygal
import json

#NOTE: API KEY = 4NJ262WL2WQKBMQ1

# Set Global Values
stock_symbol = "IBM"
chart_type = "Bar"
time_series_function = "TIME_SERIES_INTRADAY"
date_format = "%Y-%m-%d"
time_format = "%Y-%m-%d %H:%M:%S"
beginning_date = "2020-01-01"
end_date = "2020-01-10"
datetime_beginning_date = 1
datetime_end_date = 1

def Startup():
    global stock_symbol
    global chart_type
    global time_series_function
    global date_format
    global beginning_date
    global end_date
    global datetime_beginning_date
    global datetime_end_date
    # Get Stock Symbol
    stock_symbol = input("Please enter the Stock Symbol for the Company you want Data from:")
    # Get Chart Type
    print("Chart Types")
    print("-----------")
    print("1. Bar")
    print("2. Line")
    while(True):
        choice = input("Please enter the Chart Type you would like (1, 2):")
        if choice == "1":
            chart_type = "Bar"
            break
        elif choice == "2":
            chart_type = "Line"
            break
        else:
            print("Please enter a 1 or a 2.")
            continue
    # Get Time Series Function
    print("Time Series Types")
    print("-----------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")
    # Get Time Series Function
    while(True):
        choice = input("Please enter the Time Series Function you would like the API to use (1, 2, 3, 4):")
        if choice == "1":
            time_series_function = "TIME_SERIES_INTRADAY"
            break
        elif choice == "2":
            time_series_function = "TIME_SERIES_DAILY"
            break
        elif choice == "3":
            time_series_function = "TIME_SERIES_WEEKLY"
            break
        elif choice == "4":
            time_series_function = "TIME_SERIES_MONTHLY"
            break
        else:
            print("Please enter a 1, 2, 3, or 4")
            continue
    # Get Beginning Date
    while(True):
        while(True):
            try:
                beginning_date = input("Please enter the beginning date in YYYY-MM-DD format:")
                datetime_beginning_date = datetime.strptime(beginning_date, date_format)
                # print(datetime_beginning_date)
            except ValueError:
                print("This is an invalid date. Please enter the date in the correct format.")
                continue
            break
    
        # Get End Date
        while(True):
            try:
                end_date = input("Please enter the end date in YYYY-MM-DD format:")
                datetime_end_date = datetime.strptime(end_date, date_format)  
                # print(datetime_end_date)  
            except ValueError:
                print("This is an invalid date. Please enter the date in the correct format.")
                continue  
            break
        if (datetime_beginning_date < datetime_end_date):
            break
        elif (datetime_beginning_date >= datetime_end_date):
            print("The end date must be after the beginning date. Please enter the dates again.")
            continue

def Get_Info():
    if time_series_function == "TIME_SERIES_INTRADAY":
        url = 'https://www.alphavantage.co/query?function=' + time_series_function + '&symbol=' + stock_symbol + '&interval=60min&apikey=4NJ262WL2WQKBMQ1'
    elif time_series_function == "TIME_SERIES_DAILY":
        url = 'https://www.alphavantage.co/query?function=' + time_series_function + '&symbol=' + stock_symbol + '&outputsize=full&apikey=4NJ262WL2WQKBMQ1'
    elif time_series_function == "TIME_SERIES_WEEKLY":
        url = 'https://www.alphavantage.co/query?function=' + time_series_function + '&symbol=' + stock_symbol + '&apikey=4NJ262WL2WQKBMQ1'
    elif time_series_function == "TIME_SERIES_MONTHLY":
        url = 'https://www.alphavantage.co/query?function=' + time_series_function + '&symbol=' + stock_symbol + '&apikey=4NJ262WL2WQKBMQ1'
    # Return information from url
    r = requests.get(url)
    data = r.json()
    # Iterate through dictionary, generate lists for each graph value
    if time_series_function == "TIME_SERIES_INTRADAY":
        keystring = "Time Series (60min)"
    elif time_series_function == "TIME_SERIES_DAILY":
        keystring = "Time Series (Daily)"
    elif time_series_function == "TIME_SERIES_WEEKLY":
        keystring = "Weekly Time Series"
    elif time_series_function == "TIME_SERIES_MONTHLY":
        keystring = "Monthly Time Series"
    x_axis_values = []
    open_values = []
    for value in data[keystring]:
        if(datetime.strptime(value[0:10], date_format) >= datetime_beginning_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            # This is only needed for one data category to populate the x-axis labels
            x_axis_values.append(value)
            open_values.append(float(data[keystring][value]['1. open']))
    high_values = []
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_beginning_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            high_values.append(float(data[keystring][value]['2. high']))
    low_values = []
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_beginning_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            low_values.append(float(data[keystring][value]['3. low']))
    close_values = []
    for value in data[keystring]:
        if (datetime.strptime(value[0:10], date_format) >= datetime_beginning_date and datetime.strptime(value[0:10], date_format) <= datetime_end_date):
            # x_axis_values.append(value)
            close_values.append(float(data[keystring][value]['4. close']))

    print(x_axis_values)
    print(open_values)
    print(high_values)
    print(low_values)
    print(close_values)
    
    # Using "Basic" line graph from pygal
    if chart_type == "Bar":
        if time_series_function == "TIME_SERIES_INTRADAY":
            api_chart = pygal.Bar()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_DAILY":
            api_chart = pygal.Bar()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_WEEKLY":
            api_chart = pygal.Bar()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_MONTHLY":
            api_chart = pygal.Bar()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
    if chart_type == "Line":
        if time_series_function == "TIME_SERIES_INTRADAY":
            api_chart = pygal.Line()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_DAILY":
            api_chart = pygal.Line()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_WEEKLY":
            api_chart = pygal.Line()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
        elif time_series_function == "TIME_SERIES_MONTHLY":
            api_chart = pygal.Line()
            api_chart.title = "Stock data for " + stock_symbol + ": " + beginning_date + " - " + end_date
            api_chart.x_labels = x_axis_values
            


    api_chart.add("Open", open_values)
    api_chart.add("High", high_values)
    api_chart.add("Low", low_values)
    api_chart.add("Close", close_values)
    api_chart.render_in_browser()
    return 0
      
        
def main():
    do_another = True
    while(do_another):
        print("Stock Data Visualizer\n")
        print("-----------------------")

        Startup()
        Get_Info()
        
        restart = input("Would you like to view more stock data? (y/n)")
        if(restart != "y"):
            do_another = False
    
main()