// MT25019 - Part A - Client
#include "MT25019_Part_A_common.h"
#include <time.h>

typedef struct {
    int msg_size;
} thread_args;

void *client_thread(void *arg) {
    thread_args *args = (thread_args *)arg;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    char *buffer = malloc(args->msg_size);

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "10.0.0.1", &serv_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection Failed");
        free(buffer);
        free(args);
        return NULL;
    }

    // run for fixed duration i.e, 3 sec
    struct timespec start, current;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    long long bytes = 0;
    long long messages = 0;
    
    while (1) {
        clock_gettime(CLOCK_MONOTONIC, &current);
        if (current.tv_sec - start.tv_sec >= 3) break;

        int n = recv(sock, buffer, args->msg_size, 0);
        if (n <= 0) break;
        bytes += n;
        
        // count full messages (handling fragmentation roughly)
        if (bytes/args->msg_size > messages) messages++;
    }

    close(sock);
    free(buffer);
    free(args);
    return (void *)bytes;
}

int main(int argc, char *argv[]) {

    // default
    if (argc < 3) {
        printf("Usage: %s <Threads> <MsgSize>\n", argv[0]);
        return 1;
    }

    int n_threads = atoi(argv[1]);
    int msg_size = atoi(argv[2]);

    // dynamically allocate thread array
    pthread_t *threads = malloc(sizeof(pthread_t) * n_threads);

    // start timer
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < n_threads; i++) {
        thread_args *args = malloc(sizeof(thread_args));
        args->msg_size = msg_size;
        pthread_create(&threads[i], NULL, client_thread, args);
    }

    long long total_bytes = 0;
    for (int i = 0; i < n_threads; i++) {
        void *ret;
        pthread_join(threads[i], &ret);
        total_bytes += (long long)ret;
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_taken = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    // calculate app level metrics
    // throughput = total bits / time taken
    double bits = total_bytes * 8.0;
    double gbps = (bits / time_taken) / 1e9;
    
    // avg latency per msg = total time / total msgs
    long long total_msgs = total_bytes / msg_size;
    double latency_us = (time_taken * 1e6) / total_msgs;

    // csv format for easy parsing later
    // format: throughput(Gbps), latency(microsec)
    printf("%.4f,%.2f\n", gbps, latency_us);
    
    free(threads);
    return 0;
}