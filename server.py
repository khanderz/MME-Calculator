"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db, User, Med, Opioid
import crud
import decimal
from jinja2 import StrictUndefined
from datetime import date, datetime, timedelta

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#app routes and view functions
@app.route('/')
def homepage():
    """View homepage."""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
 
    return render_template('homepage.html', user=user, user_id=user_id)

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
    if "user_id" in session:
        user = crud.get_user_by_id(user_id)
        
        print(user, '****** USER ******')
        print(user.med_list, '***** USER.MEDLIST **********')

        return render_template('user_details.html', user=user)  
    else:
        flash("You are not currently logged in.")
    
    return redirect('/')       

# MME and drug routes
@app.route('/results')
def addMed():
    """ add med for non-logged in users"""

    drug = request.args.get('drug')
    dose = decimal.Decimal(request.args.get('dose'))
    quantity = decimal.Decimal(request.args.get('quantity'))
    days_supply = decimal.Decimal(request.args.get('days_supply'))
    date_filled = request.args.get('date_filled', 0)

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

        date_filled = None
        if request.form.get('date_filled', None) != "": 
            date_filled = request.form.get('date_filled', None)

        print(date_filled, '####### DATE FILLED #######')
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
            MME,
            date_filled,
        )

        print(user.med_list, user, '*********** user.med_list *********')

        return jsonify({'msg': 'medication added',}), 200
    else:
        return jsonify("unauthorized")


@app.route('/meds_this_month')
def get_meds_by_date_range():
    """Get med list data by data range search"""

    # call crud function for date range search
    # end date is today
    # date_filled within 7 days ago
    med_list = crud.get_meds_by_date_range(date_filled, end_date)



























# not sure if the following routes are necessary


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


@app.route('/get-seven-day-avg') 
def save_seven_day():
    date = request.args.get('date')
    drug = request.args.get('drug')
    dose = decimal.Decimal(request.args.get('dose'))
    quantity = decimal.Decimal(request.args.get('quantity'))
    days_supply = decimal.Decimal(request.args.get('days_supply'))

    print(date, drug, '@@@@@DATE & DRUG@@@@@')
    print(dose, quantity, days_supply, '@@@@@ dose, quantity, days supply@@@@@')

    MME = crud.calculate_MME(
        drug=drug,
        dose=dose,
        quantity=quantity,
        days_supply=days_supply,
    )

    print(MME, '@@@@@ MME!!!!!!!! @@@@@')

    total = 0
    day_count = 0

    # for i in range(7):
    #     start_date = datetime.strptime(date, "%Y-%m-%d")
    #     end_date = datetime.today() - timedelta(days=i)
    #     day = datetime.strptime(date, "%Y-%m-%d").date() - timedelta(days=i)
    #     iso = datetime.strptime(day.isoformat(), "%Y-%m-%d").date()
    #     print(f"{i} days ago: {iso}")
        # print(start_date, "***********Start************")
        # print(end_date, "***********End************")

    start_date = datetime.strptime(date, "%Y-%m-%d")
    end_date = datetime.today()    
    # delta = timedelta(days=7)

    # print(start_date, "***********Start************")
    # print(end_date, "***********End************")  

    for i in range(7):
        delta = timedelta(days=i)
        end_date -= delta
        print(end_date, "***********End************") 
        count = (end_date - start_date)
        print(count.days, "########### count days ###############") # should print 5 days (6/21-6/17), but is printing 3 days for 6/24-6/21
        day_count = abs(count.days) 

    # while start_date < end_date:
    #     print(start_date) # test date: 2021-6-17
    #     end_date -= delta #should stop at end date (today or 6/21), but stops at 2021-6-24
    #     count = (end_date - start_date)
    #     print(count.days, "########### count days ###############") # should print 5 days (6/21-6/17), but is printing 3 days for 6/24-6/21
    #     day_count = abs(count.days) 

    print(start_date, "***********Start************")
    # print(end_date, "***********End************")  
    print(total, "^^^^^^^^^^^^^^^ total ^^^^^^^^^^^^^^")
    print(day_count, "^^^^^^^^^^^^^^^ day_count ^^^^^^^^^^^^^^^")    

        # opioid = Opioid.query.filter_by(opioid_name=drug).first()
        # meds = Med.query.filter_by(date_filled=iso_date, opioid_id=opioid.opioid_id).all()
        # meds = Med.query.join(Opioid).filter(Med.date_filled==iso, Opioid.opioid_name==drug).all()
        # ^^ faster query using join method instead (: -thu

        # print(day, iso, "$$$$$$$$$$$$$$ DAY AND ISO $$$$$$$$$$$$")

            # if meds:
            #     print(meds)
        # day_count += 1
            # mmes = [med.daily_MME for med in meds]
        # total += sum(mmes)


    sevenday = 0

    if day_count == 0:   
        sevenday == 0
    else:
        total = MME * day_count
        sevenday = str(total/day_count)   

    print(sevenday, "&&&&&&&&&&& seven day &&&&&&&&&&")    
        
    # calculate the last 7 days
    # turn last 7 days into datettime objects
    # query db for those days
    # if exists, add MME to total and +1 to day_count
    # divide and return jsonify('seven-day-avg': total/day_count)

    return jsonify({'seven_avg': sevenday})


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
