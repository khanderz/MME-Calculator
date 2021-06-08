"""CRUD operations."""

from model import db, User, Med, Opioid, connect_to_db
import decimal

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
def calculate_MME(drug, dose, quantity, days_supply): 
    """Calculate MME with unqiue conversion factor from db for specific drug."""       

    conversion_factor = db.session.query(Opioid.conversion_factor).where(drug == Opioid.opioid_name).first()
    dose = decimal.Decimal(dose)
    quantity = decimal.Decimal(quantity)
    days_supply = decimal.Decimal(days_supply)

    for row in conversion_factor:
        MME = dose * (quantity/days_supply) * row
        return MME

    db.session.add(MME)
    db.session.commit()

    return MME

if __name__ == '__main__':
    from server import app
    connect_to_db(app)    