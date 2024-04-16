# ////////////////////// to run this code first execute this code ////////////////////////////////
# pip install -r requirements.txt 
# than this code 
# python server.py
# ////////////////////////////////////////////////////////////////////
from flask import Flask, render_template, request, redirect, url_for ,jsonify
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
# Function to read users from CSV
def read_users_from_csv(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users
def write_expenses_to_csv(expenses, file_path):
    fieldnames = ["username", "individual_expense", "shared_expense", "shared_with", "cost"]
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)
# Function to write user to CSV
def write_user_to_csv(user, file_path):
    fieldnames = ["username", "email", "password"]  # Define field names
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # Check if file is empty
            writer.writeheader()  # Write header if file is empty
        writer.writerow(user)

# Function to read expenses from CSV
def read_expenses_from_csv(file_path):
    expenses = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)
    return expenses

# Function to write expense to CSV
def write_expense_to_csv(expense, file_path):
    fieldnames = ["username", "individual_expense", "shared_expense", "shared_with", "cost"]
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(expense)

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        users = read_users_from_csv("users.csv")
        for user in users:
            if user['username'] == username or user['email'] == email:
                return "Username or email already exists!"
        
        # If username and email are unique, add the new user
        new_user = {"username": username, "email": email, "password": password}
        write_user_to_csv(new_user, "users.csv")
        return "Signup successful!"
    
    return render_template('signup.html')

@app.route('/expenses')
def expenses():
    expenses_data = read_expenses_from_csv("expenses.csv")
    return render_template('expenses.html', expenses=expenses_data)
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        username = request.form['username']
        individual_expense = request.form['individual_expense']
        shared_expense = request.form['shared_expense']
        shared_with = request.form.getlist('shared_with')  # Get list of selected users
        cost = request.form['cost']
        
        # Create expense dictionary
        new_expense = {
            "username": username,
            "individual_expense": individual_expense,
            "shared_expense": shared_expense,
            "shared_with": shared_with,
            "cost": cost
        }
        
        # Write expense to CSV
        write_expense_to_csv(new_expense, "expenses.csv")
        
        # Redirect to expenses page
        return redirect(url_for('expenses'))
    
    # Read users from CSV
    users = read_users_from_csv("users.csv")
    
    return render_template('add_expense.html', users=users)
# Route for deleting expenses
@app.route('/delete_expenses', methods=['POST'])
def delete_expenses():
    selected_expenses = request.form.getlist('selected_expenses')  # Get list of selected expense usernames
    expenses = read_expenses_from_csv("expenses.csv")
    
    # Filter out selected expenses
    expenses = [expense for expense in expenses if expense['username'] not in selected_expenses]
    
    # Write updated expenses to CSV
    write_expenses_to_csv(expenses, "expenses.csv")
    
    # Redirect back to expenses page
    return redirect(url_for('expenses'))
if __name__ == '__main__':
    app.run(debug=True)
