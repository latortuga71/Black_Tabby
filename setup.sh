echo "Attempting to run couchDB Container on 127.0.0.1:5984" 
dockerd &> /dev/null &
echo "Starting Docker Service...."
sleep 10
echo "Starting CouchDB Docker Container..."
docker run --name cat_on_couch -d -p 127.0.0.1:5984:5984 couchdb
echo "Enter Username for CouchDB Admin"
read CouchUser
echo "Enter Password for CouchDB Admin"
read -s CouchPass
echo "Keep in mind you need to edit server.py to match the username and password you just entered"
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5984/_cluster_setup -d '{"action": "enable_single_node", "bind_address":"0.0.0.0", "username": "'$CouchUser'", "password":"'$CouchPass'"}'
echo "Run BlackTabby.py to create the DB and view and begin deploying agents"
echo "When running the container next time use docker start cat_on_couch"
echo "Starting Flask Server..."
python3 server.py $CouchUser $CouchPass 127.0.0.1 5984
