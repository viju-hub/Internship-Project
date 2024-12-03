from flask import Flask, render_template, url_for, request
import mysql.connector as sql
from logging import FileHandler,WARNING

app = Flask(__name__, template_folder="templates")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)
db_connect = sql.connect(
    host="localhost", database="flower", user="root", passwd="Vijju@123", use_pure=True)
my_cursor = db_connect.cursor(buffered=True)

@app.route('/', methods=['GET'])
def login():  # put application's code here
    return render_template('login.html')

@app.route("/Mylogin", methods=['GET', 'POST'])
def Mylogin():
    uid = request.form["username"]
    pwd = request.form["password"]
    try:
        sql = "Select username, password From login where username = " + "'" + uid + "'"
        my_cursor.execute(sql)
        cno = my_cursor.fetchall()
        res = [tuple(str(item) for item in t) for t in cno]
    except Exception as err:
        print(err)
        return render_template('error.html')
    if len(res) == 0:
        return render_template('error.html')
    else:
        usrid = res[0][0]
        passwd = res[0][1]
        if usrid == uid and pwd == passwd:
            return render_template('home.html', usrid=usrid)
        else:
            return render_template('error.html')

@app.route("/My_sign_process", methods=['POST'])
def My_sign_process():
    uid = request.form["username"]
    eid = request.form["email"]
    pwd = request.form["password"]
    try:
        sql = "INSERT INTO sign_up(username,email,password) VALUES(" + "'" + uid + "'" + "," + "'" + eid + "'" + "," + "'" + pwd + "'" + ")"
        sql1 = "INSERT INTO login(username,password) VALUES(" + "'" + uid + "'" +  "," + "'" + pwd + "'" + ")"
        my_cursor.execute(sql1)
        my_cursor.execute(sql)
        db_connect.commit()
        return render_template('home.html')
    except Exception as err:
        print(err)
        return render_template('error.html')

@app.route("/cat", methods=['GET'])
def cat():
    return render_template('catalouge.html')

@app.route("/cart", methods=['GET'])
def cart():
    return render_template('crt.html')

@app.route("/view", methods=['POST'])
def view():
    return render_template('catalouge.html')

@app.route('/logout', methods=['GET'])
def logout():
    return render_template('login.html')

@app.route('/add_to_db', methods=['POST'])
def add_to_db():
    prod_name = request.form['product_name']
    prod_price = request.form['product_price']
    quantity = request.form['product_quantity']
    total = float(prod_price)*float(quantity)
    try:
        sql = "INSERT INTO cart(name,price,quantity,total) VALUES(" + "'" + prod_name + "'" + "," + "'" + prod_price + "'" + "," + "'" + quantity + "'" + "," + "'" + str(total) + "'" +")"
        sql1 = "SELECT * FROM cart"
        sql2 = "SELECT SUM(price) as total_price FROM cart;"
        my_cursor.execute(sql)
        my_cursor.execute(sql1)
        cdata = my_cursor.fetchall()
        db_connect.commit()
        my_cursor.execute(sql2)
        new_d = my_cursor.fetchall()
        print(new_d)
        return render_template('crt.html', cdata= cdata, sumt = new_d[0][0])
    except Exception as err:
        print(err)
        return render_template('error.html')

@app.route('/deletes',methods=['GET','POST'])
def deletes():
    name = request.form['product_name']
    try:
        sql = f"DELETE FROM cart WHERE name='{name}';"
        sql1 = "SELECT * FROM cart"
        my_cursor.execute(sql)
        my_cursor.execute(sql1)
        cdata = my_cursor.fetchall()
        db_connect.commit()
        return render_template('crt.html',cdata=cdata)
    except Exception as err:
        print(err)
        return render_template('error.html')

@app.route('/continues', methods=['POST','GET'])
def continues():
    return render_template('home.html')

@app.route('/check',methods=['GET','POST'])
def check():

    try:
        sql = "DELETE FROM cart;"
        my_cursor.execute(sql)
        db_connect.commit()
    except Exception as err:
        return render_template("error.html")
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
