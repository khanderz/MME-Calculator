"""CRUD operations."""

from model import db, User, Med, Opioid, connect_to_db
import decimal
from datetime import datetime

# Create, Read, Update, Delete functions
# User functions
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first() 

def get_user_by_email_and_password(email, password):
    """Return user by email and password."""
    
    user = User.query.filter(User.email == email).first()

    if user:
        if user.password == password:
            return user
    else:
        return None
    
# MME and drug functions
def get_opioid_by_name(opioid_name):
    """Return `Opioid` with the given `opioid_name`."""
    
    return Opioid.query.filter_by(opioid_name=opioid_name).first()


def add_opioid_to_user_medlist(
    user,
    opioid,
    drug_dose,
    quantity,
    days_supply,
    daily_MME,
    date_filled
):
    """Create `Med` object associated with `user`."""

    med = Med(
        drug_dose=drug_dose, 
        quantity=quantity, 
        days_supply=days_supply, 
        daily_MME=daily_MME,
        date_filled=date_filled,
    )
    med.opioid = opioid
    
    user.med_list.append(med)
    
    db.session.add(user)
    db.session.commit()


def calculate_MME(drug, dose, quantity, days_supply): 
    """Calculate MME with unqiue conversion factor from db for specific drug.
    
    Args:
        - drug (str): the name of a drug (must be present in database)
        - dose (decimal.Decimal)
        - quantity (decimal.Decimal)
        - days_supply (decimal.Decimal)
    """
    
    if not dose or not quantity or not days_supply:
        return 0

    # Get `Opioid` from database to get its conversion factor
    opioid = get_opioid_by_name(drug)

    MME = dose * (quantity // days_supply) * opioid.conversion_factor

    return MME

def get_meds():
    """view all meds in med list"""

    return Med.query.all()    


def get_meds_by_date_range(date_filled, end_date):    
    """Takes in a date_filled and end_date and returns a list of med items that fit within the date range.
    
    Args:
        date_filled = db.Column(db.Date, nullable=True)   
        end_date = db.Column(db.Date, nullable=True)
    """

    med_list = Med.query.filter(
        Med.end_date <= end_date
    ).filter(
        Med.date_filled >= date_filled
    ).all()

    return med_list


if __name__ == '__main__':
    from server import app
    connect_to_db(app)    