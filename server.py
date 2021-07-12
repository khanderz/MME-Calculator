"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify, Markup)
from model import connect_to_db, db, User, Med, Opioid
import crud
import decimal
from jinja2 import StrictUndefined
from datetime import date, datetime, timedelta
import bcrypt
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

DATE_FORMAT = '%Y-%m-%d'

# flask_mail parameters
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "mmecalc@gmail.com"
app.config['MAIL_PASSWORD'] = "mmecalculation"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# create Mail class instance
mail = Mail(app)


#app routes and view functions
@app.route('/')
def homepage():
    """View homepage."""

    # temporary flash
    flash(Markup('New security measures have been implemented on July 10, 2021. Please change your password <a href="/change_pw_page">here</a>.'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('homepage.html', user=user, user_id=user_id)


@app.route('/about')
def about_page():
    """View about page."""

    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('resources.html', user=user, user_id=user_id)


@app.route('/updates')
def updates_page():
    """View updates page."""

    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('updates.html', user=user, user_id=user_id)

@app.route('/contact')
def contacts_page():
    """Render contacts page."""

    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('contact.html', user=user, user_id=user_id)


@app.route('/message_page')    
def render_message_page():
    """Render message page"""

    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('message.html', user=user, user_id=user_id) 

@app.route('/message', methods=['POST'])
def send_message():
    """Send message"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    # message_type = request.form.get("message_type")
    message = request.form.get("message")
    print(first_name, last_name, email, message, "*******user inputs")

    msg = Message(sender = email, recipients = ['mmecalc@gmail.com'])
    msg.body = "Message from" + " " + first_name + " " + last_name + " " + email + " " + "message:" + " " + message
    mail.send(msg)

    flash('Message submitted.')
    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('message.html', user=user, user_id=user_id) 


# User routes
@app.route('/create_user')
def render_create_user():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    return render_template('create_account.html', user_id=user_id)


@app.route('/user_reg', methods=['POST'])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    pw1 = request.form.get("password1").encode('utf-8')
    pw2 = request.form.get("password2").encode('utf-8')

    if pw1 == pw2:
        password_encoded = bcrypt.hashpw(pw1, bcrypt.gensalt())
        # turn hashed password back into string to be stored in db
        password = password_encoded.decode('utf-8')

        user = crud.get_user_by_email(email)

        crud.create_user(email, password)

        user_id = session.get('user_id')
        user = User.query.get(user_id)
            
        flash("Account created successfully! Please log in.")
        return render_template('user_login.html', user_id=user_id)

    else:
        flash('Passwords do not match. Please try again.')
        user = crud.get_user_by_email(email)
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        return render_template('create_account.html', user_id=user_id)
        


@app.route('/login_page')
def render_login_page():

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        flash(f"Hello {user.email}! You are already logged in.")
    
    return render_template('user_login.html', user_id=user_id)    


@app.route('/user_login', methods=['POST'])
def login():
    """Allow existing users to log in."""

    email = request.form.get("email")
    pw = request.form.get("password").encode("utf-8")

    user_password = crud.get_user_password(email)

    hashed2 = bcrypt.hashpw(pw, user_password.encode('utf-8'))
    hashed2_str = hashed2.decode('utf-8')

    if hashed2_str == user_password:
        print("Password match!")
        # Log the user in ...

        user = crud.get_user_by_email_and_password(email, hashed2_str)

        # chart descriptions
        today = date.today()
        ago = today - timedelta(days=7)
        month = today.strftime("%B")


        session["user_email"] = user.email
        session["user_id"] = user.user_id
        flash(f"Hello {user.email}! You are now logged in.")
        return render_template('user_details.html', user=user, user_id=user.user_id, ago=ago, today=today, month=month) 

    else:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        flash("Please enter the correct email and password or create a new account.")
        return render_template('user_login.html', user_id=user_id)


@app.route('/logout')
def logout():
    """Allow a logged in user to logout."""

    if session:
        session.pop("user_id")
        session.pop("user_email")
        flash("You are now logged out.")

    else:
        flash("You are not currently logged in.")
    
    return redirect('/')   


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details of a particular user"""
    if "user_id" in session:
        user = crud.get_user_by_id(user_id)
        

        # chart descriptions
        today = date.today()
        ago = today - timedelta(days=7)
        month = today.strftime("%B")

        return render_template('user_details.html', user=user, user_id=user_id, ago=ago, today=today, month=month)  
    else:
        flash("You are not currently logged in. Please login to view your dashboard.")
    
    return redirect('/')    


@app.route('/reset_page')
def render_reset_page():
    """Render reset password page"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    return render_template('reset.html', user_id=user_id)


@app.route('/reset', methods=['POST'])
def reset_password(user):
    """Reset user password"""    

    pass


@app.route('/change_pw_page')
def render_change_pw_page():
    """Render change password page"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    return render_template('change_password.html', user_id=user_id)

@app.route('/change_pw', methods=['POST'])
def change_password():
    """Check old password and change it to new password"""
    email = request.form.get("email")
    old_password = request.form.get("old_pw")
    new_password = request.form.get("new_pw").encode('utf-8')
    new_password2 = request.form.get("new_pw2").encode('utf-8')

    user_old_password = crud.get_user_password(email)

    if user_old_password == old_password:
        print("%%%%%%%%%%%%%%%%%passwords match!%%%%%%%%%%%%%%")
        
        if new_password == new_password2:
            password_encoded = bcrypt.hashpw(new_password, bcrypt.gensalt())
            password = password_encoded.decode('utf-8')

            user = crud.get_user_by_email(email)

            crud.change_user_password(email, password)

            user_id = session.get('user_id')
            user = User.query.get(user_id)

            flash('Password changed successfully. Please log in.')
            return render_template('user_login.html', user_id=user_id)

        else:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
            flash('New passwords do not match. Please try again.')
            return render_template('change_password.html', user_id=user_id) 

    else:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        flash("Please enter the correct email and old password")
        return render_template('change_password.html', user_id=user_id)   



# MME and drug routes
@app.route('/results')
def addMed():
    """ add med for non-logged in users"""

    drug = request.args.get('drug')   
    dose = decimal.Decimal(request.args.get('dose'))
    quantity = decimal.Decimal(request.args.get('quantity'))
    days_supply = decimal.Decimal(request.args.get('days_supply'))
    date_filled = request.args.get('date_filled', 0)


    MME = float(crud.calculate_MME(drug=drug, dose=dose, quantity=quantity, days_supply=days_supply)) 


    return jsonify({'MME': MME})


@app.route('/add', methods=['POST'])
def add():
    """Add new `Med` to user.med_list"""

    if "user_id" in session:
    # Query for logged in `User` obj from db
        user = User.query.get(session['user_id'])

    # Query for `Opioid` from db, by drug name (from request.form)
        drug = request.form.get('drug')
        opioid = crud.get_opioid_by_name(opioid_name=drug)

    # Create `Med` object, `Med` attributes:
    # drug_dose = db.Column(db.Integer)
    # quantity = db.Column(db.Integer)
    # days_supply = db.Column(db.Integer)
    # daily_MME = db.Column(db.Integer)  

        drug_dose = decimal.Decimal(request.form.get('dose', 0))
        quantity = decimal.Decimal(request.form.get('quantity', 0))
        days_supply = decimal.Decimal(request.form.get('days_supply', 0))

        date_filled = None
        if request.form.get('date_filled', None) != "": 
            date_filled = request.form.get('date_filled', None)


        MME = crud.calculate_MME(
            drug=drug,
            dose=drug_dose,
            quantity=quantity,
            days_supply=days_supply,
        )

        crud.add_opioid_to_user_medlist(
            user,
            opioid,
            drug_dose,
            quantity,
            days_supply,
            MME,
            date_filled,
        )


        return jsonify({'msg': 'medication added',}), 200
    else:
        return jsonify("unauthorized")
        

@app.route('/api/med_list')
def get_users_med_list():
    """Get currently logged in user's med list.

    Can filter by date range.
    """
    
    date_filled = request.args.get('date_filled')
    end_date = request.args.get('end_date')
    
    if date_filled:
        date_filled = datetime.strptime(date_filled, DATE_FORMAT).date()

    if end_date:
        end_date = datetime.strptime(end_date, DATE_FORMAT).date()
    
    # Get currently logged in user
    if 'user_id' in session:
        # user = User.query.options(
        #     db.joinedload('med_list')
        # ).get(session['user_id'])
        user = User.query.get(session['user_id'])

        today = date.today()
        ago = today - timedelta(days=7)

        filtered_med_list = Med.query.filter(
                            Med.date_filled != None, 
                            Med.user_id== user.user_id,
                            ).all()


        if date_filled and end_date:
            med_list = user.get_meds_by_date_range(
                date_filled=date_filled,
                end_date=end_date
            )
        else:
            med_list = filtered_med_list
        
        med_list_json = []
        
        for med in med_list:
            med_list_json.append({
                'med_id': med.med_id,
                'user_id': med.user_id,
                'opioid': {
                    'opioid_name': med.opioid.opioid_name,
                    'conversion_factor': float(med.opioid.conversion_factor),
                },
                'drug_dose': med.drug_dose,
                'quantity': med.quantity,
                'days_supply': med.days_supply,
                'date_filled': med.date_filled.strftime(DATE_FORMAT), 
                'end_date': med.end_date.strftime(DATE_FORMAT),
                'daily_MME': float(med.daily_MME),
            })


        return jsonify(med_list_json)            
            


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=False)
