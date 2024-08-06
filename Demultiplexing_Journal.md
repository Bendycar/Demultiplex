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

7/30/24:

We've talked at length about read 2 and read 3 representing indices 1 and 2, where index 2 is the reverse complement of index 1, but I quickly looked at the head of these files and manually compared them, confirming that the sequence lines are indeed reverse complements of each other:

    $ zcat 1294_S1_L008_R2_001.fastq.gz | head
    $ zcat 1294_S1_L008_R3_001.fastq.gz | head

To determine the length of the reads from each file, I took a sample of the first 10 records in hopes that this would be representative of all the lengths:

    $ zcat 1294_S1_L008_R3_001.fastq.gz | head -40 | sed -n 2~4p | awk '{print length($0)}'
    $ zcat 1294_S1_L008_R3_001.fastq.gz | head -40 | sed -n 2~4p | awk '{print length($0)}'
    $ zcat 1294_S1_L008_R3_001.fastq.gz | head -40 | sed -n 2~4p | awk '{print length($0)}'
    $ zcat 1294_S1_L008_R3_001.fastq.gz | head -40 | sed -n 2~4p | awk '{print length($0)}'

Doing this revealed that the index sequences were 8 characters long, and the biological reads were 101 characters. 

Finally, to assess if Phred score is encoding with ASCII + 33 or + 64, I searched for characters that only exist in one type of encoding.

    $ zcat 1294_S1_L008_R1_001.fastq.gz | head -40 | sed -n 4~4p | grep '#'

Repeating this command for all files revealed that the "#" character exists in all the quality score lines, meaning the encoding must be Phred +33.

Next, I created my unit test files. To do this I essentially just took the first 5 records from each record to get the correct formatting, then manipulated the data to represent all possible outcomes of reads:

Read 1: Unknown with N's
Read 2: Unknown with matched but invalid index
Read 3: Mismatched but valid
Read 4: Mismatched and invalid
Read 5: Matched but one record below QScore cutoff
Read 6: Valid matched

The last thing I did today was write my python script for part 1 of the assignment, which creates figures for the average quality distribution of each read.

7/31/24:

Had to fix a few errors in my python script -- I very lazily extracted the title of each ride ("R1", "R2", etc) using index slicing, but this failed when I moved from text files to the real deal. I changed to using .split, which should be much safer, then ran the script again.

I also moved on to the questions of part 1, and used some bash commands to answer them.

8/5/24:

Added remaining features of Pt.3 Python script, which I was able to get working on my test files. When I ran it on the real deal files, I got this bizarre error:

Traceback (most recent call last):
  File "/gpfs/projects/bgmp/bcarr/bioinfo/Bi622/Demultiplex/Assignment-the-third/./Demulti.py", line 219, in <module>
    record1 = [fh1.readline().strip() for i in range(4)] #Calls the readline function 4 times -- easier for me to work with than modulo shenanigans
               ^^^^^^^^^^^^^^
  File "<frozen codecs>", line 322, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start byte
Command exited with non-zero status 1

Even googling this didn't reveal much.... will ask Leslie tomorrow!