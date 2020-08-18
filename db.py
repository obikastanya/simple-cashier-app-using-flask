import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_cashier"
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE db_cashier")

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


def saveTransaction(allData, total):
    sql="insert into tb_transaksi (item, totalPrice) values(%s, %s)"
    val=(allData, str(total))
    cursor.execute(sql,val)
    db.commit()


