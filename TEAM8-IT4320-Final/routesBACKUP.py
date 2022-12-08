from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .flask_wtforms_tutorial.forms import *


@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = AdminLoginForm()
    seat_chart = []
    total_sales = get_sales()
    if request.method == 'POST':
        if form.validate_on_submit():
            # User Authentication (check passcodes.txt)
            username = request.form['username']
            password = request.form['password']
            with open('passcodes.txt') as f:
                if (username + ", " + password) in f.read():
                    err = None
                    # Generate default reservations chart
                    seat_chart = get_reservations()
                    login=True
                else:
                    err = "Error: Username and password are invalid."
                    login=False
                    
            return render_template("admin.html", form=form, template="form-template", err=err, seat_chart=seat_chart, total_sales=total_sales, login=login)
    return render_template("admin.html", form=form, template="form-template")
    


@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    seat_chart = get_reservations()
    prices = get_cost_matrix()
    # Calculate total sales
    total_sales = 0
    confirm = False
    err = None
    # Update seating chart
    if request.method == 'POST':
        if form.validate_on_submit():
            # Choose a seat
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            row = int(request.form['row']) - 1
            seat = int(request.form['seat']) - 1
            ticket = generate_ticket(first_name)

            if seat_chart[row][seat] == "X":
                confirm = True
                err = "This seat is already reserved. Please choose an unoccupied seat."
            # Write new reservation to reservations file
            if err is None:
                with open('reservations.txt','a') as r:
                    confirm = True
                    seat_chart[row][seat] == "X"
                    r.write('\n' + first_name + ", " + str(row) + ", " + str(seat) + ", " + ticket)
               
            return render_template("reservations.html", form=form, template="form-template", err=err, confirm=confirm, seat_chart=seat_chart, ticket=ticket, row=row)
    
    return render_template("reservations.html", form=form, template="form-template", seat_chart=seat_chart)
    

# Function to generate cost matrix for flights
# Input: none
# Output: Returns a 12 x 4 matrix of prices
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

# Function to generate seating chart
def get_reservations():
    seat_chart = [["O","O","O","O"] for x in range(12)]
    reservations = []
    with open('reservations.txt') as r:
        for line in r:
            line = line.rstrip('\n')
            reservations.append((line.split(', ')))

    # Populate seating chart
    for x in reservations:
        seat_chart[int(x[1])][int(x[2])] = "X"
    
    # Send seat_chart back to either admin.html or reservations.html   
    return seat_chart

# Function to generate ticket string
def generate_ticket(first_name):        
    key = "INFOTC1040"
    limiter = ""
    trailing = ""
    ticket = ""
    # Compare string lengths, set range beforehand and determind how many excess characters are in the longer string
    if (len(first_name) <= len(key)):
        limiter = range(len(first_name))
        count = len(key) - len(first_name)
        trailing = key[len(key) - count:]
    elif (len(first_name) > len(key)):
        limiter = range(len(key))
        count = len(first_name) - len(key)
        trailing = first_name[len(first_name) - count:]

    for i in limiter:
        ticket += first_name[i] + key[i]
    ticket += trailing
    return ticket

def get_sales():
    total_sales = 0
    prices = get_cost_matrix()
    seats = get_reservations()
    for x in range(len(seats)):
        for y in range(len(seats[x])):
            if seats[x][y] == "X":
                total_sales += prices[x][y]
    return total_sales