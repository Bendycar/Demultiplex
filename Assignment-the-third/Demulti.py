#!/usr/bin/env python
import bioinfo
import argparse
import math
import gzip
import numpy as np
#import matplotlib.pyplot as plt Why on earth is this not working if I'm in my base environment and literally imported plt in pt1...
import itertools

def get_args():

    parser = argparse.ArgumentParser(description="Takes all 4 FASTQ files")
    parser.add_argument("-R1", help="Read 1", type = str, required = True)
    parser.add_argument("-R2", help="Read 2", type = str, required = True)
    parser.add_argument("-R3", help="Read 3", type = str, required = True)
    parser.add_argument("-R4", help="Read 4", type = str, required = True)
    parser.add_argument("-Q", help="QScore Quality cutoff", type = int, default=30)
    parser.add_argument("-O", help="Output directory", type = str, required = True)
    parser.add_argument("-I", help="Path to indices file", type = str, required = True)
    return parser.parse_args()
        
args = get_args()
R1 = args.R1
R2 = args.R2
R3 = args.R3
R4 = args.R4
QScore_cutoff = args.Q
output = args.O
Indices = args.I

def reverse_complement(DNA: str) -> str:
    '''Simply takes a DNA strand, validates it, and returns the reverse complement if it is a valid DNA string. Case insensitive.'''

    assert bioinfo.validate_base_seq(DNA), "Not a valid DNA sequence"
    complement = {"A" : "T", "T" : "A", "G" : "C", "C" : "G", "a" : "t", "t" : "a", "g" : "c", "c" : "g", "N" : "N", "n" : "N"}
    RC = ""

    for nucleotide in reversed(DNA):
        RC += complement[nucleotide]
    
    return RC

def average_QScore(phred_score: str) -> float:
    """Takes a string of ASCII + 33 encoded quality scores, returns average value"""
    running_total = 0
    for score in phred_score:
        value = bioinfo.convert_phred(score)
        running_total += value

    return running_total / len(phred_score)

def get_indices(index_location: str) -> set:
    '''Opens a properly formatted indices file at the path given through argparse, creates a set of the indices in this file'''
    
    valid_indices = set()

    with open(index_location, "r") as fh:
        fh.readline() #Gets rid of the first header line
        for line in fh:
            line = line.strip('\n')
            line = line.split('\t')
            index = line[4]
            valid_indices.add(index)
    
    return valid_indices


def get_RC_indices(indices: set) -> dict:
    '''The purpose of this function is to quickly convert the a valid index in R3 to its reverse complement, in order to append to header of matched index reads.
    If the index in R3 is unknown, we will have to manually create its reverse complement. However, this should dramatically speed up generating the RC for known indices.'''
    
    RC_valid_indices = {}

    for index in indices:
        RC_index = reverse_complement(index)
        RC_valid_indices[RC_index] = index #RC is the key because our input will be the RC index in read 3
    
    return RC_valid_indices

def open_files_for_writing(indices: set) -> tuple: #Tuple of two dictionaries, one for R1 and R2
    '''Creates all output files! These are saved for later use in the form of two dictionaries (R1 and R2).
    To write to the files, just call the appropriate dictioanry with either the Index (for matched reads) or "Unknown" / "Hopped"'''
    R1_files = {}
    R2_files = {}

    for index in indices:
        R1_files[index] = open(f"R1_{index}.fastq", "w")
        R2_files[index] = open(f"R2_{index}.fastq", "w")
    
    R1_files['Hopped'] = open(f"R1_Hopped.fastq", "w")
    R1_files['Unknown'] = open(f"R1_Unknown.fastq", "w")

    R2_files['Hopped'] = open(f"R2_Hopped.fastq", "w")
    R2_files['Unknown'] = open(f"R2_Unknown.fastq", "w")

    return R1_files, R2_files

def close_all_files(R1_files: dict, R2_files: dict) -> None:
    '''Just call at the end to close all files'''
    for file in R1_files:
        file_handle = R1_files[file]
        file_handle.close()
    
    for file in R2_files:
        file_handle = R2_files[file]
        file_handle.close()


def append_indices(Header: str, Index1: str, Index2: str) -> str:
    '''Appends Index 1 and the reverse complement of Index 2 to the header of the given record.
    Returns the modified header'''
    if matched == True or hopped == True: #Quickly gets the RC Index from the dictionary if it is a valid index
        RC_Index2 = RC_index_set[Index2]
        Header += f"_{Index1}_{RC_Index2}"
    else: #Manually create RC if it's not a valid index that we already have stored
        RC_Index2 = reverse_complement(Index2)
        Header += f"_{Index1}_{RC_Index2}"

    return Header

