#!/usr/bin/python

import sys
from Bio import SeqIO
import pickle
from pprint import pprint

def main(imgt_fasta):
    """ Parsing VDJ database to a TCR Builder input """

    imgt_dict = {}
    with open(imgt_fasta, 'r') as fh:
        for record in SeqIO.parse(fh, "fasta"):
            imgt_dict.setdefault(record.id.replace('HLA:', ''), str(record.seq))
    
    with open('IMGT_HLA.pickle', 'wb') as imgt_dump:
        pickle.dump(imgt_dict, imgt_dump, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main(sys.argv[1])