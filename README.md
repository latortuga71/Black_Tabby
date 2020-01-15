# Black Tabby

Black Tabby is a quick C2 Server i created using Python Flask and CouchDB 
the motivation behind this project was to learn more about noSQL databases as well as how C2 server's work on the back end.

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

![](setup1.jpg)

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

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
