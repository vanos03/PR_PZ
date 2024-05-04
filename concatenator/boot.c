#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

#define COMMAND_DEL "/bin/rm"
#define FILENAME argv[0]
#define ERR(msg) do{perror(msg);exit(EXIT_FAILURE);}while(0);

char *resize(char *str, int new_size){
    char tmp[strlen(str)];
    strcpy(tmp, str);
    if (realloc(str, new_size*2) == NULL) ERR("realloc");
    // strcat(str, tmp);
    return str;
}

int main(int argc, char **argv){

    int fd = open(FILENAME, O_RDONLY);
    if (fd == -1) ERR("open");

    unsigned int size = lseek(fd, 0, SEEK_END) - lseek(fd, 0, SEEK_SET);
    unsigned char *buf = malloc(size+3);
    if (buf == NULL)ERR("malloc");
    memset(buf, 0, size);
    buf[size+2] = 0x4c;
    buf[size+1] = 0x45;
    buf[size] = 0x7f;

    if (read(fd, buf, size) != size) ERR("read");
    printf("%lx %lx %lx\n", buf[0], buf[1], buf[2]);
    close(fd);

    char out_filename[] = ".out_0";
    
    int prev_file_offset;
    for (int i = 0; i < size-3; i++)
        if (buf[i] == 0x7f && buf[i+1] == 0x45 && buf[i+2] == 0x4c && i >0){ 
            // buf = buf+i;
            prev_file_offset = i;
            break;
        }

    // char *command_cls = malloc(strlen(COMMAND_DEL));
    // strcpy(command_cls, COMMAND_DEL);

    for (int i = 0; i <= size; i++){
        if (buf[i] == 0x7f && buf[i+1] == 0x45 && buf[i+2] == 0x4c && i > prev_file_offset) {
            
            int fd_out = open(out_filename, O_WRONLY | O_CREAT | O_TRUNC, 0744);
            if (fd_out == 1) ERR("open");

            printf("i = %d prev_file_off = %d %d\n", i, prev_file_offset, i - prev_file_offset);
            write(fd_out, buf + prev_file_offset, i - prev_file_offset);
            prev_file_offset = i;
            close(fd_out);

            pid_t pid = fork();
            if (pid < 0){
                ERR("fork");
            } else if (pid == 0) {
                char command[strlen(out_filename)*2];
                sprintf(command, "./%s", out_filename);
                printf("%s\n", command);
                char *args[] = {command, NULL};
                execv(command, args);
                perror("execv");
                exit(EXIT_FAILURE);
            } else {
                // command_cls = resize(command_cls, strlen(command_cls) + strlen(out_filename));
                // strcat(command_cls, " ");
                // strcat(command_cls, out_filename);

                prev_file_offset = i;
                out_filename[strlen(out_filename)-1]++;
            }
        }
    }

    pid_t pid_cls = fork();
    if (pid_cls < 0){
        ERR("fork");
    } else if (pid_cls == 0) {
        char *args[] = {"/bin/bash", "-c", "/bin/rm -f .out_*", NULL};
        execv(args[0], args);
        perror("execv");
        exit(EXIT_FAILURE);
    }
    

    return 0;
    
}