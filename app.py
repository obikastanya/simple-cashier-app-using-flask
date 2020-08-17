import connection
from flask import (Flask, render_template, url_for, request, redirect, session)
from werkzeug import secure_filename

# create flask instance
app = Flask(__name__)
# set secret key before add session
app.secret_key='64f14a0b24234f27843ca0500ca5ce6f'
# generate with: import uuid -> uuid.uuid4().hex


# create instance connection
cursor = connection.cursor
db = connection.db


# get data from db
def getItem():
    cursor.execute("select * from tb_barang order by price")
    result = cursor.fetchall()
    return result

def getAuthentification(username):
    sql="select username, password from users where username= '"+str(username)+"'"
    cursor.execute(sql)
    result= cursor.fetchone()
    print(result)
    return result

listItem = {}


def listingSelectedItem(data):
    # create new dictionary index
    newKey = len(listItem)+1
    listItem[newKey] = {}
    # adding data to dictionary
    listItem[newKey]['itemName'] = data['itemName']
    listItem[newKey]['price'] = int(data['price'])
    listItem[newKey]['numberOfItem'] = int(data['numberOfItem'])
    listItem[newKey]['subTotal'] = int(data['numberOfItem'])*int(data['price'])

    print(listItem)
    return listItem

def getAllItem():
    allData=""
    for index, data in listItem.items():
        allData = allData + listItem[index]["itemName"] +" x "+ str(listItem[index]["numberOfItem"])+" , "
    return allData

def getTotal():
    total = 0
    for index, data in listItem.items():
        total += listItem[index]["subTotal"]
    return total

def checkIsSession():
    if "username" in session:
        return redirect(url_for("index"))

def checkNoSession():
    if not "username" in session:
        return redirect(url_for("showLogin"))

@ app.route('/')
def index():
    checkNoSession()
    item = getItem()
    return render_template('index.html', item=item)


@ app.route('/cashier', methods=['GET', 'POST'])
def showCashier():
    checkNoSession()
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
    print(allData)
    print(listItem)
    sql="insert into tb_transaksi (item, totalPrice) values(%s, %s)"
    val=(allData, str(total))
    cursor.execute(sql,val)
    db.commit()
    
    return redirect(url_for('reset'))

@ app.route('/login', methods=["GET", "POST"])
def showLogin():
    checkIsSession()
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        auth=getAuthentification(username)
        if auth:
            print("not empty")
            if auth[1]==str(password):
                session["username"]=auth[0]
                return redirect(url_for("index"))
            else:
                print("Password Is Wrong")
        else:
            print("Username is Wrong")
    return render_template('login.html')
