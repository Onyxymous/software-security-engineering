#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stddef.h>
#include <string.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/unistd.h>
#include <sys/mman.h>

#define MSG_SIZE 256

char _message[MSG_SIZE];

void configure_seccomp() {
  struct sock_filter filter [] = {
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (offsetof(struct seccomp_data, nr))),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_open, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_write, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL)
  };

  struct sock_fprog prog = {
       .len = (unsigned short)(sizeof(filter) / sizeof (filter[0])),
       .filter = filter,
  };

  printf("Configuring seccomp\n");
  prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
  prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
}

int main(int argc, char* argv[]) {
  char buffer[128];

  setbuf(stdout, NULL);
  printf("Your input will be safely stored at: %p\n", &_message);
  printf("Input?\n");
  fflush(stdin);

  fgets(buffer, MSG_SIZE, stdin);

  mprotect((void *)((unsigned long) &_message & 0xFFFFFFFFFFFFF000), getpagesize(), PROT_EXEC | PROT_WRITE | PROT_READ);

  configure_seccomp(); 
  
  return strncpy(_message, buffer, MSG_SIZE);
}
