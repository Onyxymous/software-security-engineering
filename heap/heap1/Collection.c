#include <stdlib.h>
#include <unistd.h>
 
// shell script
int main(void)
{
        execv("/bin/sh", NULL);
        return 0;
}
