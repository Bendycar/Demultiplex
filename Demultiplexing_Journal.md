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

8/6/24:

I actually realized last night that this was just due to not opening the files with gzip! Need to be better about making note of what is different in test files vs real deal (ideally, there should be none... if I did this again I would gzip the test files!)
I ran the script after making this fix, and it finished in about 2:07 and output what appeared to be reasonable results.
I made one key modification for efficiency recommended by Leslie -- rewriting my reverse complement function to use a global variable for the complement dictionary, rather than recreating it every time.
This dramatically cut down on the run time! I ran the script a final time, and received this slurm output:

Command being timed: "./Demulti.py -R1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz -R2 /$        User time (seconds): 4165.56
        System time (seconds): 56.55
        Percent of CPU this job got: 89%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 1:18:48

Just making that change saved me nearly an hour!!! Big data is crazy.

At this point, I think the assignment is done. My code is well commented and efficiently written -- there are a few things that I recognize could be trimmed just slightly, but to be honest I think any further modifications would just be mostly aesthetic and I'm a little afraid to mess with what works!

Lastly, I discussed the prospect of creating figures with Leslie this morning, and decided against it.
Perhaps this is just revealing of my lack of expertise in data visualization, but for this particular output I struggle to see how a figure would improve my understanding of the results.
The primary output in my eyes is the percentage of reads matched/hopped/unknown, and this is just three percentages. I don't need a pie chart to understand what 84% looks like. 
There might be something to be said for visualizing the number of reads mapped from each sample, but it is unclear to me what the actual meaning of this visualization would be. If, say sample 1 matched more reads than sample 2, does that actually mean anything? It might mean that index hopping was more likely to occur in index 2, but couldn't it also just reflect that more reads were read off sample 1 on the sequencer??


I'm not saying that I think data visualization is pointless here, just that it would be lost on me with my current level of understanding.

As far as I know, I don't know if anybody is making figures, but I would be curious to see what people do / have done!
