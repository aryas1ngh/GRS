# MT25019 Part D Plotter
import matplotlib.pyplot as plt
import sys
import os
import subprocess
import math

OUTPUT_DIR = "test" 
TEST_DURATION = 3  # seconds

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# for footer containing system config
def get_system_config():
    try:
        cmd_cpu = "lscpu | grep 'Model name' | cut -d':' -f2 | xargs"
        cpu_model = subprocess.check_output(cmd_cpu, shell=True).decode().strip()
        cmd_kernel = "uname -sr"
        kernel_ver = subprocess.check_output(cmd_kernel, shell=True).decode().strip()
        return f"System Config: {cpu_model} | Kernel: {kernel_ver}"
    except:
        return "System Config: Linux (Auto-detection failed)"

SYS_CONFIG_STR = get_system_config()

def add_config_footer(plt):
    plt.figtext(0.5, 0.01, SYS_CONFIG_STR, ha="center", fontsize=9, 
                bbox={"facecolor":"orange", "alpha":0.2, "pad":5})

# reading data
def read_data():
    
    # hardcoded data
    raw_data = [
        {'Mode': 1, 'MsgSize': 256, 'Threads': 1, 'Throughput_Gbps': 9.1828, 'Latency_us': 0.22, 'Cycles': 1426901155, 'Instructions': 2460945364, 'L1_Misses': 16554862, 'LLC_Misses': 8030, 'ContextSwitch': 1556},
        {'Mode': 1, 'MsgSize': 256, 'Threads': 2, 'Throughput_Gbps': 17.6876, 'Latency_us': 0.12, 'Cycles': 3342693951, 'Instructions': 5324127886, 'L1_Misses': 40370340, 'LLC_Misses': 33889, 'ContextSwitch': 5032},
        {'Mode': 1, 'MsgSize': 256, 'Threads': 4, 'Throughput_Gbps': 33.6372, 'Latency_us': 0.06, 'Cycles': 8367502590, 'Instructions': 10169559109, 'L1_Misses': 100825866, 'LLC_Misses': 117524, 'ContextSwitch': 8929},
        {'Mode': 1, 'MsgSize': 256, 'Threads': 6, 'Throughput_Gbps': 48.0676, 'Latency_us': 0.04, 'Cycles': 13874173024, 'Instructions': 14747323758, 'L1_Misses': 170002377, 'LLC_Misses': 212664, 'ContextSwitch': 16175},
        {'Mode': 1, 'MsgSize': 256, 'Threads': 8, 'Throughput_Gbps': 59.9814, 'Latency_us': 0.03, 'Cycles': 18933431417, 'Instructions': 19405635324, 'L1_Misses': 214419167, 'LLC_Misses': 297007, 'ContextSwitch': 14863},
        {'Mode': 1, 'MsgSize': 512, 'Threads': 1, 'Throughput_Gbps': 16.8461, 'Latency_us': 0.24, 'Cycles': 2963592813, 'Instructions': 5120361511, 'L1_Misses': 34640849, 'LLC_Misses': 6878, 'ContextSwitch': 4737},
        {'Mode': 1, 'MsgSize': 512, 'Threads': 2, 'Throughput_Gbps': 33.3077, 'Latency_us': 0.12, 'Cycles': 5946369394, 'Instructions': 10238072769, 'L1_Misses': 69558379, 'LLC_Misses': 33570, 'ContextSwitch': 7160},
        {'Mode': 1, 'MsgSize': 512, 'Threads': 4, 'Throughput_Gbps': 28.8682, 'Latency_us': 0.14, 'Cycles': 30764102991, 'Instructions': 36549051973, 'L1_Misses': 404164826, 'LLC_Misses': 5701, 'ContextSwitch': 659},
        {'Mode': 1, 'MsgSize': 512, 'Threads': 6, 'Throughput_Gbps': 27.954, 'Latency_us': 0.15, 'Cycles': 30973368514, 'Instructions': 36679189531, 'L1_Misses': 398782704, 'LLC_Misses': 11817, 'ContextSwitch': 1280},
        {'Mode': 1, 'MsgSize': 512, 'Threads': 8, 'Throughput_Gbps': 27.9233, 'Latency_us': 0.15, 'Cycles': 30948513685, 'Instructions': 36725830843, 'L1_Misses': 400390349, 'LLC_Misses': 12166, 'ContextSwitch': 1249},
        {'Mode': 1, 'MsgSize': 1024, 'Threads': 1, 'Throughput_Gbps': 12.2008, 'Latency_us': 0.67, 'Cycles': 10723767002, 'Instructions': 17248701120, 'L1_Misses': 98060944, 'LLC_Misses': 3082, 'ContextSwitch': 14},
        {'Mode': 1, 'MsgSize': 1024, 'Threads': 2, 'Throughput_Gbps': 24.2004, 'Latency_us': 0.34, 'Cycles': 20995267906, 'Instructions': 34194916347, 'L1_Misses': 192944801, 'LLC_Misses': 2567, 'ContextSwitch': 21},
        {'Mode': 1, 'MsgSize': 1024, 'Threads': 4, 'Throughput_Gbps': 25.9378, 'Latency_us': 0.32, 'Cycles': 30916590170, 'Instructions': 39407524850, 'L1_Misses': 387598953, 'LLC_Misses': 6924, 'ContextSwitch': 647},
        {'Mode': 1, 'MsgSize': 1024, 'Threads': 6, 'Throughput_Gbps': 25.644, 'Latency_us': 0.32, 'Cycles': 30795624545, 'Instructions': 38990455401, 'L1_Misses': 381085354, 'LLC_Misses': 5380, 'ContextSwitch': 1252},
        {'Mode': 1, 'MsgSize': 1024, 'Threads': 8, 'Throughput_Gbps': 25.5952, 'Latency_us': 0.32, 'Cycles': 30642268308, 'Instructions': 38724816703, 'L1_Misses': 379439778, 'LLC_Misses': 7784, 'ContextSwitch': 1264},
        {'Mode': 1, 'MsgSize': 2048, 'Threads': 1, 'Throughput_Gbps': 10.8751, 'Latency_us': 1.51, 'Cycles': 10541905171, 'Instructions': 16090332068, 'L1_Misses': 96272940, 'LLC_Misses': 2008, 'ContextSwitch': 12},
        {'Mode': 1, 'MsgSize': 2048, 'Threads': 2, 'Throughput_Gbps': 21.1224, 'Latency_us': 0.78, 'Cycles': 20939320759, 'Instructions': 32274316395, 'L1_Misses': 180998115, 'LLC_Misses': 3478, 'ContextSwitch': 23},
        {'Mode': 1, 'MsgSize': 2048, 'Threads': 4, 'Throughput_Gbps': 25.0635, 'Latency_us': 0.65, 'Cycles': 30795996400, 'Instructions': 38718906273, 'L1_Misses': 400411052, 'LLC_Misses': 4086, 'ContextSwitch': 611},
        {'Mode': 1, 'MsgSize': 2048, 'Threads': 6, 'Throughput_Gbps': 24.9333, 'Latency_us': 0.66, 'Cycles': 30548045240, 'Instructions': 38464658128, 'L1_Misses': 405383231, 'LLC_Misses': 5798, 'ContextSwitch': 1228},
        {'Mode': 1, 'MsgSize': 2048, 'Threads': 8, 'Throughput_Gbps': 24.9808, 'Latency_us': 0.66, 'Cycles': 30542158124, 'Instructions': 38374117230, 'L1_Misses': 409219115, 'LLC_Misses': 6230, 'ContextSwitch': 1228},
        {'Mode': 1, 'MsgSize': 4096, 'Threads': 1, 'Throughput_Gbps': 10.8254, 'Latency_us': 3.03, 'Cycles': 10724654007, 'Instructions': 17280372017, 'L1_Misses': 92389236, 'LLC_Misses': 1614, 'ContextSwitch': 11},
        {'Mode': 1, 'MsgSize': 4096, 'Threads': 2, 'Throughput_Gbps': 20.9548, 'Latency_us': 1.56, 'Cycles': 20969013020, 'Instructions': 33984922343, 'L1_Misses': 180784948, 'LLC_Misses': 2879, 'ContextSwitch': 24},
        {'Mode': 1, 'MsgSize': 4096, 'Threads': 4, 'Throughput_Gbps': 24.1125, 'Latency_us': 1.36, 'Cycles': 30837977276, 'Instructions': 39237901014, 'L1_Misses': 384526629, 'LLC_Misses': 5066, 'ContextSwitch': 616},
        {'Mode': 1, 'MsgSize': 4096, 'Threads': 6, 'Throughput_Gbps': 24.1163, 'Latency_us': 1.36, 'Cycles': 30548028967, 'Instructions': 38571638291, 'L1_Misses': 375083970, 'LLC_Misses': 5531, 'ContextSwitch': 1235},
        {'Mode': 1, 'MsgSize': 4096, 'Threads': 8, 'Throughput_Gbps': 24.1131, 'Latency_us': 1.36, 'Cycles': 30484444603, 'Instructions': 38797613231, 'L1_Misses': 389134625, 'LLC_Misses': 3962, 'ContextSwitch': 665},
        {'Mode': 1, 'MsgSize': 8192, 'Threads': 1, 'Throughput_Gbps': 10.8286, 'Latency_us': 6.05, 'Cycles': 10505520106, 'Instructions': 17289629012, 'L1_Misses': 90621005, 'LLC_Misses': 1882, 'ContextSwitch': 11},
        {'Mode': 1, 'MsgSize': 8192, 'Threads': 2, 'Throughput_Gbps': 21.1566, 'Latency_us': 3.1, 'Cycles': 20930014225, 'Instructions': 34467585268, 'L1_Misses': 176439384, 'LLC_Misses': 2366, 'ContextSwitch': 25},
        {'Mode': 1, 'MsgSize': 8192, 'Threads': 4, 'Throughput_Gbps': 24.3125, 'Latency_us': 2.7, 'Cycles': 30804754628, 'Instructions': 39632837323, 'L1_Misses': 375632053, 'LLC_Misses': 4472, 'ContextSwitch': 616},
        {'Mode': 1, 'MsgSize': 8192, 'Threads': 6, 'Throughput_Gbps': 24.1126, 'Latency_us': 2.72, 'Cycles': 30435930015, 'Instructions': 39132203812, 'L1_Misses': 377814936, 'LLC_Misses': 5119, 'ContextSwitch': 658},
        {'Mode': 1, 'MsgSize': 8192, 'Threads': 8, 'Throughput_Gbps': 24.4354, 'Latency_us': 2.68, 'Cycles': 30673595854, 'Instructions': 39308412846, 'L1_Misses': 375297097, 'LLC_Misses': 5644, 'ContextSwitch': 1504},
        {'Mode': 2, 'MsgSize': 256, 'Threads': 1, 'Throughput_Gbps': 9.1011, 'Latency_us': 0.23, 'Cycles': 1928433414, 'Instructions': 2603358047, 'L1_Misses': 12436125, 'LLC_Misses': 3212, 'ContextSwitch': 1991},
        {'Mode': 2, 'MsgSize': 256, 'Threads': 2, 'Throughput_Gbps': 17.8256, 'Latency_us': 0.11, 'Cycles': 3953162299, 'Instructions': 5315048999, 'L1_Misses': 25946667, 'LLC_Misses': 17851, 'ContextSwitch': 5031},
        {'Mode': 2, 'MsgSize': 256, 'Threads': 4, 'Throughput_Gbps': 33.767, 'Latency_us': 0.06, 'Cycles': 9474694916, 'Instructions': 10162190687, 'L1_Misses': 70947078, 'LLC_Misses': 66258, 'ContextSwitch': 10582},
        {'Mode': 2, 'MsgSize': 256, 'Threads': 6, 'Throughput_Gbps': 49.7899, 'Latency_us': 0.04, 'Cycles': 16113347859, 'Instructions': 15209048949, 'L1_Misses': 127448489, 'LLC_Misses': 178369, 'ContextSwitch': 13101},
        {'Mode': 2, 'MsgSize': 256, 'Threads': 8, 'Throughput_Gbps': 40.8463, 'Latency_us': 0.05, 'Cycles': 29689460971, 'Instructions': 31931181674, 'L1_Misses': 283009315, 'LLC_Misses': 97527, 'ContextSwitch': 4203},
        {'Mode': 2, 'MsgSize': 512, 'Threads': 1, 'Throughput_Gbps': 17.2467, 'Latency_us': 0.24, 'Cycles': 3910369854, 'Instructions': 5313265651, 'L1_Misses': 24207893, 'LLC_Misses': 5898, 'ContextSwitch': 3011},
        {'Mode': 2, 'MsgSize': 512, 'Threads': 2, 'Throughput_Gbps': 32.8168, 'Latency_us': 0.12, 'Cycles': 7773717370, 'Instructions': 10304756249, 'L1_Misses': 53635420, 'LLC_Misses': 38644, 'ContextSwitch': 6902},
        {'Mode': 2, 'MsgSize': 512, 'Threads': 4, 'Throughput_Gbps': 28.1461, 'Latency_us': 0.15, 'Cycles': 30707437156, 'Instructions': 35140244880, 'L1_Misses': 303168342, 'LLC_Misses': 10334, 'ContextSwitch': 884},
        {'Mode': 2, 'MsgSize': 512, 'Threads': 6, 'Throughput_Gbps': 27.0642, 'Latency_us': 0.15, 'Cycles': 30990625038, 'Instructions': 35772129706, 'L1_Misses': 302044859, 'LLC_Misses': 6404, 'ContextSwitch': 1261},
        {'Mode': 2, 'MsgSize': 512, 'Threads': 8, 'Throughput_Gbps': 27.0567, 'Latency_us': 0.15, 'Cycles': 30990128938, 'Instructions': 35556921386, 'L1_Misses': 301350375, 'LLC_Misses': 9736, 'ContextSwitch': 1613},
        {'Mode': 2, 'MsgSize': 1024, 'Threads': 1, 'Throughput_Gbps': 11.325, 'Latency_us': 0.72, 'Cycles': 10711513580, 'Instructions': 16206825364, 'L1_Misses': 73564563, 'LLC_Misses': 2742, 'ContextSwitch': 7},
        {'Mode': 2, 'MsgSize': 1024, 'Threads': 2, 'Throughput_Gbps': 22.096, 'Latency_us': 0.37, 'Cycles': 20950749414, 'Instructions': 31608824188, 'L1_Misses': 144902537, 'LLC_Misses': 3366, 'ContextSwitch': 26},
        {'Mode': 2, 'MsgSize': 1024, 'Threads': 4, 'Throughput_Gbps': 24.8903, 'Latency_us': 0.33, 'Cycles': 30924561089, 'Instructions': 37660666502, 'L1_Misses': 311501324, 'LLC_Misses': 5438, 'ContextSwitch': 616},
        {'Mode': 2, 'MsgSize': 1024, 'Threads': 6, 'Throughput_Gbps': 24.7997, 'Latency_us': 0.33, 'Cycles': 30775804544, 'Instructions': 37676319599, 'L1_Misses': 319247544, 'LLC_Misses': 3458, 'ContextSwitch': 689},
        {'Mode': 2, 'MsgSize': 1024, 'Threads': 8, 'Throughput_Gbps': 24.4873, 'Latency_us': 0.33, 'Cycles': 30495615646, 'Instructions': 36895014114, 'L1_Misses': 306449547, 'LLC_Misses': 5258, 'ContextSwitch': 1220},
        {'Mode': 2, 'MsgSize': 2048, 'Threads': 1, 'Throughput_Gbps': 10.4208, 'Latency_us': 1.57, 'Cycles': 10725364632, 'Instructions': 15222645388, 'L1_Misses': 78363258, 'LLC_Misses': 2607, 'ContextSwitch': 10},
        {'Mode': 2, 'MsgSize': 2048, 'Threads': 2, 'Throughput_Gbps': 20.342, 'Latency_us': 0.81, 'Cycles': 20961981961, 'Instructions': 30061590925, 'L1_Misses': 148075892, 'LLC_Misses': 5529, 'ContextSwitch': 27},
        {'Mode': 2, 'MsgSize': 2048, 'Threads': 4, 'Throughput_Gbps': 24.6288, 'Latency_us': 0.67, 'Cycles': 30865916581, 'Instructions': 37260906156, 'L1_Misses': 321001285, 'LLC_Misses': 3724, 'ContextSwitch': 638},
        {'Mode': 2, 'MsgSize': 2048, 'Threads': 6, 'Throughput_Gbps': 24.3067, 'Latency_us': 0.67, 'Cycles': 30583265153, 'Instructions': 37010705848, 'L1_Misses': 319115233, 'LLC_Misses': 5436, 'ContextSwitch': 662},
        {'Mode': 2, 'MsgSize': 2048, 'Threads': 8, 'Throughput_Gbps': 23.9961, 'Latency_us': 0.68, 'Cycles': 30381128048, 'Instructions': 36513878869, 'L1_Misses': 311894591, 'LLC_Misses': 4334, 'ContextSwitch': 1169},
        {'Mode': 2, 'MsgSize': 4096, 'Threads': 1, 'Throughput_Gbps': 10.2427, 'Latency_us': 3.2, 'Cycles': 10715119766, 'Instructions': 16520223063, 'L1_Misses': 71493793, 'LLC_Misses': 2668, 'ContextSwitch': 15},
        {'Mode': 2, 'MsgSize': 4096, 'Threads': 2, 'Throughput_Gbps': 20.069, 'Latency_us': 1.63, 'Cycles': 20942634221, 'Instructions': 32032347537, 'L1_Misses': 148978277, 'LLC_Misses': 3556, 'ContextSwitch': 29},
        {'Mode': 2, 'MsgSize': 4096, 'Threads': 4, 'Throughput_Gbps': 23.225, 'Latency_us': 1.41, 'Cycles': 30825113578, 'Instructions': 37805918197, 'L1_Misses': 300218742, 'LLC_Misses': 5633, 'ContextSwitch': 613},
        {'Mode': 2, 'MsgSize': 4096, 'Threads': 6, 'Throughput_Gbps': 22.8535, 'Latency_us': 1.43, 'Cycles': 30628025674, 'Instructions': 37679634309, 'L1_Misses': 299393889, 'LLC_Misses': 3539, 'ContextSwitch': 658},
        {'Mode': 2, 'MsgSize': 4096, 'Threads': 8, 'Throughput_Gbps': 22.5746, 'Latency_us': 1.45, 'Cycles': 30576868203, 'Instructions': 37485040656, 'L1_Misses': 292976592, 'LLC_Misses': 3877, 'ContextSwitch': 660},
        {'Mode': 2, 'MsgSize': 8192, 'Threads': 1, 'Throughput_Gbps': 10.2815, 'Latency_us': 6.37, 'Cycles': 10534021328, 'Instructions': 16539737387, 'L1_Misses': 68487149, 'LLC_Misses': 1804, 'ContextSwitch': 14},
        {'Mode': 2, 'MsgSize': 8192, 'Threads': 2, 'Throughput_Gbps': 20.3162, 'Latency_us': 3.23, 'Cycles': 20931603990, 'Instructions': 32913499353, 'L1_Misses': 142203071, 'LLC_Misses': 3525, 'ContextSwitch': 21},
        {'Mode': 2, 'MsgSize': 8192, 'Threads': 4, 'Throughput_Gbps': 23.0992, 'Latency_us': 2.84, 'Cycles': 30801433265, 'Instructions': 38328163532, 'L1_Misses': 292232222, 'LLC_Misses': 5625, 'ContextSwitch': 601},
        {'Mode': 2, 'MsgSize': 8192, 'Threads': 6, 'Throughput_Gbps': 22.7076, 'Latency_us': 2.89, 'Cycles': 30551409982, 'Instructions': 37687828831, 'L1_Misses': 292839610, 'LLC_Misses': 3988, 'ContextSwitch': 1096},
        {'Mode': 2, 'MsgSize': 8192, 'Threads': 8, 'Throughput_Gbps': 23.1321, 'Latency_us': 2.83, 'Cycles': 30643043308, 'Instructions': 37901109037, 'L1_Misses': 291149258, 'LLC_Misses': 6051, 'ContextSwitch': 1200},
        {'Mode': 3, 'MsgSize': 256, 'Threads': 1, 'Throughput_Gbps': 6.6935, 'Latency_us': 0.31, 'Cycles': 2628682910, 'Instructions': 6797945747, 'L1_Misses': 4378068, 'LLC_Misses': 4587, 'ContextSwitch': 29097},
        {'Mode': 3, 'MsgSize': 256, 'Threads': 2, 'Throughput_Gbps': 12.9627, 'Latency_us': 0.16, 'Cycles': 7896225687, 'Instructions': 16147603635, 'L1_Misses': 42710260, 'LLC_Misses': 20524, 'ContextSwitch': 78505},
        {'Mode': 3, 'MsgSize': 256, 'Threads': 4, 'Throughput_Gbps': 23.9543, 'Latency_us': 0.09, 'Cycles': 17592373347, 'Instructions': 29958246083, 'L1_Misses': 87849365, 'LLC_Misses': 81688, 'ContextSwitch': 117811},
        {'Mode': 3, 'MsgSize': 256, 'Threads': 6, 'Throughput_Gbps': 19.5705, 'Latency_us': 0.1, 'Cycles': 30331024818, 'Instructions': 39998131114, 'L1_Misses': 229084701, 'LLC_Misses': 61915, 'ContextSwitch': 12038},
        {'Mode': 3, 'MsgSize': 256, 'Threads': 8, 'Throughput_Gbps': 19.4188, 'Latency_us': 0.11, 'Cycles': 30551573148, 'Instructions': 40451448776, 'L1_Misses': 230857473, 'LLC_Misses': 62844, 'ContextSwitch': 10475},
        {'Mode': 3, 'MsgSize': 512, 'Threads': 1, 'Throughput_Gbps': 8.13, 'Latency_us': 0.5, 'Cycles': 10626487300, 'Instructions': 18839082865, 'L1_Misses': 62504852, 'LLC_Misses': 7493, 'ContextSwitch': 19},
        {'Mode': 3, 'MsgSize': 512, 'Threads': 2, 'Throughput_Gbps': 14.647, 'Latency_us': 0.28, 'Cycles': 20529580065, 'Instructions': 33091720563, 'L1_Misses': 135653498, 'LLC_Misses': 12574, 'ContextSwitch': 6525},
        {'Mode': 3, 'MsgSize': 512, 'Threads': 4, 'Throughput_Gbps': 15.8458, 'Latency_us': 0.26, 'Cycles': 30710501944, 'Instructions': 42203209231, 'L1_Misses': 284411776, 'LLC_Misses': 28364, 'ContextSwitch': 2274},
        {'Mode': 3, 'MsgSize': 512, 'Threads': 6, 'Throughput_Gbps': 15.9877, 'Latency_us': 0.26, 'Cycles': 30543389877, 'Instructions': 42156823400, 'L1_Misses': 276301901, 'LLC_Misses': 48738, 'ContextSwitch': 3031},
        {'Mode': 3, 'MsgSize': 512, 'Threads': 8, 'Throughput_Gbps': 16.2589, 'Latency_us': 0.25, 'Cycles': 30681534925, 'Instructions': 42625114656, 'L1_Misses': 278875364, 'LLC_Misses': 13842, 'ContextSwitch': 3634},
        {'Mode': 3, 'MsgSize': 1024, 'Threads': 1, 'Throughput_Gbps': 8.0493, 'Latency_us': 1.02, 'Cycles': 10722917795, 'Instructions': 20555587448, 'L1_Misses': 66277994, 'LLC_Misses': 6106, 'ContextSwitch': 26},
        {'Mode': 3, 'MsgSize': 1024, 'Threads': 2, 'Throughput_Gbps': 16.1966, 'Latency_us': 0.51, 'Cycles': 20894903675, 'Instructions': 40502910537, 'L1_Misses': 120444853, 'LLC_Misses': 6438, 'ContextSwitch': 49},
        {'Mode': 3, 'MsgSize': 1024, 'Threads': 4, 'Throughput_Gbps': 17.2955, 'Latency_us': 0.47, 'Cycles': 30813869230, 'Instructions': 44404417977, 'L1_Misses': 283705922, 'LLC_Misses': 5185, 'ContextSwitch': 722},
        {'Mode': 3, 'MsgSize': 1024, 'Threads': 6, 'Throughput_Gbps': 17.0389, 'Latency_us': 0.48, 'Cycles': 30424581678, 'Instructions': 44115091795, 'L1_Misses': 280581543, 'LLC_Misses': 7278, 'ContextSwitch': 1331},
        {'Mode': 3, 'MsgSize': 1024, 'Threads': 8, 'Throughput_Gbps': 17.1474, 'Latency_us': 0.48, 'Cycles': 30686032928, 'Instructions': 44331676152, 'L1_Misses': 281981695, 'LLC_Misses': 8047, 'ContextSwitch': 1710},
        {'Mode': 3, 'MsgSize': 2048, 'Threads': 1, 'Throughput_Gbps': 7.8805, 'Latency_us': 2.08, 'Cycles': 10603014831, 'Instructions': 20028718105, 'L1_Misses': 63643520, 'LLC_Misses': 2064, 'ContextSwitch': 24},
        {'Mode': 3, 'MsgSize': 2048, 'Threads': 2, 'Throughput_Gbps': 15.6036, 'Latency_us': 1.05, 'Cycles': 20890566249, 'Instructions': 39461060487, 'L1_Misses': 125228262, 'LLC_Misses': 2634, 'ContextSwitch': 53},
        {'Mode': 3, 'MsgSize': 2048, 'Threads': 4, 'Throughput_Gbps': 16.9758, 'Latency_us': 0.97, 'Cycles': 30863919090, 'Instructions': 44217544959, 'L1_Misses': 278089699, 'LLC_Misses': 4871, 'ContextSwitch': 692},
        {'Mode': 3, 'MsgSize': 2048, 'Threads': 6, 'Throughput_Gbps': 16.7286, 'Latency_us': 0.98, 'Cycles': 30485499350, 'Instructions': 43786486124, 'L1_Misses': 278325700, 'LLC_Misses': 5695, 'ContextSwitch': 1371},
        {'Mode': 3, 'MsgSize': 2048, 'Threads': 8, 'Throughput_Gbps': 16.6015, 'Latency_us': 0.99, 'Cycles': 30494560040, 'Instructions': 43574028821, 'L1_Misses': 279782284, 'LLC_Misses': 9281, 'ContextSwitch': 1395},
        {'Mode': 3, 'MsgSize': 4096, 'Threads': 1, 'Throughput_Gbps': 6.893, 'Latency_us': 4.75, 'Cycles': 10526504562, 'Instructions': 19872216603, 'L1_Misses': 72735450, 'LLC_Misses': 6181, 'ContextSwitch': 18},
        {'Mode': 3, 'MsgSize': 4096, 'Threads': 2, 'Throughput_Gbps': 13.2836, 'Latency_us': 2.47, 'Cycles': 20561440608, 'Instructions': 38266865848, 'L1_Misses': 132740146, 'LLC_Misses': 9867, 'ContextSwitch': 68},
        {'Mode': 3, 'MsgSize': 4096, 'Threads': 4, 'Throughput_Gbps': 16.0326, 'Latency_us': 2.04, 'Cycles': 30499372116, 'Instructions': 42813455400, 'L1_Misses': 272713589, 'LLC_Misses': 16258, 'ContextSwitch': 735},
        {'Mode': 3, 'MsgSize': 4096, 'Threads': 6, 'Throughput_Gbps': 15.9731, 'Latency_us': 2.05, 'Cycles': 30482116562, 'Instructions': 42969606151, 'L1_Misses': 277689611, 'LLC_Misses': 14108, 'ContextSwitch': 1466},
        {'Mode': 3, 'MsgSize': 4096, 'Threads': 8, 'Throughput_Gbps': 15.9838, 'Latency_us': 2.05, 'Cycles': 30471807618, 'Instructions': 42866995971, 'L1_Misses': 272903080, 'LLC_Misses': 22373, 'ContextSwitch': 1458},
        {'Mode': 3, 'MsgSize': 8192, 'Threads': 1, 'Throughput_Gbps': 6.7702, 'Latency_us': 9.68, 'Cycles': 10416880366, 'Instructions': 19418532389, 'L1_Misses': 68886000, 'LLC_Misses': 8628, 'ContextSwitch': 29},
        {'Mode': 3, 'MsgSize': 8192, 'Threads': 2, 'Throughput_Gbps': 13.4496, 'Latency_us': 4.87, 'Cycles': 20726179242, 'Instructions': 38801068412, 'L1_Misses': 129090672, 'LLC_Misses': 5182, 'ContextSwitch': 53},
        {'Mode': 3, 'MsgSize': 8192, 'Threads': 4, 'Throughput_Gbps': 15.885, 'Latency_us': 4.13, 'Cycles': 30605732225, 'Instructions': 42909726023, 'L1_Misses': 279975620, 'LLC_Misses': 10639, 'ContextSwitch': 711},
        {'Mode': 3, 'MsgSize': 8192, 'Threads': 6, 'Throughput_Gbps': 16.0667, 'Latency_us': 4.08, 'Cycles': 30424921425, 'Instructions': 42919142473, 'L1_Misses': 277334887, 'LLC_Misses': 10085, 'ContextSwitch': 1386},
        {'Mode': 3, 'MsgSize': 8192, 'Threads': 8, 'Throughput_Gbps': 15.9818, 'Latency_us': 4.1, 'Cycles': 30579433346, 'Instructions': 43120507207, 'L1_Misses': 275348161, 'LLC_Misses': 12519, 'ContextSwitch': 1609},
    ]

    for row in raw_data:
        try:
            throughput_bps = row['Throughput_Gbps'] * 1e9
            total_bytes = (throughput_bps / 8.0) * TEST_DURATION
            if total_bytes > 0:
                row['Cycles_Per_Byte'] = row['Cycles'] / total_bytes
            else:
                row['Cycles_Per_Byte'] = 0
        except KeyError:
            row['Cycles_Per_Byte'] = 0
            
    print(f"Loaded {len(raw_data)} rows.")
    return raw_data

