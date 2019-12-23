from cmd import Cmd
from colorama import Fore, Back, Style
import pyfiglet
import json
from time import sleep

class Shell(Cmd):
    prompt = Fore.RED + 'BlackTabby> '
    intro = Fore.BLUE + "Welcome! Type ? to list commands"



    def do_exit(self, inp):
        print(Style.RESET_ALL)
        print("Bye")
        return True

    def help_exit(self):
        print(Style.RESET_ALL)
        print('exit the application. Shorthand: x q Ctrl-D.')

    def do_get_all(self, inp):
        print(Style.RESET_ALL)
        print(Fore.YELLOW + "*** Fetching All Info On Agent ***")
        print(Style.RESET_ALL)
        db = self.db_connection
        agent = self.agent_id
        document = dict(db[agent])
        print(json.dumps(document,sort_keys=True,indent=4))

    def help_get_all(self):
        print(Style.RESET_ALL)
        print(Fore.YELLOW + "Gets all the database information on the current agent.")
        print(Style.RESET_ALL)


    def help_export_json(self):
        print(Style.RESET_ALL)
        print(Fore.YELLOW + "Write agent information to file path specified Ex. export_json /tmp/output.json")
        print(Style.RESET_ALL)


    def do_export_json(self,filepath):
        print(Style.RESET_ALL)
        doc = str(self.db_connection[self.agent_id])
        print("export json output to file path")
        with open(filepath,'w') as f:
            f.write(doc)
        f.close()
        

    def do_execute(self,command):
        print(Style.RESET_ALL)
        db = self.db_connection
        agent = self.agent_id
        document_struct = dict(db[agent])
        doc = document_struct
        doc['pending_commands'].append(command)
        self.doc_id, self.doc_rev = db.save(doc)
        print(Fore.YELLOW + "Sending command...' {} '.. Waiting on response...".format(command))
        print(Style.RESET_ALL)
        for x in range(0,15):
            sleep(1)
            print(".",end=" ")
        newdoc = dict(db[agent])
        if command not in newdoc['pending_commands']:
            print(Fore.GREEN + "Successfuly executed command")
            print(Style.RESET_ALL)
        else:
            print(Fore.RED + "Failed to run command...")
            print(Style.RESET_ALL)
            return 
        index = len(newdoc['completed_commands'])
        #print(index)
        index -=1
        output = newdoc['completed_commands'][index]
        print(Fore.YELLOW + str(newdoc['completed_commands'][index]))
        print(Style.RESET_ALL)

    def help_execute(self):
        print(Style.RESET_ALL)
        print(Fore.YELLOW + "Ex. execute pwd ")
        print(Style.RESET_ALL)



    def default(self, inp):
        print(Style.RESET_ALL)
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit

