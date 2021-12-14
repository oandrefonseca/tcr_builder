#!/usr/bin/python

import sys
import csv
from Bio import SeqIO
import pickle
from pprint import pprint

def imgt_database():
    ''' Description '''

    try:
        with open('./data/IMGT_HLA.pickle', 'rb') as fh:
            imgt_dictionary = pickle.load(fh)
    except:
        quit("Please check IMGT_HLA.pickle file")

    return imgt_dictionary

def tcr_database():
    ''' Description '''

    try:
        with open('./data/TCRModel.pickle', 'rb') as fh:
            tcr_dictionary = pickle.load(fh)
    except:
        quit("Please check TCRModel.pickle file")

    return tcr_dictionary

def main(template):
    ''' Description 
    
    tcr_name,cdr3_alpha,cdr3_beta,v_and_d_alpha,j_alpha,v_and_d_beta,j_beta,peptide,imgt_hla
    tcr0001,AAAAAAAAAAAAAAAAAAAAAA,BBBBBBBBBBBBBBBBBBBBBB,TRAV1-1*01,TRAJ1*01,TRBV10-1*01,TRBJ1-1*01,PPPPPPPPP,HLA00005

    '''

    tcr_dictionary = tcr_database()
    imgt_dictionary = imgt_database()

    with open(template, 'r') as csvfile:
        spamreader = csv.DictReader(csvfile)
        for row in spamreader:
            try:
                complex_sequence = {
                    'Alpha' : tcr_dictionary[row['v_and_d_alpha']] + row['cdr3_alpha'] + tcr_dictionary[row['j_alpha']],
                    'Beta' : tcr_dictionary[row['v_and_d_beta']] + row['cdr3_beta'] + tcr_dictionary[row['j_beta']],
                    'peptide': row['peptide'],
                    row['imgt_hla'] : imgt_dictionary[row['imgt_hla']]
                }
            except:
                quit("Soemthing went wrong!")


            # pprint(complex_sequence)

            with open(f"./output/{row['tcr_name']}.fasta", "w") as fw:
                for chain, sequence in complex_sequence.items(): 
                    fw.write(f">{row['tcr_name']}_" + chain + "\n" + sequence + "\n")


if __name__ == "__main__":
    main(sys.argv[1])