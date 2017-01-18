"""
Given a ;-delimited csv file (with a header) having at least the columns:

scopus1;scopus2;scopus3

this script queries Scopus for each ScopusID associated with a given author,
producing a ;-delimited csv file titled 'papers_[SCOPUSID_1].csv' located in
'../Data/' and structured as:

Author;PaperID;Citations;Year;Journal

for each author.
"""

import requests
import json
import os
import csv

## an api key for scopus can be obtained at https://dev.elsevier.com/sc_apis.html
API_KEY = ""

def process_results(results, author_id):
    """Parse the JSON file received from Scopus to extract the relevant
       information for each author"""
    tmp = []
    for r in results['search-results']["entry"]:
        try:
            scopus_id = str(r['dc:identifier']).split("SCOPUS_ID:")[1]
        except:
            scopus_id = "" # ignore records with no Scopus ID
        try:
            cits = str(r['citedby-count'])
        except:
            cits = "0"
        try:
            yrpub = str(r['prism:coverDate']).split('-')[0]
        except:
            yrpub = "1900" # ignore papers with nonsense dates
        try:
            pubname = str(r['prism:publicationName'].replace(';', ''))
        except:
            pubname = "Not available"
        tmp.append([author_id, scopus_id, cits, yrpub, pubname])
    return tmp


def get_all_papers(scopus1, scopus2, scopus3, counter):
    """For a given set of Scopus IDs, query Scopus to download records for each
       of their papers"""
    global API_KEY
    ## initialize the output file
    filename = "../Data/papers_" + scopus1 + ".csv"
    ## check whether file already exists (do not overwrite) and continue
    ## if there is at least one Scopus ID associated with the author
    if scopus1 != "" and os.path.isfile(filename) == False:
        ## Get the first 200 papers authored by the SCOPUS_ID
        resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus1 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200",
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': API_KEY})
        ## use the json package to parse the raw input
        results = resp.json()
        ## further parse using 'process_results()'
        table = process_results(results, scopus1)
        ## get the total number of publications on scopus by this Scopus ID
        totitems = int(results['search-results']['opensearch:totalResults'])
        ## if there are more than 200 articles, increment the counter and loop
        ## through the pages
        counter = 200
        while totitems > counter:
            resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus1 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200&start=" + str(counter),
                        headers={'Accept':'application/json',
                                 'X-ELS-APIKey': API_KEY})
            results = resp.json()
            table = table + process_results(results, scopus1)
            counter = counter + 200
        ## also add papers written by alternative Scopus IDs associated with the
        ## same author
        if scopus2 != "":
            resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus2 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200",
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': API_KEY})
            results = resp.json()
            table = table + process_results(results, scopus1)
            totitems = int(results['search-results']['opensearch:totalResults'])
            counter = 200
            while totitems > counter:
                resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus2 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200&start=" + str(counter),
                        headers={'Accept':'application/json',
                                 'X-ELS-APIKey': API_KEY})
                results = resp.json()
                table = table + process_results(results, scopus1)
                counter = counter + 200
        if scopus3 != "":
            resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus3 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200",
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': API_KEY})
            results = resp.json()
            table = table + process_results(results, scopus1)
            totitems = int(results['search-results']['opensearch:totalResults'])
            counter = 200
            while totitems > counter:
                resp = requests.get("http://api.elsevier.com/content/search/scopus?query=AU-ID(" + scopus3 + ")+AND+DOCTYPE(ar)&field=dc:identifier,prism:publicationName,citedby-count,prism:coverDate&count=200&start=" + str(counter),
                        headers={'Accept':'application/json',
                                 'X-ELS-APIKey': API_KEY})
                results = resp.json()
                table = table + process_results(results, scopus1)
                counter = counter + 200

        f = open(filename, "w")
        f.write(";".join(['Author', 'PaperID', 'Citations', 'Year', 'Journal']) + "\n")
        for r in table:
            f.write(";".join(r) + "\n")
        f.close()

"""Open a csv file containing the Scopus IDs to search for (with synonymous IDs
   ;-delimited on the same line, and nonsynonymous IDs separated by newlines)
   and loop through the file, calling 'get_all_papers()' for each ID"""
with open("../inputs/Members_SelectedSections.csv") as in_file:
    ## read in as dictionary
    all_rows = csv.DictReader(in_file, delimiter = ";")
    counter = 1
    for row in allrows:
        ## progress indicating output
        print(counter, row["FullName"], row["Section"], row["Scopus1"],row["Scopus2"],row["Scopus3"])
        ## analyze the Scopus IDs for each author
        get_all_papers(row["Scopus1"], row["Scopus2"], row["Scopus3"], counter)
        counter = counter + 1
