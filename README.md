# carpark
This is an assignment

## Dependencies
Python                   3.10.1 <br />
mysql-connector          2.2.9 <br />
mysql-connector-python   8.0.27  <br />
Flask                    2.0.2 <br />
Flask-Cors               3.0.10 <br />
PyJWT                    2.3.0 <br />


### description
user need to register and log in to take the token (registration:http://127.0.0.1:5000/; log in :http://127.0.0.1:5000/login)

user need to log in to take their token (http://127.0.0.1:5000/login)

user information detail: http://127.0.0.1:5000/getPersonalInfo (with token in header)
carpark information: http://127.0.0.1:5000/getCarparkAvailability (with token in header)