# serialize the data 
def get_series(data, mode, fixed_col, fixed_val, x_col, y_col):
    filtered = [row for row in data if row['Mode'] == mode and row[fixed_col] == fixed_val]
    filtered.sort(key=lambda x: x[x_col])
    x = [row[x_col] for row in filtered]
    y = [row[y_col] for row in filtered]
    return x, y

# main plotting logic
def create_subplots(data, x_col, y_col, fixed_col, title, ylabel, filename, log_x=False):
    unique_vals = sorted(list(set(d[fixed_col] for d in data)))
    
    if not unique_vals:
        print(f"Warning: No data found for {filename}")
        return

    num_plots = len(unique_vals)
    cols = 2
    rows = math.ceil(num_plots / cols)
    
    fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows))
    if num_plots == 1: axes = [axes]
    else: axes = axes.flatten()
    
    print(f"Generating {filename}...")
    
    for i, val in enumerate(unique_vals):
        ax = axes[i]
        
        # get data for each mode
        x1, y1 = get_series(data, 1, fixed_col, val, x_col, y_col)
        x2, y2 = get_series(data, 2, fixed_col, val, x_col, y_col)
        x3, y3 = get_series(data, 3, fixed_col, val, x_col, y_col)
        
        ax.plot(x1, y1, marker='o', label='Two-Copy (A1)')
        ax.plot(x2, y2, marker='s', label='One-Copy (A2)')
        ax.plot(x3, y3, marker='^', label='Zero-Copy (A3)')
        
        # format axes
        if log_x:
            ax.set_xscale('log', base=2)
            
        ax.set_title(f'{fixed_col}: {int(val)}')
        
        # automatically set x label
        if x_col == 'MsgSize':
            ax.set_xlabel("Message Size (Bytes)")
        elif x_col == 'Threads':
            ax.set_xlabel("Thread Count")
        else:
            ax.set_xlabel(x_col)
            
        ax.set_ylabel(ylabel)
        ax.grid(True, which="both", ls="-", alpha=0.4)
        ax.legend()


    # remove unused axes
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    
    # set name and add sysconfig
    out_path = os.path.join(OUTPUT_DIR, f'MT25019_Part_D_{filename}')
    add_config_footer(plt)
    plt.subplots_adjust(bottom=0.15)
    plt.savefig(out_path)
    print(f"Saved {out_path}")
    plt.close()

