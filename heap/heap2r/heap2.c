#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

struct auth {
  char name[48];
  int auth;
};

struct auth *auth;
char *filter;

int main(int argc, char **argv)
{
  char line[128];
  char buffer[64];
  FILE *fp;

  while(1) {
    printf("Command?\n");

    if(fgets(line, sizeof(line), stdin) == NULL) break;

    if(strncmp(line, "auth ", 5) == 0) {
      auth = malloc(sizeof(auth));
      memset(auth, 0, sizeof(auth));
      if(strlen(line + 5) < 8 - 1) {
        strcpy(auth->name, line + 5);
      }
    }
    if(strncmp(line, "filter", 6) == 0) {
	    filter = strdup(line);
    }
    if(strncmp(line, "commit", 6) == 0) {
      if(auth->auth == 1) {
        printf("New parameters committed!\n");
        printf("Filtering collection...\n");

        fp = fopen("./flag.txt", "r");
        fgets(buffer, 64, (FILE*) fp);
        printf("flag: %s\n", buffer);

      } else {
        printf("Please enter your password\n");
      }
    }
  }
}
