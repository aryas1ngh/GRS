// MT25019
// Part B Worker

#ifndef WORKER_H
#define WORKER_H

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include <string.h>

#define ROLL_LAST_DIGIT 9 

// --- 1. CPU Intensive Function ---
void* cpu(void* arg) {
    (void)arg; 
    
    // prevents the compiler from skipping the math
    volatile double result = 0.0;
    int outer_limit = ROLL_LAST_DIGIT * 1000;

    for (int i = 0; i < outer_limit; i++) {
        for (int j = 0; j < 30000; j++){
            // complex math that must be computed
            result += sin(j) * cos(j);
            result += sqrt(j) * log10(j);
        }
    }
    
    // printing to stderr so it doesn't clutter main output csv
    fprintf(stderr, " [CPU Done: %f] ", result);
    return NULL;
}

// --- 2. Memory Intensive Function ---
void* mem(void* arg) {
    (void)arg;

    size_t size = 100 * 1024 * 1024; // 100MB
    volatile int *arr = (int*)malloc(size * sizeof(int));
    
    if (!arr) return NULL;

    // Increased passes significantly to force time duration
    int passes = ROLL_LAST_DIGIT * 10000; 
    size_t num_elements = size / sizeof(int);
    size_t stride = 4096; // 4KB stride (page size) ensures cache misses

    for (int p = 0; p < passes; p++) {
        for (size_t i = 0; i < num_elements; i += stride) {
            arr[i] = p + i; 
        }
    }

    free((void*)arr); 
    fprintf(stderr, " [Mem Done] ");
    return NULL;
}

// --- 3. I/O Intensive Function ---
void* io(void* arg) {
    char filename[64];
    snprintf(filename, 64, "io_test_%ld_%ld.txt", (long)getpid(), (long)arg);

    FILE *fp = fopen(filename, "w");
    if (!fp) return NULL;

    // Increased writes significantly
    int limit = ROLL_LAST_DIGIT * 1000;

    for (int i = 0; i < limit; i++) {
        for (int j = 0; j < 1000; j++) fprintf(fp, "[Iter %d]:Writing line %d to force disk I/O latency.\n", i, j);
        fflush(fp);
        fsync(fp);
        // usleep(1000);
    }


    fclose(fp);
    remove(filename); 
    fprintf(stderr, " [IO Done] ");
    return NULL;
}
#endif