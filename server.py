"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, User, Med, Opioid
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
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    # drug = ""

    # drug_dose = ""
    # quantity = ""
    # days_supply = ""

    # MME = ""

    # return render_template('homepage.html', user=user, drug=drug, drug_dose=drug_dose, quantity=quantity, days_supply=days_supply, MME=MME)  
    return render_template('homepage.html', user=user)

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
    
    print(user, '****** USER ******')
    print(user.med_list, '***** USER.MEDLIST **********')

    return render_template('user_details.html', user=user)  

# MME and drug routes
@app.route('/results')
def addMed():
    """ add med for non-logged in users"""

    drug = request.args.get('drug')
    dose = decimal.Decimal(request.args.get('dose'))
    quantity = decimal.Decimal(request.args.get('quantity'))
    days_supply = decimal.Decimal(request.args.get('days_supply'))

    print('^^^^^^^^^^', drug, dose, quantity, days_supply, '^^^^^^^^^^')

    MME = float(crud.calculate_MME(drug=drug, dose=dose, quantity=quantity, days_supply=days_supply)) 

    print(MME, '********** MME *************')


    return jsonify({'MME': MME})
    # return render_template('homepage.html', MME=MME) 
    # return MME
    # return render_template('homepage.html')

@app.route('/add', methods=['POST'])
def add():
    """Add new `Med` to user.med_list"""
    if "user_id" in session:
    # Query for logged in `User` obj from db
        user = User.query.get(session['user_id'])
        print(user, '********** USER ************')

    # Query for `Opioid` from db, by drug name (from request.form)
        drug = request.form.get('drug')
        opioid = crud.get_opioid_by_name(opioid_name=drug)
    
        print(drug, '&&&&&&&& drug &&&&&&&&&&')
        print(opioid, '^^^^^^^^^^ OPIOID  ^^^^^^^^^^^^^^^')

    # Create `Med` object, `Med` attributes:
    # drug_dose = db.Column(db.Integer)
    # quantity = db.Column(db.Integer)
    # days_supply = db.Column(db.Integer)
    # daily_MME = db.Column(db.Integer)  

        drug_dose = decimal.Decimal(request.form.get('dose', 0))
        quantity = decimal.Decimal(request.form.get('quantity', 0))
        days_supply = decimal.Decimal(request.form.get('days_supply', 0))
        print(drug_dose, quantity, days_supply, '#######FORM INPUT#######')

        MME = crud.calculate_MME(
            drug=drug,
            dose=drug_dose,
            quantity=quantity,
            days_supply=days_supply,
        )

        print(MME, '######### MME #############')

        crud.add_opioid_to_user_medlist(
            user,
            opioid,
            drug_dose,
            quantity,
            days_supply,
            MME
        )

        print(user.med_list, user, '*********** user.med_list *********')

        # db.session.add(user)
        # db.session.commit()

        # return redirect to homepage
        return jsonify({'msg': 'medication added',}), 200
        # ('homepage.html', user=user, drug=drug, drug_dose=drug_dose, quantity=quantity, days_supply=days_supply, MME=MME)  
    else:
        return jsonify("unauthorized")

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
