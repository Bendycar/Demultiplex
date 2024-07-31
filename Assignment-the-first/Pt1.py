#!/usr/bin/env python
import argparse
import bioinfo
import argparse
import numpy as np
import matplotlib.pyplot as plt
import gzip

def get_args():

    parser = argparse.ArgumentParser(description="Takes all 4 FASTQ files")
    parser.add_argument("-r", help="FASTQ file to be analyzed", type = str, required = True)
    parser.add_argument("-l", help = "nucleotide length of sequence line", type = str, required = True)
    return parser.parse_args()
        
args = get_args()

read = args.r
read_length = int(args.l)

with gzip.open(read, mode="rt") as fh1:
    read_qscores = np.zeros(read_length, dtype = int) 
    line_count = 0
    for line in fh1:
        line = line.strip('\n') # type: ignore
        line_count += 1
        if line_count % 4 == 0:
            for score in range(len(line)):
                read_qscores[score] += bioinfo.convert_phred(line[score]) # type: ignore
    read_qscores = read_qscores / (line_count/4)


x = range(read_length)
y = read_qscores
split_file = read.split('/') #This and next 3 lines just extracts only "R1", "R2", etc in a very convoluted way to use in the title of the plots
just_fastq = split_file[5]
just_fastq = just_fastq.split('_')
title = just_fastq[3]


fig, ax = plt.subplots()             
ax.plot(x,y) 
ax.set_xlabel("Nucleotide position")
ax.set_ylabel("Average Q-Score across all reads")
plt.title(f"Average Q-Score at each nucleotide position across all reads of {title}")
plt.savefig(f"{title}_distribution.png") #Should be 'R1_distribution.png' etc
        


