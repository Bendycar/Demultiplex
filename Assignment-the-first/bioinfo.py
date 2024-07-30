#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
'''

__version__ = "0.4"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set('ATGCNatcgn')
RNA_bases = set('AUGCNaucgn')

def convert_phred(letter: str) -> int:
    """Converts a single character into a phred score"""
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    """Takes a sequence of ASCII encoded Phred + 33 scores, returns their average value."""
    if len(phred_score) == 0:
        return 0
    score_totals = 0
    for score in phred_score:
        value = convert_phred(score)
        score_totals += value

    return score_totals / len(phred_score)

def validate_base_seq(seq: str,RNAflag: bool=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq)<=(RNA_bases if RNAflag else DNA_bases) #set <= is the same thing as issubset


def gc_content(DNA: str, RNAflag: bool=False) -> float:
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    assert validate_base_seq(DNA,RNAflag), "Not a valid DNA or RNA sequence"
    
    DNA = DNA.upper()
    gc_count = DNA.count("G")+DNA.count("C")
    return gc_count/len(DNA)

def calc_median(lst: list) -> float:
    '''Takes an ALREADY SORTED list, returns the median'''
    left = 0
    right = len(lst) - 1

    while left < right:
        left += 1
        right -= 1

    if left == right: #Odd numbered list
        return lst[left]
    else: #Even numbered list, only possible case should be left > right
        return (lst[left] + lst[right]) / 2

def oneline_fasta(read, write):
    '''Takes a FASTA file and returns a new FASTA file with no line breaks between sequences'''
    with open(write, "w") as ofh:
        with open(read, "r") as fh:
            prev = fh.readline() #Prev would be undefined if we began on line 1
            for line in fh: #Starts on line 2 of file because fh acts like a generator function, already gave line 1 to prev
                curr = line 
                if prev.startswith(">") or curr.startswith(">"): #If prev is a header or the last line before the header
                    ofh.write(prev) #Either way we just want to write prev including the newline character
                else:
                    ofh.write(prev.strip('\n')) #If prev is a sequence line before another sequence line, we want to remove newline char
                prev = curr #Increments prev, the loop will increment curr
            ofh.write(prev) #Loop will terminate once curr is empty, prev will be the last line of file

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert qual_score("!!!!!!!!!") == 0, "Wrong quality score"
    assert qual_score("++55") == 15, "Wrong quality score"
    assert qual_score("") == 0, "Can't handle empty string"
    print("Quality score works correctly")

    assert validate_base_seq("atcgtagtatagacatt") == True, "Fails for lowercase DNA"
    assert validate_base_seq("agacaguguguca", True) == True, "Fails for lowercase RNA"
    assert validate_base_seq("ATGCAGTACGGACTGAC") == True, "Fails for uppercase DNA"
    assert validate_base_seq("AUGCGUCGUACUGUAC", True) == True, "Fails for uppercase RNA"
    assert validate_base_seq("NSDLDFKHPASINA;DIUFHFA98H") == False, "Incorrectly identifies incorrect uppercase string"
    assert validate_base_seq("skdfn;asoidfhsa") == False, "Incorrectly identifies incorrect lowercase string"
    assert validate_base_seq("SDNPF8W048THPEAAFAS]FPA[]", True) == False, "Incorrectly identifies incorrect uppercase string with RNA flag"
    assert validate_base_seq("naldkhpad98hnd;oi8p,asdf", True) == False, "Incorrectly identifies incorrect lowercase string with RNA flag"
    print("Validate base seq works!")

    assert gc_content("atgcatgcatgcatgcatgc") == .5, "Fails for lowercase DNA"
    assert gc_content("augcaugcaugcaugc", True) == .5, "Fails for lowercase RNA"
    assert gc_content("TTTTGGGGCCCCGGGG") == .75, "Fails for uppercase DNA"
    assert gc_content("UUUUGGGGCCCCGGGG", True) == .75, "Fails for uppercase RNA"
    try:
        gc_content("a;kcjnpa98ughb'd")
    except:
        print("GC content works beautifully")
    

    assert calc_median([0,0,0,0,0,0,0]) == 0, "Fails for list of zeros"
    assert calc_median([1,2,3,4,5]) == 3, "Fails for odd numbered list"
    assert calc_median([1,2,3,4]) == 2.5, "Fails for even numbered list DNA"
    assert calc_median([1]) == 1, "Fails on single number"
    print("Calc median works")