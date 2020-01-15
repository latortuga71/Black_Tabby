# Black Tabby

Black Tabby is a quick C2 Server i created using Python Flask and CouchDB 
the motivation behind this project was to learn more about noSQL databases as well as how C2 server's work on the back end. I ended up learning about JWT as well as thats how the agents keep tokens fresh. 

### Prerequisites
```
Docker
Python3
```
### Installing

After docker and python3 is on your machine all you need to do is clone this repo and run the setup.sh file

```
git clone https://github.com/latortuga71/Black_Tabby.git
cd Black_Tabby
chmod +x setup.sh
pip3 -r install requirements.txt
./setup.sh
```

Then you will be asked to set the username & password for the CouchDB container and it will run on port 5984 of your local machine
It will also ask you for two secrets, a user-agent secret and an agent secret, these are very importing and are used when creating agents
so they can authenticate to your flask server. Which in turn communicates to the CouchDB container

![](https://github.com/latortuga71/Black_Tabby/blob/master/setup1.JPG)

After that has successfully completed run the following command
```
python3 BlackTabby.py
```
You will be asked for the credentials provided as well as the ip address and port that the CouchDB container is running on which should be 127.0.0.1 5984 unless you set this up to run on a different server that the CLI interface will be running on. This will create a view in CouchDB that is neccesary for the CLI to function properly.

## Creating Agents

There is an option on the CLI that allows you to create agents, it will ask you for the ip address and port it will be connecting to. In this case you do not enter the port 5984 which is CouchDB you would enter 9000 which is the flask server.
So if you are running the CLI and Server on same host, you would enter 127.0.0.1 and port 9000. After you will be asked for the two secrets specified during the bash setup script.

## Agent CLI (Work in progress)

Once you have connected to an agent just enter ? to see a list of options
* execute followed by a command will run a command and return the result
```
execute cmd
```
* get_all will return the full database document for that agent
* export json will write the json to a file.
```
export_json /tmp/json_output.txt
```

![](https://github.com/latortuga71/Black_Tabby/blob/master/setup3.JPG)

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
