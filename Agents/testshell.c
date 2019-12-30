#include <stdlib.h>
#include <stdio.h>
#include <string.h>

 


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



int main(){
	char *output = run_command_return_ouput("ls");
	printf("%s\n",output);
	//free(outputs);
	return 0;
}	

