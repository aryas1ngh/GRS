CC = gcc
CFLAGS = -Wall -pthread -g -Wno-unused-variable

all: server client

server: MT25019_Part_A_server.c
	$(CC) $(CFLAGS) -o server MT25019_Part_A_server.c

client: MT25019_Part_A_client.c
	$(CC) $(CFLAGS) -o client MT25019_Part_A_client.c

clean:
	rm -f server client