def write_record(record1: list, record2: list, Index: str) -> None:
    '''Writes to the appropriate R1 and R2 files based on the index and global variables related to matching status".
    Uses dictionaries generated by open_files_for_writing to find the correct file handles'''
    if matched == True:
        fhr1 = R1_files[Index] #Gets file handles from dictionary
        fhr2 = R2_files[Index]

        for line in record1:
            fhr1.write(f"{line}\n")
        for line in record2:
            fhr2.write(f"{line}\n")
    elif hopped == True:
        fhr1 = R1_files['Hopped']
        fhr2 = R2_files['Hopped']

        for line in record1:
            fhr1.write(f"{line}\n")
        for line in record2:
            fhr2.write(f"{line}\n")
    elif unknown == True:
        fhr1 = R1_files['Unknown']
        fhr2 = R2_files['Unknown']

        for line in record1:
            fhr1.write(f"{line}\n")
        for line in record2:
            fhr2.write(f"{line}\n")
    else:
        errors += 1

def output_stats(matched_counts: dict, hopped_counts: dict, unknown_counts: dict, errors: int) -> None:

    '''Creates output file with formatted display of relevant statistics'''
    pass

def update_counts(index1: str, index2: str) -> None:
    '''Takes index 1 and RC index 2, checks global booleans to see which case we're in then updates counts accordingly'''
    
    if unknown == True:
        if 'Unknown' in unknown_counts:
            unknown_counts['Unknown'] += 1
        else:
            unknown_counts['Unknown'] = 1
        
    elif hopped == True:
        if (index1, index2) in hopped_counts:
            hopped_counts[index1, index2] += 1
        else:
            hopped_counts[index1, index2] = 1
    elif matched == True:
        if (index1, index2) in matched_counts:
            matched_counts[index1, index2] += 1
        else:
            matched_counts[index1, index2] = 1

index_set = get_indices(Indices)
RC_index_set = get_RC_indices(index_set) #Dict where keys are RC index and values are corresponding original index

matched_counts = {}
hopped_counts = {}
unknown_counts = {}
errors = 0 #Increments only if something weird happens, should ideally be zero at the end
R1_files, R2_files = open_files_for_writing(index_set)

with open(R1, "r") as fh1, open(R2, "r") as fh2, open(R3, "r") as fh3, open(R4, "r") as fh4:
    while True:
        matched = False
        hopped = False
        unknown = False
        record1 = [fh1.readline().strip() for i in range(4)] #Calls the readline function 4 times -- easier for me to work with than modulo shenanigans
        record2 = [fh2.readline().strip() for i in range(4)]
        record3 = [fh3.readline().strip() for i in range(4)]
        record4 = [fh4.readline().strip() for i in range(4)]

        if not record1[0] or not record2[0] or not record3[0] or not record4[0]: #This line feels kinda sketchy, will test it thoroughly
            break

        if record2[1] not in index_set or record3[1] not in RC_index_set: #First check if either index is unknown
            unknown = True
            RC_index2 = reverse_complement(record3[1])
        elif average_QScore(record2[3]) < QScore_cutoff or average_QScore(record3[3]) < QScore_cutoff: #Next check if indices are known but poor quality
            unknown = True
            RC_index2 = reverse_complement(record3[1])
        elif RC_index_set[record3[1]] != record2[1]: #Checking if indices match. This is the whole point of creating the dictionary, so that I can check by looking at the dict rather than calling the RC function
            RC_index2 = RC_index_set[record3[1]]
            hopped = True
        elif RC_index_set[record3[1]] == record2[1]:
            RC_index2 = RC_index_set[record3[1]]
            matched = True
        else:
            errors += 1
        

        append_indices(record1[0], record2[1], RC_index2)
        append_indices(record4[0], record2[1], RC_index2)

        write_record(record1, record4, record2[1])
        update_counts(record2[1], RC_index2)
        
        record1 = []
        record2 = []
        record3 = []
        record4 = []

close_all_files(R1_files, R2_files)
#output_stats(matched_counts, hopped_counts, unknown_counts, errors)

#Notes to self 8/3/24: Should clean up main code by using variables instead of constantly referencing the list
#Getting key error in my append indices function, which is odd because it should never check the dictionary unless it's already been proven
#that the index exists within the dictionary...