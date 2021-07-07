# MME-Calculator
Morphine Milligram Equivalent (MME) Calculator

## Description:
MME is a numerical standard for clinicians to gauge opioid addiction risk. It is the amount of morphine in milligrams equivalent to the strength of the opioid dose prescribed. Calculating total daily MME can help guide clinicians in pain management and aid in mitigating opioid addiction and accidental overdose. The calculator will calculate the total daily MME for the given medication list, and relay the appropriate clinical assessment for the MME that populates. 

This web app is designed for use by clinicians and by patients.

For patients: Using this web app to calculate your MME will increase the transparency between you and your pain management. Understand your options and ways to improve your therapy by reading the clinical assessments based on your MME. Know what is an acceptable therapeutic range and when it may be time to consider a naloxone prescription, which could save your life in an accidental overdose situation. Be prepared. Know your risk. Take control back.

Per CDC: Calculating the MME of opioids helps identify patients who may benefit from closer monitoring, reduction or tapering of opioids, prescribing of naloxone, or other measures to reduce risk of overdose. 

*There is no completely safe opioid dose, and this calculator does not substitute for clinical judgment. Use caution when prescribing opioids at any dosage, and prescribe the lowest effective dose.*


## Contents
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Installation](#installation)
* [Links](#links)

## <a name="tech-stack"></a>Technologies:
* Python
* Javascript
* Flask
* Jinja2
* jQuery
* HTML
* CSS
* AJAX
* SQLAlchemy
* BootStrap
* PostgreSQL
* Chart.js

## <a name="features"></a>Features: 

#### Login/Logout
![alt text](https://github.com/khanderz/MME-Calculator/blob/main/static/img/login.gif)

#### Total MME Increments
![alt text](https://github.com/khanderz/MME-Calculator/blob/main/static/img/increment.gif)

#### Save a Medication to Your User Dashboard & Charts
![alt text](https://github.com/khanderz/MME-Calculator/blob/main/static/img/save.gif)

Weekly and monthly charts on the user dashboard displays 7-day and 30-day total daily MMEs. This feature allows the clinician/patient to assess when a person experienced one or more days in the last 7 days/30 days where their cumulative MME from opioid prescriptions exceeded 90 MME, increasing their risk of opioid addiction and/or accidental overdose.

Date filled is a required input for the charts.


## <a name="installation"></a>Installation: 
```git clone https://github.com/khanderz/MME-Calculator.git```
```cd MME-calculator```
```pip3 install -r requirements.txt```
```python3 seed_db.py```

## Run program:
```python3 server.py```


## <a name="links"></a>Links:
* https://www.cdc.gov/drugoverdose/index.html
* https://www.linkedin.com/in/khanh-mai-33190/

