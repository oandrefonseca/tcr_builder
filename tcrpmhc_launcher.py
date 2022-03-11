#!/usr/bin/python
"""tcrpmhc_launcher.py: Description."""

__author__ = "Finn"
__maintainer__ = "Andre, Finn"

import os
import sys
from os import listdir as ls

import wget
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

def create_project_directory(project_name):
    """ Description """

    project_directory = os.path.join(os.getcwd(), project_name)
    if os.path.exists(project_directory):
        quit(f'The {project_name} folder already exists and cannot be overwritten')
    else:
        print(f"Creating {project_directory}")
        os.mkdir(project_directory)

    return project_directory

def setting_cookies(driver):
    """ Description """

    print(f"--- Settings cookies")
    try:
        accept = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "cookiescript_accept"))
        )
        accept.click()
    except:
        quit("Please, check the cookies pop-up.")
    
    time.sleep(10)

def modeller_key(driver, default_key = 'MODELIRANJE'):
    """ Description """

    print(f"--- Adding modeller key")
    try:
        modellerkey = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.NAME, "modellerkey"))
        )
        modellerkey.send_keys(default_key)
    except:
        quit("Please, check your modeller_key field.")

def wget_download(url_data, project_directory, complexname):
    """ Description """

    filename = os.path.basename(url_data)

    if 'results' not in filename:
        output = os.path.join(project_directory, filename.replace('model', complexname))
    else:
        output = os.path.join(project_directory, filename.replace('results', complexname))

    wget.download(url_data, out = output)

def running_tcrpmhc(driver, project_directory, fasta_input):
    """ Description """

    try:
        driver.switch_to.frame(0)
        fasta = driver.find_element(By.ID, "uploadfile")
        fasta.send_keys(fasta_input)

        modeller_key(driver)
    except:
        quit('Please, check the fasta input.')

    # Submit button
    time.sleep(5)
    print(f"--- Submiting job {fasta_input}")

    submit_btn = driver.find_element(By.XPATH, "//input[@type='submit']") 
    submit_btn.click()

    try:
        # Waiting 5 minutes
        download_btn = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/nav/div[2]/ul[2]/div/a"))
        )

        downloaded = []
        elem_href = driver.find_elements_by_xpath("//a[@href]")
       
        complexname = os.path.basename(fasta_input).replace('.fasta', '')
        print(f"--- Download model from {complexname}")
        time.sleep(20)

        for href in elem_href:
            url_data = href.get_attribute("href")
            for ext in ['.pdb', '.csv', '.pir', '.json']:
                if url_data.endswith(ext) and url_data not in downloaded:
                    downloaded.append(url_data)
                    wget_download(url_data, project_directory, complexname)
    except:
        quit("The download failed. Try it again later.")

    time.sleep(20)

    driver.back()
    driver.refresh()

def main(project_name, fasta_directory):
    """ Description """
    if project_name:
        project_directory = create_project_directory(project_name)
    
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://services.healthtech.dtu.dk/service.php?TCRpMHCmodels-1.0")
        time.sleep(5)
    except:
        quit("Please check your Chrome webdriver.")

    # Setting cookies
    setting_cookies(driver)

    fasta_directory = os.path.abspath(fasta_directory)
    print(f"\nScanning {fasta_directory}")

    fasta_list = [fasta_input for fasta_input in ls(fasta_directory)]
    for fasta_input in fasta_list:
        if fasta_input.endswith('.fasta'):
            print(f"-- Processing {fasta_input}.")
            running_tcrpmhc(driver, project_directory, os.path.abspath(fasta_input))

    if not fasta_list:
        quit("Please, provide a directory with fasta files.")

    print("\nThat's all folks!")
    driver.quit()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])