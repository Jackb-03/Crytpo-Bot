import sqlite3
import twitterclass
import json
import datetime
from hashlib import sha512
import time
from flask import Flask, render_template, request, redirect, session
#from request.models import Response
from werkzeug.security import generate_password_hash, check_password_hash 
from multiprocessing import Process



'''!Sign in with the Details BELOW!'''
#Username: Jack
#Password: 123






# Create dynamic web app
app = Flask(__name__)
app.secret_key = "abcd"

# Open and connect to database 
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

#Allow access to fields by name
conn.row_factory = sqlite3.Row

def trackingsmain():
    x = 1
    while x==1:
        second = 10
        time.sleep(second)
        adjust = 0
        for row in conn.execute("SELECT * from tracking").fetchall():
            print("Hello")
            endDate = datetime.datetime.utcnow() 
            time_sub = datetime.timedelta(seconds = second+1)
            time_sub1 = datetime.timedelta(seconds = adjust)

            prestartDate = endDate - time_sub
            startDate = prestartDate - time_sub1
            start_timer = time.time()


            key = row[6]
            secret = row[7]
            secret = secret.encode()
            user_id = row[0]
            tracking_id = row[1]
            taccount = row[2]
            keyword = row[3]
            currency = row[4]
            amount = row[5]
            amounttype = "aud"
            user = twitterclass.Main(taccount, keyword, key, secret, currency , amount, amounttype, endDate, startDate)
            user.check_tweet()
            print(twitterclass.Main.tweetstatus)
            if twitterclass.Main.tweetstatus == True:
                response = twitterclass.Main.buy(user)
                if response["status"] == "error":
                    print(response["message"])
                    print("")
            
                else:
                    print("$"+str(amount)+ " in "+ currency + " was purchased")
                    bought = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

                    conn.execute('''
                        INSERT INTO transactions
                        (user_id, tracking_id, transaction_twitteraccount, transaction_keyword, transaction_cryptocurrency, transaction_amount, transaction_bought, transaction_APIkey, transaction_APIsecret)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (user_id, tracking_id, taccount, keyword, currency, amount, bought, key, secret)
                    )
                    conn.commit() 
                    
            else:
                print("")

            exetime = (time.time() - start_timer)
            adjust = (adjust + exetime)




#Default login page
@app.route("/")
def start():
    
    p = Process(target=trackingsmain)
    p.start()
    return redirect("/login") 

@app.route("/register") #app route needs to be -
def register():
    
    return render_template("register.html")


@app.route("/signout") #app route needs to be -
def signout():
    session.clear()
    return redirect("/")
 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    #method post    
    user_name = request.form['user_name']
    user_password = request.form['user_password']
    users = conn.execute("SELECT * FROM users WHERE user_name = ?", (user_name,)).fetchone()

    if not users:
        return render_template("login.html", msg = "Invalid username and/or password.")
    #check pw
    if not check_password_hash(users["user_password"], user_password):
        return render_template("login.html", msg = "Invalid username and/or password.")
    #set session
    print (users["user_id"])
    session["user_id"] = users["user_id"]
    session["user_name"] = users["user_name"]
    return redirect("/home")


@app.route("/create-account", methods=["POST"])
def create_account():

    preresults = cur.execute("select * from users").fetchall()
    count = (len(preresults))
    print (count)
    user_name = request.form["username"]
    user_password = request.form["password"]
    user_confirmpassword = request.form["confirm_password"]   

    if user_password != user_confirmpassword:
        return render_template("register.html", msg = "Passwords do not match.")

    if count >= 1:
        return render_template("register.html", msg = "The account creation limit has has been reached")
    else:
        conn.execute('''
            INSERT INTO users
            (user_name, user_password)
            VALUES(?, ?)
        ''',
            (user_name, generate_password_hash(user_password))
        )
    
        conn.commit() 

    return redirect("/login")

@app.route("/home") #app route needs to be -
def home():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        return render_template("home.html")

@app.route("/details")
def details():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        return render_template("details.html")


@app.route("/add-details", methods=["GET", "POST"])
def add():
    if not 'user_id' in session:
        return redirect("login.html")
    else:
        user_APIkey = request.form["api_key"]
        user_APIsecret = request.form["api_secret"]
        global user_id 
        user_id= session['user_id']
        print (user_id)

        cur.execute(''' UPDATE users 
                        SET user_APIkey = '%s', user_APIsecret = '%s'
                        WHERE user_id = '%s' '''
                        % (user_APIkey, user_APIsecret, user_id))
        (user_APIkey, user_APIsecret, user_id)

        conn.commit()
        return redirect("/new-tracking")

@app.route("/new-tracking")
def newtracking():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        return render_template("new_tracking.html")

@app.route("/add-new-tracking", methods=["POST", "GET"])
def addnewtracking():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        user_id= session['user_id']
        record = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
        for item in record:
            api_key = item[3]
            secret_key = item[4]
            tracking_twitteraccount = request.form["twitteraccount"]
            tracking_keyword = request.form["keyword"]
            tracking_cryptocurrency = request.form["cryptocurrency"]
            tracking_amount = request.form["amount"]

            conn.execute('''INSERT INTO tracking
            (user_id, tracking_twitteraccount, tracking_keyword, tracking_cryptocurrency, tracking_amount, user_APIkey, user_APIsecret)
            VALUES(?,?,?,?,?,?,?)
            ''',
            (user_id, tracking_twitteraccount, tracking_keyword, tracking_cryptocurrency, tracking_amount, api_key, secret_key))
            conn.commit()
        return redirect("/tracking")



@app.route("/tracking")
def tracking():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        tracking = conn.execute("SELECT * FROM tracking").fetchall()
        return render_template("tracking.html", tracking=tracking)


@app.route("/transactions") #app route needs to be -
def transactions():
    if not 'user_id' in session:
        return redirect("/login")
    else:
        transactions = conn.execute("SELECT * FROM transactions").fetchall()
        return render_template("transactions.html", transactions=transactions)




@app.route("/del-tracking/<tracking_id>", methods = ["POST", "GET", "DELETE"]) # Delete Tracking
def del_crypto(tracking_id):
    if not 'user_id' in session:
        return redirect("/login")
    else:
        conn.execute('''DELETE FROM tracking WHERE tracking_id = ?''',
                    tracking_id)
        conn.commit()
        return redirect("/tracking")

@app.route("/del-confirm/<tracking_id>") #  Confirm delete tracker page
def del_confrim(tracking_id):
    if not 'user_id' in session:
        return redirect("/login")
    else:
        tracking = conn.execute("SELECT * FROM tracking WHERE tracking_id = ?", tracking_id).fetchone()
        return render_template("del_tracking.html", tracking=tracking)





@app.route("/edit-tracking/<tracking_id>")
def edit_tracking(tracking_id):
    if not 'user_id' in session:
        return redirect("/login")
    else:
        tracking = conn.execute("SELECT * FROM tracking WHERE tracking_id = ?", tracking_id).fetchone()
        return render_template("edit_tracking.html", tracking=tracking)


@app.route("/update-tracking/<tracking_id>", methods=["POST", "GET", "DELETE"])
def update_tracking(tracking_id):
    if not 'user_id' in session:
        return redirect("/login")
    else:
        tracking_twitteraccount = request.form["t_account"]
        tracking_keyword = request.form["t_keyword"]
        tracking_cryptocurrency = request.form["t_cryptocurrency"]
        tracking_amount = request.form["t_amount"]
        if tracking_twitteraccount == "":
            return "You must give me an account"

        cur.execute(''' UPDATE tracking 
                        SET tracking_twitteraccount = '%s', tracking_keyword = '%s', tracking_cryptocurrency = '%s', tracking_amount = '%s'
                        WHERE tracking_id = '%s' '''
                        % (tracking_twitteraccount, tracking_keyword, tracking_cryptocurrency, tracking_amount, tracking_id))
        (tracking_twitteraccount, tracking_keyword, tracking_cryptocurrency, tracking_amount, tracking_id)
        conn.commit()
        return redirect("/tracking")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

