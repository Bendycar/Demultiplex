# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | Read 1 |  101 |  + 33|
| 1294_S1_L008_R2_001.fastq.gz | Index 1 | 8 | + 33 |
| 1294_S1_L008_R3_001.fastq.gz | Index 2 (reverse complement) | 8 | + 33 |
| 1294_S1_L008_R4_001.fastq.gz | Read 2 | 101 | + 33 |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.

    [R1 distribution](R1_distribution.png)
    [R2 distribution](R2_distribution.png)
    [R3 distribution](R3_distribution.png)
    [R4 distribution](R4_distribution.png)

    2. I think I will plan on eliminating all index reads with a mean quality score less than 30. The primary rationale for such a high standard is that, given the size of our data set, I would rather throw away good data than keep bad data. I also considered the Hamming Distance between our indices, which was chosen to be relatively high. Considering that a QScore of 30 represents a .1% chance of error, I think the multiplicative probability of several base pairs switching on BOTH READS with this chance of error is quite low. 

    For downstream analysis, I would be less stringent in my cutoff value for biological reads. However, Illumina's website suggests a QScore cutoff of 30, which seems fairly reasonable to me. 

    3. Bash one liner: 
        $ ls -1 | grep -E "R[2-3]" | while read line; do zcat $line | sed -n 2~4p | grep -c "N";done
    
    R2: 3976613
    R3: 3328051
    
## Part 2
**ALL ANSWERS IN PSEUDOCODE.MD**
1. Define the problem
2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement

