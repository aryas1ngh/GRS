// MT25019 - Part A - Common Header File
#ifndef COMMON_H
#define COMMON_H

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/uio.h>
#include <errno.h>
#include <linux/errqueue.h>
#include <time.h>

#define PORT 8080
#define NUM_FIELDS 8

// modes
#define MODE_TWO_COPY 1
#define MODE_ONE_COPY 2
#define MODE_ZERO_COPY 3

// 8 dynamically allocated strings
typedef struct {
    char *fields[NUM_FIELDS];
    int field_len; // length of individual field
} someMessage;

#endif