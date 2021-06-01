"""Server for MME calculator app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db


#app routes and view functions
@app.route('/')
def homepage():
    """view homepage"""

    return render_template('homepage.html') 


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
