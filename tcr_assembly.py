#!/usr/bin/python

import sys
import csv
from Bio import SeqIO

def tcr_database():
    ''' Description '''

    tcr_dictionary = {}
    with open('./data/TCR_database.tsv') as fh:
        for row in fh:
            columns = list(map(lambda field: field.strip(), row.split()))
            tcr_dictionary.setdefault(
                columns[0], columns[1]
            )
    return tcr_dictionary

def main(template):
    ''' Description 
    
    tcr_name,cdr3_alpha,cdr3_beta,v_and_d_alpha,j_alpha,v_and_d_beta,j_beta
    tcr0001,AAAAAAAAAAAAAAAAAAAAAA,BBBBBBBBBBBBBBBBBBBBBB,TRAV1-1*01,TRAJ1*01,TRBV10-1*01,TRBJ1-1*01

    '''

    tcr_dictionary = tcr_database()

    with open(template, 'r') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            try:
                tcr_sequence = {
                    'Alpha' : tcr_dictionary[row['v_and_d_alpha']] + row['cdr3_alpha'] + tcr_dictionary[row['j_alpha']],
                    'Beta' : tcr_dictionary[row['v_and_d_beta']] + row['cdr3_beta'] + tcr_dictionary[row['j_beta']]
                }
            except:
                quit("Soemthing went wrong!")

            with open(f"./output/{row['tcr_name']}.fasta", "w") as fw:
                for chain, sequence in tcr_sequence.items(): 
                    fw.write(f">{row['tcr_name']}_" + chain + "\n" + sequence + "\n")


if __name__ == "__main__":
    main(sys.argv[1])