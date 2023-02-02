"""
Carroll_WebScraper2023.py
Author: Sam Carroll
Date: 1/23/2023
"""

from bs4 import BeautifulSoup
import requests
import time
import os

# Initializes an empty set to hold scraped links.
url_set = set()

"""
Uses functions from requests and BeautifulSoup
to parse HTMP data.
Parameters:
   domain (String) - The domain all scraped links are to be within.
   URL (String) - The URL scraping is to begin at.
Author - Sam Carroll
"""
def soup_parse(domain, URL):
    # Initializes an empty set to hold the result set.
    b_set = set()

    # Returns an HTML document through an HTTP request.
    r = requests.get(URL)

    # Isolates all HTML links from the document.
    soup = BeautifulSoup(r.text, 'html.parser')
    a_set = soup.find_all('a')

    for link in a_set:
        # Isolates the link itself from HTML code.
        new_link = link.get('href')

        # Verifies that the link is within the domain and adds it to the result set.
        if str(new_link).startswith(domain):
            b_set.add(new_link)
        elif str(new_link).startswith('/'):
            b_set.add(domain + str(new_link))

    # Returns the result set.
    return b_set

"""
Scrapes the web and saves harvested URLs to a set.
Parameters:
   domain (String) - The domain all scraped links are to be within.
   URL (String) - The URL scraping is to begin at.
   depth (Integer) - The current depth.
   max_depth (Integer) - The maximum depth for scraping.
Author - Sam Carroll
"""
def scrape(domain, URL, depth, max_depth):
    # Base case.
    # Adds returned links to the result set.
    # Does not follow links, as the maximum depth has been reached.
    if depth == max_depth:
        # Returns a list of links from the URL.
        # As soup_parse() already verifies that links are within the domain,
        # a check is not necessary here.
        a_set = soup_parse(domain, URL)

        # Adds returned links to the result set.
        for link in a_set:
            url_set.add(link)

            print(str(len(url_set))+ ' | Depth = ' + str(depth) + ' | ' + str(link))

    # Recursive case.
    # Adds returned links to the result set.
    # Follows links at an incremented depth in order to scrape more links.
    else:
        # Returns a list of links from the URL.
        # As soup_parse() already verifies that links are within the domain,
        # a check is not necessary here.
        a_set = soup_parse(domain, URL)

        for link in a_set:
            # Adds returned links to the result set.
            url_set.add(link)

            print(str(len(url_set)) + ' | Depth = ' + str(depth) + ' | ' + str(link))

            # Recursively calls scrape() at an incremented depth.
            if '.mp4' not in str(link) and '.png' not in str(link) and '.jpg' not in str(link) and '.pdf' not in str(link):
                scrape(domain, link, depth + 1, max_depth)

"""
Writes the saved set of scraped URLs to a text file
within the current working directory.
Author - Sam Carroll
"""
def write_to_file():
    # Removes the text file if it exists in the
    # working directory.
    # Added for speed/testing purposes.
    if os.path.exists('Links.txt'):
        os.remove('Links.txt')

    # Creates a text file to hold links.
    with open('Links.txt', 'w') as f:
        for link in url_set:
            f.write(link + '\n')

"""
Takes user input to prepare for scraping.
Author - Sam Carroll
"""
def take_input():
    # Takes a domain, URL, and depth.
    domain = input('Enter a domain: ')
    startURL = input('Enter a starting URL: ')
    depth = input("Enter a maximum depth: ")

    # Appends the https prefix if not included.
    if not domain.startswith('https://'):
        domain = 'https://' + domain

    if not startURL.startswith('https://'):
        startURL = 'https://' + startURL

    # Begins scraping.
    starter(domain, startURL, int(depth))

"""
Completes setup for and begins scraping.
Input:
   domain - The domain all scraped links are to be within.
   URL - The URL scraping is to begin at.
   depth - The maximum depth for scraping.
Author - Sam Carroll
"""
def starter(domain, URL, depth):
    # Creates a beginning timestamp.
    first_stamp = time.time()

    # Begins scraping at an initial depth of 0.
    scrape(domain, URL, 0, depth)

    # Creates an ending timestamp.
    last_stamp = time.time()

    # Calcualtes the elapsed time.
    elapsed_time = int(last_stamp - int(first_stamp))

    # Writes the scraped links to a text file 
    # in the current working directly.
    write_to_file()

    # Prints closing message.
    path = os.getcwd() + '/Links.py'

    # Prints closing message.
    print('\n')
    print('\n')
    print(str(len(url_set)) + ' links were scraped from ' + domain + '.')
    print('Scraping took ' + str(elapsed_time) + ' seconds.')
    print('A list of collected links can be found at ' + path)

# Takes user input and begins the program.
take_input()