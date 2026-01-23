#!/bin/bash
# MT25019_Part_D_runner.sh

CSV_FILE="MT25019_Part_D_CSV.csv"
echo "Program,Worker,Count,Time_Sec,Avg_CPU,Avg_Mem_KB,Avg_IO_kB_s" > $CSV_FILE

# cleanup first then silently compile
make clean > /dev/null 2>&1
make > /dev/null 2>&1

echo "Starting Part D Data Collection..."
echo "---------------------------------------------------------------------"
printf "%-10s %-5s %-5s %-10s %-10s %-10s %-10s\n" "Prog" "Work" "Cnt" "Time" "CPU%" "Mem(KB)" "IO(kB/s)"

# function to measure cpu/mem/io stats for given number of workers (processes or threads)
measure() {
    PROG=$1
    WORK=$2
    COUNT=$3
    
    # 1. start program pinned to CPU 0 using taskset
    taskset -c 0 ./$PROG $WORK $COUNT > /dev/null 2>&1 &
    PID=$!
    START_TIME=$(date +%s.%N)
    
    SUM_CPU=0
    SUM_MEM=0
    SUM_IO=0
    SAMPLES=0
    
    # 2. monitor loop
    while kill -0 $PID 2> /dev/null; do
        # A. CPU
        # sums CPU for all processes matching the program name
        STATS=$(top -b -n 1 | grep "$PROG" | awk '{cpu+=$9} END {print cpu}')
        
        # B. MEM
        # using ps since it gives KB, and not mem %. 
        MEM_VAL=$(ps -C "$PROG" -o rss= | awk '{sum+=$1} END {print sum}')
        if [ -z "$MEM_VAL" ]; then MEM_VAL=0; fi

        # C. IO
        # we run for 2 iterations (-c 2) and parse the LAST one to get real-time stats
        # then sum 4th column (kB_wrtn/s) for all devices to be safe
        IO_VAL=$(iostat -d -k 1 2 | tail -n +4 | grep -v "Device" | grep -v "^$" | awk '{sum+=$4} END {print sum}')
        
        # fallback if iostat output format varies slightly
        if [ -z "$IO_VAL" ]; then IO_VAL=0; fi

        if [ ! -z "$STATS" ]; then
            # cap cpu at 100%
            IS_OVER=$(echo "$STATS > 100.0" | bc)
            if [ "$IS_OVER" -eq 1 ]; then STATS="100.00"; fi

            SUM_CPU=$(echo "$SUM_CPU + $STATS" | bc)
            SUM_MEM=$(echo "$SUM_MEM + $MEM_VAL" | bc)
            SUM_IO=$(echo "$SUM_IO + $IO_VAL" | bc)
            SAMPLES=$((SAMPLES + 1))
        fi
    done

    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)

    if [ $SAMPLES -gt 0 ]; then
        AVG_CPU=$(echo "scale=2; $SUM_CPU / $SAMPLES" | bc)
        AVG_MEM=$(echo "$SUM_MEM / $SAMPLES" | bc) # int division for KB
        AVG_IO=$(echo "scale=2; $SUM_IO / $SAMPLES" | bc)
    else
        AVG_CPU=0; AVG_MEM=0; AVG_IO=0
    fi
    
    printf "%-10s %-5s %-5s %-10.2f %-10s %-10s %-10s\n" "$PROG" "$WORK" "$COUNT" "$DURATION" "$AVG_CPU" "$AVG_MEM" "$AVG_IO"
    echo "$PROG,$WORK,$COUNT,$DURATION,$AVG_CPU,$AVG_MEM,$AVG_IO" >> $CSV_FILE
}

# execute for processes + threads
for count in {2..5}; do
    for worker in cpu mem io; do measure "program_a" "$worker" "$count"; done
done

for count in {2..8}; do
    for worker in cpu mem io; do measure "program_b" "$worker" "$count"; done
done

echo "---------------------------------------------------------------------"
echo "Part D data collection complete. Data saved to $CSV_FILE"
echo "---------------------------------------------------------------------"

# plotting using matplotlib
echo "Generating Plots..."
python3 MT25019_Part_D_plotter.py
echo "Done. All plots saved."

echo "---------------------------------------------------------------------"
echo "Part D Complete."
echo "---------------------------------------------------------------------"