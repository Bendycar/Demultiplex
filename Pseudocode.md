NOTE: Open all files at the start, close all files at the end

DEFINING THE PROBLEM:
We are given 24 biological samples. Each of these have been prepared in some different way -- some have been given a treatment, some are control groups, some are prepared in the same way by different students -- whatever the reason, we want to sequence them all together (for the sake of efficiency) then computationally separate them by sample at the end. To accomplish this, every sample is attached to an index to keep track of its origin. Each DNA fragment is read twice -- once from the 3' end, once from the 5' end. We will call these Biological Read 1 and Biological Read 2. In a perfect world, both Read 1 and Read 2 will have the same index -- however, it is possible that some indexes will "hop" and be replaced by a different index. It is also possible that the index will be improperly copied, resulting in an unknown identity, and it is possible that some reads will be of low enough quality that we want to reject them as well. The goal of this program is to separate our data into 52 files: 24 files for Read 1, 24 files for Read 2, 2 unknown files, and 2 hopped files.

PROCESS DESCRIPTION:

![alt text](image-1.png)

To begin, we read each of our four input files 4 lines at a time, giving us one full record from each file. Once we have this, want to append the both indices to the header of each biological read. Then, we first check if both indices are in our set of valid indices. If at least one of them are not valid, then we write these to the "read1_unknown" and "read2_unknown" files and increment a counter (held as a dictionary for memory's sake) to keep track of how many records are written to this file. Next we check if both quality scores have an average above a specified threshold -- if either of them fail, we also add these to the unknown files and increment the counter. Next, we check if the reverse complement of read 3 (index 2) is the same as read 2 (index 1) -- if not, we similarly will write these records to the apppropriate "hopped" files. Finally, if we've made it this far, our data is good, so we just write the biological reads to their appropriate files.


FUNCTIONS:

Reverse complement(DNA: str) -> str
Takes valid DNA string (use validate base seq?), returns its reverse complement

Append indices(Header: str, Index1: str, Index2: str) -> Modified Header: str
Extracts just indices from read 2 and read 3 (index 1 and index 2), appends them to the end of the given header. Modifies header in place.

Write record to file(record: list, file: str, counter: int) -> None
Opens ouput file in append mode, write every entry in header list with new lines in the appropriate locations. Increments the appropriate entry in the dictionary of counts.

Average QScore(Qscore line: str) -> float (or could be a bool if below threshold)
Takes in full quality score line, uses convert phred function to calculate each position then returns their average.

PSEUDOCODE:

```Takes arguments through argparse: R1.fq, R2.fq, R3.fq, R4.fq, q score threshold (int), matched index.txt
Creates set from matched index.txt
Creates reverse complement dictionary (keys = index, values = reverse complement)

unknown_dict = {unknown: 0} #Basically just needs to be a counter, but I'm making it a dictionary for consistency with the others
hopped_dict = {}
index_dict = {}

while True:
    if file is empty:
        break
    opens all 4 files concurrently
    reads 4 lines from each file 
    append_indices function
    appends all lines to one list for each file

    if index 1 or reverse complement index 2 (obtained from dictionary) not in set of indices:
        write biological reads to unknown file (file name = "unknown")
        increment counter in unknown dictionary 
    elif either average qscore of index files below threshold:
        write biological reads to unknown file
        increment counter in unknown dictionary
    elif reverse complement of index 2 is not equal to index 1:
        write biological reads to appropriate hopped file (file name = {index}_hopped)
        increment counter in hopped dictionary with key as the two indices or adds index pair if not in dictionary
    elif reverse complement of index 2 == index 1:
        write to appropriate index file (file name = {index}_matched)
        increment counter in matched dictionary with key as the two indices or adds index pair if not in dictionary
    else:
        Nothing should be in here, something has gone horribly wrong. Write all records to error file. 
    ```

