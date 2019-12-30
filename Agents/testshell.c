#include <stdlib.h>
#include <stdio.h>

char output[1024];

void run_command_return_ouput(char *cmd,int **result){
	*result = malloc(1024);
	size_t n;
	FILE *ff = popen(cmd,"r");
	if (ff == NULL){
		printf("fail\n");
		exit(1);
	}
	 while ((n = fread(result, 1, sizeof(result)-1, ff)) > 0) {
	 	result[n] = '\0';
        //printf("%s", output);
    }
    if (pclose(ff) < 0)
    	perror("pclose(3) error");
}



int main(){
	int *outputs;
	run_command_return_ouput("ls",&outputs);
	printf("%s\n",outputs);
	return 0;
}	

