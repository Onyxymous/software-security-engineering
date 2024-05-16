#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

#define BUF_SIZE 16 

struct collect_mode {
  int priority;
  char *mode;
};

int main(int argc, char **argv)
{
  struct collect_mode *i1, *i2;

  i1 = malloc(sizeof(struct collect_mode));
  i1->priority = 1;
  i1->mode = malloc(BUF_SIZE);

  i2 = malloc(sizeof(struct collect_mode));
  i2->priority = 2;
  i2->mode = malloc(BUF_SIZE);

  strcpy(i1->mode, argv[1]);
  strcpy(i2->mode, argv[2]);

  printf("Collection in progress...\n");
  system("");
}
