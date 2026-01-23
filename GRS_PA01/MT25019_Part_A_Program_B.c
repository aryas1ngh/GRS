// MT25019
// Part A Program B
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include "MT25019_Part_B_worker.h"

int main(int argc, char *argv[]) {
    // check for at least 2 arguments
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <cpu|mem|io> [num_threads]\n", argv[0]);
        return 1;
    }

    // default to 2 threads, but read from argv[2] if provided
    int count = 2; 
    if (argc >= 3) {
        count = atoi(argv[2]);
    }

    // get worker function
    void* (*worker_func)(void*) = NULL;
    if (strcmp(argv[1], "cpu") == 0) worker_func = cpu;
    else if (strcmp(argv[1], "mem") == 0) worker_func = mem;
    else if (strcmp(argv[1], "io") == 0) worker_func = io;
    else return 1;

    // allocate memory
    pthread_t *threads = malloc(count * sizeof(pthread_t));
    int *thread_ids = malloc(count * sizeof(int));

    if (!threads || !thread_ids) {
        perror("Malloc failed");
        return 1;
    }

    // create threads
    for (int i = 0; i < count; i++) {
        thread_ids[i] = i;
        if (pthread_create(&threads[i], NULL, worker_func, &thread_ids[i]) != 0) {
            perror("Thread create failed");
        }
    }

    // join them
    for (int i = 0; i < count; i++) {
        pthread_join(threads[i], NULL);
    }

    free(threads);
    free(thread_ids);
    return 0;
}