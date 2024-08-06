#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp


/usr/bin/time -v ./Demulti.py -R1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-R2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-R3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
-R4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
-O ./First_try_realdeal \
-I /projects/bgmp/shared/2017_sequencing/indexes.txt

exit