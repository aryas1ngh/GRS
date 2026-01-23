# MT25019
# Makefile

# compiler + flags
CC = gcc
CFLAGS = -Wall -Wextra
LDFLAGS = -lm
PTHREAD_FLAGS = -pthread
SRC_A = MT25019_Part_A_Program_A.c
SRC_B = MT25019_Part_A_Program_B.c

# targets
all: program_a program_b

# compile program A (processes)
program_a: $(SRC_A) MT25019_Part_B_worker.h
	$(CC) $(CFLAGS) -o program_a $(SRC_A) $(LDFLAGS)

# compile program B (threads)
program_b: $(SRC_B) MT25019_Part_B_worker.h
	$(CC) $(CFLAGS) -o program_b $(SRC_B) $(LDFLAGS) $(PTHREAD_FLAGS)

# clean up
clean:
	rm -f program_a program_b *.o *.txt