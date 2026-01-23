// MT25019
// Part A Program A
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <string.h>
#include "MT25019_Part_B_worker.h"

int main(int argc, char *argv[]) {
    // check for at least 2 arguments
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <cpu|mem|io> [num_processes]\n", argv[0]);
        return 1;
    }

    // default to 2 threads, but read from argv[2] if provided
    int count = 2; 
    if (argc >= 3) {
        count = atoi(argv[2]);
    }

    void* (*worker_func)(void*) = NULL;
    if (strcmp(argv[1], "cpu") == 0) worker_func = cpu;
    else if (strcmp(argv[1], "mem") == 0) worker_func = mem;
    else if (strcmp(argv[1], "io") == 0) worker_func = io;
    else {
        fprintf(stderr, "Invalid worker type. Use cpu, mem, or io.\n");
        return 1;
    }

    // create 'count' child processes
    for (int i = 0; i < count; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("Fork failed");
            exit(1);
        } else if (pid == 0) {
            worker_func((void*)(long)i);
            exit(0);
        }
    }

    // wait for all children
    while (wait(NULL) > 0);
    return 0;
}