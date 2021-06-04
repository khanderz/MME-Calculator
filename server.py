"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"

#app routes and view functions
@app.route('/')
def homepage():
    """view homepage"""

    return render_template('homepage.html') 

@app.route('/results')
def addMed():

    drug = request.args.get('drug')
    dose = request.args.get ('dose')
    quantity = request.args.get('quantity')
    days_supply = request.args.get('days_supply')

    MME = crud.calculate_MME(drug=drug, dose=dose, quantity=quantity, days_supply=days_supply) 

    return render_template('results.html', drug=drug, dose=dose, quantity=quantity, days_supply=days_supply, MME=MME)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
