Initial Data Exploration:

    $ nano README.txt
    $ ls -lah
    $ less -S 1294_S1_L008_R1_001.fastq.gz
    $ less -S 1294_S1_L008_R2_001.fastq.gz
    $ less -S 1294_S1_L008_R3_001.fastq.gz
    $ less -S 1294_S1_L008_R4_001.fastq.gz

Based on the appearance and size of the files (), I would conclude that R1 and R4 are biological reads, whereas R2 and R3 are index reads.


I wanted to count the lines of each file, so I used the following bash command:

    $ ls -1 | grep "^1294" | while read line; do zcat $line | wc -l; done

This output:

    1452986940
    1452986940
    1452986940
    1452986940

Showing that each file had the same number of lines; approximately 1.45 billion lines. This means we are dealing with 

    1,452,986,940 / 4 = 363,246,735 reads. 