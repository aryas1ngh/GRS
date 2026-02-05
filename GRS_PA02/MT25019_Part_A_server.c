#include "MT25019_Part_A_common.h"

int MODE = MODE_TWO_COPY;

// helper to setup 8 dynamic buffers
void setup_message(someMessage *msg, int total_size) {
    msg->field_len = total_size / NUM_FIELDS;
    for (int i = 0; i < NUM_FIELDS; i++) {
        msg->fields[i] = malloc(msg->field_len);
        memset(msg->fields[i], 'E', msg->field_len); // fill with dummy data
    }
}

void cleanup_message(someMessage *msg) {
    for (int i = 0; i < NUM_FIELDS; i++) {
        free(msg->fields[i]);
    }
}

// helper to clear zerocopy notifs (a3)
void flush_zerocopy_queue(int sock) {
    char buf[512];
    struct msghdr msg = {0};
    struct iovec iov;
    char control[CMSG_SPACE(sizeof(struct sock_extended_err))];
    
    iov.iov_base = buf;
    iov.iov_len = sizeof(buf);
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    msg.msg_control = control;
    msg.msg_controllen = sizeof(control);

    // non-blocking check for completion signals
    while (recvmsg(sock, &msg, MSG_ERRQUEUE | MSG_DONTWAIT) > 0);
}

/////////////////  A1: two copy [standard] //////////////////////
void send_two_copy(int sock, someMessage *msg) {
    int total = msg->field_len * NUM_FIELDS;
    
    // 1st copy - user-space serialization
    char *linear_buf = malloc(total);
    for (int i = 0; i < NUM_FIELDS; i++) {
        memcpy(linear_buf + (i * msg->field_len), msg->fields[i], msg->field_len);
    }

    // 2nd copy - user -> kernel
    send(sock, linear_buf, total, 0);
    free(linear_buf);
}

//////////////////// A2: one copy (scatter/gather) //////////////////////
void send_one_copy(int sock, someMessage *msg) {
    struct msghdr header = {0};
    struct iovec iov[NUM_FIELDS];

    // point directly to the 8 heap buffers
    for (int i = 0; i < NUM_FIELDS; i++) {
        iov[i].iov_base = msg->fields[i];
        iov[i].iov_len = msg->field_len;
    }
    header.msg_iov = iov;
    header.msg_iovlen = NUM_FIELDS;

    // kernel reads directly from the 8 buffers
    sendmsg(sock, &header, 0);
}

////////////////////  A3: zero copy //////////////////////////
void send_zero_copy(int sock, someMessage *msg) {
    struct msghdr header = {0};
    struct iovec iov[NUM_FIELDS];

    for (int i = 0; i < NUM_FIELDS; i++) {
        iov[i].iov_base = msg->fields[i];
        iov[i].iov_len = msg->field_len;
    }
    header.msg_iov = iov;
    header.msg_iovlen = NUM_FIELDS;

    // hint kernel to use DMA
    if (sendmsg(sock, &header, MSG_ZEROCOPY) == -1) {
        if (errno == ENOBUFS) {
            // if sk buff is full, wait for a bit
            usleep(100); 
        }
    }
    // periodic flush
    flush_zerocopy_queue(sock);
}

// thread per client
void *handle_client(void *arg) {
    int sock = *(int *)arg;
    free(arg);
    
    // enable zerocopy on socket if needed
    if (MODE == MODE_ZERO_COPY) {
        int one = 1;
        setsockopt(sock, SOL_SOCKET, SO_ZEROCOPY, &one, sizeof(one));
    }

    // default message size 4kb
    someMessage msg;
    setup_message(&msg, 4096); 

    // send continuously
    while (1) {
        // break on broken pipe
        ssize_t ret = 0; // simulate check
        
        // send based on mode
        switch(MODE) {
            case MODE_TWO_COPY: send_two_copy(sock, &msg); break;
            case MODE_ONE_COPY: send_one_copy(sock, &msg); break;
            case MODE_ZERO_COPY: send_zero_copy(sock, &msg); break;
        }
        
        // error check to break loop if client leaves
        if (errno == EPIPE || errno == ECONNRESET) break;
    }

    cleanup_message(&msg);
    close(sock);
    return NULL;
}

// driver
int main(int argc, char *argv[]) {
    if (argc > 1) MODE = atoi(argv[1]);
    
    int server_fd, *new_sock;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    // create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // bind
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));

    // listen
    listen(server_fd, 5);

    printf("Server listening (Mode %d)...\n", MODE);

    // accept
    while (1) {
        new_sock = malloc(sizeof(int));
        *new_sock = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen);
        if (*new_sock >= 0) {
            pthread_t tid;
            pthread_create(&tid, NULL, handle_client, new_sock); // [cite: 25]
        }
    }
    return 0;
}