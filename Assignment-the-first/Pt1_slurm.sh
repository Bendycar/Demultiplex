#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH -c 4
#SBATCH --mem=16G

usr/bin/time -v 

./Pt1.py -l 101 -r /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz
./Pt1.py -l 8 -r /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz
./Pt1.py -l 8 -r /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz
./Pt1.py -l 101 -r /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz

exit