if __name__ == "__main__":
    all_data = read_data()
    
    # 1. L1 Misses
    create_subplots(all_data, 'MsgSize', 'L1_Misses', 'Threads', 
                   "L1 Cache Misses vs Message Size", 
                   "L1 Misses", "final_l1_misses.png", log_x=True)
                   
    # 2. LLC Misses
    create_subplots(all_data, 'MsgSize', 'LLC_Misses', 'Threads', 
                   "LLC Misses vs Message Size", 
                   "LLC Misses", "final_llc_misses.png", log_x=True)

    # 3. Latency
    create_subplots(all_data, 'Threads', 'Latency_us', 'MsgSize', 
                   "Latency vs Thread Count", 
                   "Latency (us)", "final_latency.png", log_x=False)

    # 4. Total Cycles vs Message Size
    create_subplots(all_data, 'MsgSize', 'Cycles', 'Threads', 
                   "Total CPU Cycles vs Message Size", 
                   "Total CPU Cycles", "final_cycles_vs_bytes.png", log_x=True)

    # 5. Throughput
    create_subplots(all_data, 'MsgSize', 'Throughput_Gbps', 'Threads', 
                   "Throughput vs Message Size", 
                   "Throughput (Gbps)", "final_throughput.png", log_x=True)
    
    print("\nAll plots generated successfully.")