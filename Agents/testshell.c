#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <json-c/json.h>
 
struct json_doc {
	char *document_id;
	char *document_ip;
	char *document_os;
	char *document_agent_id;
	char *document_rev;
	char *document_user;
	char *document_pending;
	char *document_complete;
};

char *completed_commands= {"guest","root0","linux"};
char *cmd_list = {"whoami","id","uname -a"};

struct json_doc test;

test.document_id = "99999";
test.document_ip = "127.0.0.1";
test.document_os = "linux";
test.document_agent_id = "123";
test.document_rev = "123123";
test.document_user = "root";
test.document_pending = cmd_list;
test.document_complete = completed_commands;

char *run_command_return_ouput(char *cmd){
	char *tmp;
	int counter = 0;
	tmp = malloc(1024 * sizeof(char));
	size_t n; // size for buffer
	char *dest = malloc(1025 * sizeof(char));
	FILE *ff = popen(cmd,"r");
	if (ff == NULL){
		printf("fail\n");
		exit(1);
	}
	while(fgets(tmp,1025,ff )!= NULL){
		//printf("%d\n",counter+=1);
		strncat(dest,tmp,n);

	}
    if (pclose(ff) < 0)
    	perror("pclose(3) error");

    //printf("%s\n",dest);
    return dest;

}
/*
  "_id": "91f836e1a5e1e8ab04a1f042dc01e86c",
  "_rev": "2-db0b092833e656118beb690a0483623e",
  "agent_id": "123",
  "os": "Linux",
  "ip": "0.0.0.0",
  "user": "notroot",
  "completed_commands": [],
  "pending_commands": [
  */
char *create_json(struct json_doc thedoc){
		  /*Creating a json object*/
  json_object * jobj = json_object_new_object();

  /*Creating a json string*/
  json_object *jstring = json_object_new_string(thedoc.document_user);

  /*Creating a json integer*/
  json_object *jint = json_object_new_int(10);

  /*Creating a json boolean*/
  json_object *jboolean = json_object_new_boolean(1);

  /*Creating a json double*/
  json_object *jdouble = json_object_new_double(2.14);

  /*Creating a json array*/
  json_object *jarray = json_object_new_array();

  /*Creating json strings*/
  json_object *jstring1 = json_object_new_string("c");
  json_object *jstring2 = json_object_new_string("c++");
  json_object *jstring3 = json_object_new_string("php");

  /*Adding the above created json strings to the array*/
  /*
  json_object_array_add(jarray,jstring1);
  json_object_array_add(jarray,jstring2);
  json_object_array_add(jarray,jstring3);
  */
  int x = 0;
  while(completed_commands[x] != NULL){

  	json_object_array_add(jarray,completed_commands[x]);
  	x++;

  }
  /*Form the json object*/
  /*Each of these is like a key value pair*/
  json_object_object_add(jobj,"user", jstring);
  json_object_object_add(jobj,"completed_commands", jarray);


  /*Now printing the json object*/
  printf ("The json object created:\n %s\n",json_object_to_json_string(jobj));

}


int main(){
	char *output = run_command_return_ouput("ls /root");
	//printf("%s\n",output);
	//free(outputs);





	return 0;
}	




