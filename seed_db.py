"""Script to seed database."""
from server import app
from model import db, connect_to_db, Opioid
import os

os.system('dropdb opioids')
os.system('createdb opioids')

connect_to_db(app)
db.create_all()

# opioid database
opioids = [
    Opioid(opioid_name="Codeine", conversion_factor=0.15),
    Opioid(opioid_name="Fentanyl transdermal", conversion_factor=2.4),
    Opioid(opioid_name="Fentanyl buccal/sublingual/lozenge", conversion_factor=0.13),
    Opioid(opioid_name="Fentanyl film/oral spray", conversion_factor=0.18),
    Opioid(opioid_name="Fentanyl nasal spray", conversion_factor=0.16),
    Opioid(opioid_name="Hydrocodone", conversion_factor=1),
    Opioid(opioid_name="Hydrocodone", conversion_factor=4),
    Opioid(opioid_name="Methadone 1-20mg", conversion_factor=4),
    Opioid(opioid_name="Methadone 21-40mg", conversion_factor=8),
    Opioid(opioid_name="Methadone 41-60mg", conversion_factor=10),
    Opioid(opioid_name="Methadone 61-80mg", conversion_factor=12),
    Opioid(opioid_name="Morphine", conversion_factor=1),
    Opioid(opioid_name="Oxycodone", conversion_factor=1.5),
    Opioid(opioid_name="Oxymorphone", conversion_factor=3),
    Opioid(opioid_name="Tapentadol", conversion_factor=0.4)
]

db.session.add_all(opioids)
db.session.commit()
print("Added opioids to DB")