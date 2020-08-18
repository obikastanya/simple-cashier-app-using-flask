from db import (getItem, getAuthentification, saveTransaction)
from controller  import (listItem, listingSelectedItem, getAllItem, getTotal)
from flask import (Flask, render_template, url_for, request, redirect, session, flash)
from werkzeug import secure_filename

# create flask instance
app = Flask(__name__)
# set secret key before add session
# generate with: import uuid -> uuid.uuid4().hex
app.secret_key='64f14a0b24234f27843ca0500ca5ce6f'

@ app.route('/')
def index():
    if not "username" in session:
        return redirect(url_for("showLogin"))
    item = getItem()
    return render_template('index.html', item=item)

@ app.route('/cashier', methods=['GET', 'POST'])
def showCashier():
    if not "username" in session:
        return redirect(url_for("showLogin"))
    if(request.method == 'POST'):
        listingSelectedItem(request.form)
        item = getItem()
        total = getTotal()
        return render_template('cashier.html', item=item, listItem=listItem, total=total)
    item = getItem()
    return render_template('cashier.html', item=item)

@app.route('/reset')
def reset():
    # removed all data in dictionary
    listItem.clear()
    return redirect(url_for('showCashier'))

@app.route('/save')
def saving():
    allData=getAllItem()
    total=getTotal()
    if total > 0:
        saveTransaction(allData, total)
        flash("Transaction Has Been Saved")
        return redirect(url_for('reset'))

@ app.route('/login', methods=["GET", "POST"])
def showLogin():
    if "username" in session:
        return redirect(url_for("index"))

    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        auth=getAuthentification(username)
        if auth:
            if auth[1]==str(password):
                session["username"]=username
                return redirect(url_for("index"))
            else:
                flash("Password Is Wrong !")
        else:
            flash("Username Is Wrong !")
    return render_template('login.html')

@app.route('/logOut')
def logOut():
    session.pop("username", None)
    return redirect(url_for('showLogin'))
