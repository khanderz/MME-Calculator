"""Models for MME calculator app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

#user class
class User(db.Model):
    """a user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement = True,
                        primary_key = True)
    email = db.Column(db.String, unique=True, nullable=False) 
    password = db.Column(db.String, nullable=False) 

    med_list = db.relationship("Med", backref="user")  

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} password={self.password} med_lists={self.med_list}>'
    
    def get_meds_by_date_range(self, date_filled, end_date):    
        """Takes in a date_filled and end_date and returns a list of med items that fit within the date range.
        
        Args:
            date_filled (datetime.date): start date
            end_date (datetime.date): end date
        """
        
        filtered_meds = []

        if med.date_filled != None:
            for med in self.med_list:
                if med.end_date <= end_date and med.date_filled >= date_filled:
                    filtered_meds.append(med)

        return filtered_meds


#med class
class Med(db.Model):
    """a med."""

    __tablename__ = 'meds'

    med_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))                    
    opioid_id = db.Column(db.Integer, db.ForeignKey('opioids.opioid_id'))

    drug_dose = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    days_supply = db.Column(db.Integer, nullable=False)
    date_filled = db.Column(db.Date, nullable=True)   
    end_date = db.Column(db.Date, nullable=True)

    daily_MME = db.Column(db.Numeric)

    opioid = db.relationship("Opioid", backref="med")
    
    def __init__(self, drug_dose, quantity, days_supply, daily_MME, date_filled):

        # Calculate end_date based on date_filled + days_supply
        
        if date_filled:
            date_filled = datetime.strptime(date_filled, "%Y-%m-%d").date()
            end_date = date_filled + timedelta(days=int(days_supply))
        else:
            date_filled = None 
            end_date = None
        
        new_med = super().__init__(  # db.Model.__init__()
            drug_dose=drug_dose,
            quantity=quantity,
            days_supply=days_supply,
            daily_MME=daily_MME,
            date_filled=date_filled,
            end_date=end_date,
        )
        
        return new_med

    def __repr__(self):
        return f'<med_id={self.med_id} drug dose={self.drug_dose} quantity={self.quantity} days supply={self.days_supply} daily MME={self.daily_MME} date filled={self.date_filled} end date={self.end_date} User={self.user_id}>'


#opioids class
class Opioid(db.Model):
    """an opioid."""

    __tablename__ = 'opioids'

    opioid_id = db.Column(db.Integer, 
                        autoincrement = True,
                        primary_key = True)
    opioid_name = db.Column(db.String, nullable=False)
    conversion_factor = db.Column(db.Numeric, nullable=False)         

    def __repr__(self):
        return f'<Opioid opioid_id={self.opioid_id} opioid name={self.opioid_name} MME conversion factor={self.conversion_factor}>'


# connect to database
def connect_to_db(flask_app, db_uri='postgresql:///opioids', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



if __name__ == '__main__':
    from server import app    
    connect_to_db(app)
