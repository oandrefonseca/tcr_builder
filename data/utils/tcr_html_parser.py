#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
# from selenium import webdriver

# https://selenium-python.readthedocs.io/getting-started.html

def main():
    """ Extracting VDJ sequences from TCRModel website """
    
    try:
        with open('./data/TCRmodel.html', 'r') as fh:
            soup = BeautifulSoup(fh, "html.parser") 
            soup = soup.find(id = 'Paris') # Form with TCR sequences

            specie_check = 0
            for specie_option in ['aspecies', 'bspecies']:
                specie_name = soup.find(id = specie_option)
                specie_name = specie_name.find('option', selected = True)
                if specie_name.text == 'Human':
                    specie_check += 1

            if specie_check == 2:
                for elements in soup.find_all("option"):
                    if elements.text.startswith('TR'):
                        print(elements.text, elements['value'], sep = "\t")
    except:
        quit("Please, download manually TCR Model page at https://tcrmodel.ibbr.umd.edu/index")

if __name__ == "__main__":
    main()