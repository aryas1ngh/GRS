# MT25019
# Part D Plotter

import pandas as pd
import matplotlib.pyplot as plt

# load data
csv_file = "MT25019_Part_D_CSV.csv"
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: {csv_file} not found. Please run the Part D runner script first.")
    exit()

# set plot styles
plt.style.use('default') 
colors = {'program_a': '#1f77b4', 'program_b': '#d62728'} # process blue, thread red
labels = {'program_a': 'Prog A : Process (Fork)', 'program_b': 'Prog B :Thread (Pthread)'}
markers = {'program_a': 'o', 'program_b': 's'}

# generates a focused plot for a specific metric and worker type
def plot_individual_metric(worker_type, metric_col, metric_name, ylabel):
    
    subset = df[df['Worker'] == worker_type]
    
    plt.figure(figsize=(8, 6))
    
    # plot program A (processes)
    data_a = subset[subset['Program'] == 'program_a']
    plt.plot(data_a['Count'], data_a[metric_col], 
             marker=markers['program_a'], color=colors['program_a'], 
             linewidth=2, label=labels['program_a'])
    
    # plot program B (threads)
    data_b = subset[subset['Program'] == 'program_b']
    plt.plot(data_b['Count'], data_b[metric_col], 
             marker=markers['program_b'], color=colors['program_b'], 
             linewidth=2, linestyle='--', label=labels['program_b'])
    
    # formatting
    plt.title(f"{worker_type.upper()} Workload: {metric_name} vs Count", fontsize=14)
    plt.xlabel("Number of Workers (Count)", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    
    # save plots
    filename = f"MT25019_PartD_Plot_{worker_type}_{metric_name}.png"
    plt.savefig(filename, dpi=100)
    plt.close()
    print(f"Generated: {filename}")

workers = ['cpu', 'mem', 'io']

for worker in workers:
    # 1. execution time plot
    plot_individual_metric(worker, 'Time_Sec', 'Execution_Time', 'Time (Seconds)')
    
    # 2. cpu usage plot
    plot_individual_metric(worker, 'Avg_CPU', 'CPU_Usage', 'CPU Usage (%)')
    
    # 3. memory usage plot
    plot_individual_metric(worker, 'Avg_Mem_KB', 'Memory_Usage', 'Memory (KB)')
    
    # 4. IO speed plot only relevant for IO workers
    plot_individual_metric(worker, 'Avg_IO_kB_s', 'IO_Bandwidth', 'Disk Write Speed (kB/s)')

print("\nAll plots generated successfully!")