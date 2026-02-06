#!/bin/bash
# MT25019 Part B and C Runner Script
NS_SERVER="ns_server_arya"
NS_CLIENT="ns_client_arya"

# create namespaces
sudo ip netns add $NS_SERVER
sudo ip netns add $NS_CLIENT

# create the virtual cable
sudo ip link add veth_server type veth peer name veth_client

# plug cable into namespaces
sudo ip link set veth_server netns $NS_SERVER
sudo ip link set veth_client netns $NS_CLIENT

# turn on server side
sudo ip netns exec $NS_SERVER ip addr add 10.0.0.1/24 dev veth_server
sudo ip netns exec $NS_SERVER ip link set veth_server up
sudo ip netns exec $NS_SERVER ip link set lo up

# turn on client side
sudo ip netns exec $NS_CLIENT ip addr add 10.0.0.2/24 dev veth_client
sudo ip netns exec $NS_CLIENT ip link set veth_client up
sudo ip netns exec $NS_CLIENT ip link set lo up

# parameters
MSG_SIZES=(256 512 1024 2048 4096 8192)
THREADS=(1 2 4 6 8)
MODES=(1 2 3)
CSV_FILE="MT25019_Part_C_results.csv"

# start watch
TOTAL_START_TIME=$(date +%s)

echo "//////////////////// Compiling ////////////////////"
make clean
make
echo "//////////////////// Compilation Done ////////////////////"

# CSV Header
echo "Mode,MsgSize,Threads,Throughput_Gbps,Latency_us,Cycles,Instructions,L1_Misses,LLC_Misses,ContextSwitch" > $CSV_FILE

echo "//////////////////// Starting Experiments ////////////////////"

for MODE in "${MODES[@]}"; do
    MODE_START_TIME=$(date +%s)
    echo "////////////////////////////////////////////////////////////"
    echo "STARTING MODE $MODE"
    echo "////////////////////////////////////////////////////////////"

    for SIZE in "${MSG_SIZES[@]}"; do
        for THREAD in "${THREADS[@]}"; do
            echo "////////////////////////////////////////////////////////////"
            echo "[  TEST: Mode $MODE | Size $SIZE | Threads $THREAD  ]"
            
            # kill any old server processes
            sudo ip netns exec $NS_SERVER pkill -9 server 2>/dev/null
            
            # start server
            echo "  -> Starting Server..."
            # using 3 cores (0-2)
            # logs stdout/stderr to server.log for debugging
            sudo ip netns exec $NS_SERVER taskset -c 0-2 perf stat -x, -e cycles,instructions,L1-dcache-load-misses,LLC-load-misses,context-switches -o perf_raw.txt ./server $MODE > server.log 2>&1 &
            SERVER_PID=$!
            
            sleep 0.5
            
            # is server alive?
            if ! sudo ip netns exec $NS_SERVER kill -0 $SERVER_PID 2>/dev/null; then
                echo "ERROR: Server died immediately! Checking log:"
                cat server.log
                exit 1
            fi

            # run client
            echo "  -> Running Client (3s)..."
            
            # timeout set to 5s safety for a 3s test
            CLIENT_OUTPUT=$(sudo ip netns exec $NS_CLIENT timeout 5s ./client $THREAD $SIZE)
            
            if [ -z "$CLIENT_OUTPUT" ]; then
                echo "ERROR: Client returned no data (Timeout or Crash)."
                cat server.log
                exit 1
            fi
            
            echo "  -> Client Finished: $CLIENT_OUTPUT"

            # kill server
            sudo kill -SIGINT $SERVER_PID
            wait $SERVER_PID 2>/dev/null
            
            # parse data
            THROUGHPUT=$(echo "$CLIENT_OUTPUT" | cut -d',' -f1)
            LATENCY=$(echo "$CLIENT_OUTPUT" | cut -d',' -f2)

            get_perf_val() {
                local event=$1
                # Try finding specific cpu_core metric (for Hybrid CPUs)
                local val=$(grep "cpu_core/${event}" perf_raw.txt | awk -F, '{print $1}')
                # Fallback to standard name
                if [ -z "$val" ]; then val=$(grep "${event}" perf_raw.txt | awk -F, '{print $1}'); fi
                # Return 0 if empty/invalid
                if [[ ! "$val" =~ ^[0-9]+$ ]]; then echo "0"; else echo "$val"; fi
            }

            CYCLES=$(get_perf_val "cycles")
            INSTRUCT=$(get_perf_val "instructions")
            L1=$(get_perf_val "L1-dcache-load-misses")
            LLC=$(get_perf_val "LLC-load-misses")
            CS=$(get_perf_val "context-switches")

            # save to CSV
            echo "$MODE,$SIZE,$THREAD,$THROUGHPUT,$LATENCY,$CYCLES,$INSTRUCT,$L1,$LLC,$CS" >> $CSV_FILE
            echo "  -> Saved."
            
            # clean up temp files
            rm -f perf_raw.txt server.log
            sleep 0.2
        done
    done

    # log mode runtime
    MODE_END_TIME=$(date +%s)
    MODE_DURATION=$((MODE_END_TIME - MODE_START_TIME))
    echo "////////////////////////////////////////////////////////////"
    echo ">>> MODE $MODE COMPLETED IN $MODE_DURATION SECONDS"
    echo "////////////////////////////////////////////////////////////"
done

# stop watch
TOTAL_END_TIME=$(date +%s)
TOTAL_DURATION=$((TOTAL_END_TIME - TOTAL_START_TIME))

echo ""
echo "#################################################"
echo "ALL EXPERIMENTS COMPLETED."
echo "TOTAL RUNTIME: $TOTAL_DURATION SECONDS"
echo "#################################################"