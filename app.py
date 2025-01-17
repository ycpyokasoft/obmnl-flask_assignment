# Import libraries
from flask import Flask, request, url_for, redirect, render_template
from random import randint

# Instantiate Flask functionality
app = Flask("__name__")

# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        transaction = {
            'id': randint(1000,9999),
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }

        transactions.append(transaction)

        return redirect(url_for("get_transactions"))
    else:
        return "ERROR: Invalid method: " + request.method, 500
       
# Update operation
@app.route('/edit/<int:transaction_id>', methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # If 'GET', then find the transaction with that ID and display it
    if request.method == "GET":
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template("edit.html", transaction=transaction)
        return {"message": "Transaction not found"}, 404
    elif request.method == "POST":
        date = request.form['date']
        amount = request.form['amount']
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                return redirect(url_for("get_transactions"))
        return {"message": "Transaction not found"}, 404
    else:
        return "ERROR: Invalid method: " + request.method, 500
    
# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            return redirect(url_for("get_transactions"))
    return {"message": "Transaction not found"}, 404

# Search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = request.form['min_amount']
        max_amount = request.form['max_amount']

        filtered_transactions = []
        for transaction in transactions:
            if float(min_amount) <= float(transaction['amount']) <= float(max_amount):
                filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions=filtered_transactions)
    elif request.method == "GET":
        return render_template("search.html")
    else:
        return {"message": "Invalid method - " + request.method}
    
@app.route("/balance")
def total_balance():
    total = 0
    for transaction in transactions:
        total += float(transaction['amount'])
    return render_template("transactions.html", balance=f"Total Balance: {total}")

# Run the Flask app
if __name__ == "__main__":
    app.run(host="localhost", debug=True)