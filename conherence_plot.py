# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

def load(path):
# Data
    with open(f"{path}/c_v.txt",'r') as f:
        c_v = f.read().splitlines()
    with open(f"{path}/u_mass.txt",'r') as f:
        umass = f.read().splitlines()
    return c_v ,umass
def co_plot(path,c_vm,umass):
    # c_v_2 = [round(float(num),10) for num in c_v]
    # umass_2 = [round(float(num),10) for num in umass]
    df = pd.DataFrame({'top_num':range(5,96,5),'c_v':c_v,'umass':umass})
    # df['c_v'].round(decimals=2)
    # df['umass'].round(decimals=2)

    fig = plt.figure(figsize=(10,10)) # 創一個current figure
    # show graph
    ax1 = fig.add_subplot(221) 
    ax1.plot( 'top_num', 'umass', data=df, marker='o', color='skyblue', linewidth=2)
    ax1.title.set_text('umass Plot')
    ax1.set_xticks(range(5,96,5))
    ax2 = fig.add_subplot(222) 
    ax2.title.set_text('c_v Plot')
    ax2.plot( 'top_num', 'c_v', data=df, marker='o', color='skyblue', linewidth=2)
    ax2.set_xticks(range(5,96,5))
    # plt.show()
    fig.savefig('coherence_plot.png')

def co_plot_log(path,c_vm,umass):


    df = pd.DataFrame({'top_num':range(5,96,5),'c_v':c_v,'umass':umass})


    fig = plt.figure(figsize=(10,10)) # 創一個current figure
    # show graph
    ax1 = fig.add_subplot(221) 
    ax1.plot( 'top_num', 'umass', data=df, marker='o', color='skyblue', linewidth=2)
    ax1.title.set_text('umass Plot')
    ax1.set_xticks(range(5,96,5))
    plt.yscale('symlog')
    ax2 = fig.add_subplot(222) 
    ax2.title.set_text('c_v Plot')
    ax2.plot( 'top_num', 'c_v', data=df, marker='o', color='skyblue', linewidth=2)
    plt.yscale("log",base =10)
    ax2.set_xticks(range(5,96,5))
    # plt.show()
    fig.savefig('log_coherence_plot.png')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
      description =__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--path', help="your c_v.txt and umass.txt file path", type=str, default = './')
    # parser.add_argument('--LDA_data_path', help="Save LDA data (1, dictionary,2, corpus,3, ldamodel) path LDA_PATH/your_LDA_data", type=str, default = 'LDA_data')
    args = parser.parse_args()
    c_v ,umass = load(args.path)
    co_plot(args.path,c_v,umass)
    co_plot_log(args.path,c_v,umass)