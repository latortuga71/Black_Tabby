dockerd &> /dev/null &
disown
docker run -d -p 127.0.0.1:5984:5984 couchdb
