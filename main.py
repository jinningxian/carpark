import requests
import datetime
from flask import Flask, render_template, request
from flask_cors import CORS
import hashlib
import mysql.connector
import jwt


app = Flask(__name__)

#need to configure based on your own machine 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="assignment"
)
# print(mydb)
CORS(app) 
mycursor = mydb.cursor()
class User():

    def __init__(self,  email, password, fName, lName, contactNum):
        self.email = email
        self.password = password
        self.fName = fName
        self.lName = lName
        self.contactNum = contactNum
    
    def json(self):
        return {"email": self.email, "password": self.password, "fName":self.fName,
        "lName": self.lName, "contactNum": self.contactNum}


def password_encode(password):
    _hash = hashlib.md5(password.encode())
    return _hash.hexdigest()

@app.route("/")
def signupPage():
    return render_template("register.html"), 200

@app.route("/registerRequest", methods = ['POST'])
def receiveSignUpData():
    if request.method == 'POST':
        print(request.form["fName"])
        print(request.form["contactNum"])
        email = request.form["email"]
        password = request.form["password"]
        fName = request.form["fName"]
        lName = request.form["lName"]
        contactNum = request.form["contactNum"]

        try:
            
            sql = "INSERT INTO `user`(`email`, `password`, `first_name`, `last_name`, `contact_num`) VALUES (%s, %s, %s, %s, %s)"
            val = (email, password_encode(password), fName, lName, contactNum)
            mycursor.execute(sql, val)
            mydb.commit()
            return {"Status": "Register Successfully"}, 200
        except Exception:
            return {"Status": "Unable to register "}, 500
            
    return {"Status": "Method Not Allowed "}, 405

@app.route("/login", methods = ['POST', 'GET'])
def logIn():
    if request.method == 'GET':
        return render_template("login.html")
    
    mycursor.execute("SELECT email, password FROM user")
    listOfInfo = mycursor.fetchall()
    result = []
    email = request.form["email"]
    password = password_encode(request.form["password"])
    for info in listOfInfo:
        if info[0] == email and info[1] == password:
            token_generate = jwt.encode(
                {"Username": email, 
                "userVerify": True, 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},  #the token will valid for 30 mins only 
                key='carpark', 
                algorithm="HS256")
            return {"Status": "Success", "Token": token_generate}, 200
    
    return {"Status": "Unsuccess", "Token": "None"}, 401
    
    

@app.route("/getPersonalInfo")
def getInfo():
    if 'token' in request.headers:
        try:
            token = request.headers['token']
            info = dict(jwt.decode(token, "carpark", algorithms=["HS256"]))
            if(int(datetime.datetime.utcnow().timestamp()) > info["exp"]):
                return {"Access": "Access Denied, Token expired"}, 401
            try:
                mycursor.execute("SELECT * FROM user")
                allUserInfo = mycursor.fetchall()
                for userInfo in allUserInfo:
                    if userInfo[0] == info["Username"]:
                        user = User(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4])
                        return {"Access": "Access Allowed",
                        "Detail": 
                            {
                                "Email": user.json()
                            }}, 200
                return {"Access": "Access Allowed","Detail":"No Information Found"}, 200
            except Exception:
                 return {"Access": "Access Unsuccessfuly, Server error"}, 500
            
        except Exception:
            return {"Access": "Access Denied, Token Invalid"}, 401
    return {"Access": "Access Denied, Token is missing"}, 401
    

@app.route("/getCarparkAvailability")
def getCarParkAvailability():
    crrDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'token' in request.headers:
        try:
            token = request.headers['token']
            info = dict(jwt.decode(token, "carpark", algorithms=["HS256"]))
            if(int(datetime.datetime.utcnow().timestamp()) > info["exp"]):
                return {"Access": "Access Denied, Token expired", "RequestTime": crrDateTime,}, 401
            try:
                link = 'https://api.data.gov.sg/v1/transport/carpark-availability?date_time='+crrDateTime
                return {
                    "Access": "Access Allowed",
                    "RequestTime": crrDateTime,
                    "Carpark": requests.get(link).json()
                }, 200
            except Exception:
                 return {"Access": "Access Unsuccessfuly, Server error", "RequestTime": crrDateTime}, 500
            
        except Exception:
            return {"Access": "Access Denied, Token Invalid", "RequestTime": crrDateTime,}, 401
    return {"Access": "Access Denied, Token is missing", "RequestTime": crrDateTime,}, 401

#when request for /getCarparkAvailability and /getPersonalInfo
#developer should add token in the header 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

