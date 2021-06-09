"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

#app routes and view functions
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html') 

# User routes
@app.route('/user_reg', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("""Could not create account because an account with this email already
               exists. Please try again.""")
    else:
        crud.create_user(email, password)
        flash("Account created successfully! Please log in.")

    return redirect('/') 

@app.route('/user_login', methods=['POST'])
def login():
    """Allow existing users to log in."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email_and_password(email, password)

    print("~"*20)
    print(session)

    if user:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        print("~"*20)
        print(session)
        flash(f"Hello {user.email}! You are now logged in.")
    else:
        flash("Please enter the correct email and password or create a new account.")

    return redirect('/')

@app.route('/logout')
def logout():
    """Allow a logged in user to logout."""

    print("~"*20)
    print(session)

    if session:
        session.pop("user_id")
        session.pop("user_email")
        print("~"*20)
        print(session)
        flash("You are now logged out.")

    else:
        flash("You are not currently logged in.")
    
    return redirect('/')   

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details of a particular user"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)  

# MME and drug routes
@app.route('/results')
def addMed():

    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)    

    drug = request.args.get('drug')
    dose = request.args.get ('dose')
    quantity = request.args.get('quantity')
    days_supply = request.args.get('days_supply')

    MME = float(crud.calculate_MME(drug=drug, dose=dose, quantity=quantity, days_supply=days_supply)) 

    if session:
        session["user_drug"] = user.drug
        session["user_dose"] = user.dose
        session["user_quantity"] = user.quantity
        session["user_days_supply"] = user.days_supply
        session["user_MME"] = user.MME
    

    return jsonify({'MME': MME})
    # return render_template('homepage.html', MME=MME) 

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
