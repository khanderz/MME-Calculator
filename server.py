"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import crud
import decimal
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

    # if session:
    #     session["user_drug"] = user.drug
    #     session["user_dose"] = user.dose
    #     session["user_quantity"] = user.quantity
    #     session["user_days_supply"] = user.days_supply
    #     session["user_MME"] = user.MME
    #     print("~"*20)
    #     print(session)
    

    return jsonify({'MME': MME})
    # return render_template('homepage.html', MME=MME) 
    # return MME

@app.route('/add', methods=['POST'])
def add():
    """Add new `Med` to user.med_list"""
    
    # Query for logged in `User` obj from db
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email) 

    # Query for `Opioid` from db, by drug name (from request.form)
    drug = request.form.get('drug')
    opioid = crud.get_opioid_by_name(opioid_name=drug)
    
    # Create `Med` object, `Med` attributes:
    # drug_dose = db.Column(db.Integer)
    # quantity = db.Column(db.Integer)
    # days_supply = db.Column(db.Integer)
    # daily_MME = db.Column(db.Integer)  

    drug_dose = decimal.Decimal(request.args.get('dose', 0))
    quantity = decimal.Decimal(request.args.get('quantity', 0))
    days_supply = decimal.Decimal(request.args.get('days_supply', 0))

    MME = crud.calculate_MME(
        drug=opioid,
        dose=drug_dose,
        quantity=quantity,
        days_supply=days_supply,
    )

    new_med = crud.add_med_to_med_list(
        drug_dose=drug_dose, 
        quantity=quantity, 
        days_supply=days_supply, 
        daily_MME=MME,
    )
    
    # user.med_list.append(new_med)
    user.med_list.append(new_med)
    
    # return redirect to homepage
    # return redirect('/') 
    return render_template('homepage.html', drug=drug, drug_dose=drug_dose, quantity=quantity, days_supply=days_supply, MME=MME)  


@app.route('/api/calculate-mme')
def calculate_mme():
    drug = request.args.get('drug')

    dose = decimal.Decimal(request.args.get('dose', 0))
    quantity = decimal.Decimal(request.args.get('quantity', 0))
    days_supply = decimal.Decimal(request.args.get('days_supply', 0))
   
    MME = crud.calculate_MME(
        drug=drug,
        dose=dose,
        quantity=quantity,
        days_supply=days_supply,
    )

    return jsonify({'value': float(MME)})

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
