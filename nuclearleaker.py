#!/usr/bin/env python3
from requests import get
from bs4 import BeautifulSoup
from sys import argv
from sys import exit

#this function scrapes the data from
#nuclearleaks.com,parses it using
#BeautifulSoup and returns them as
#array of dictionaries
def NuclearLeaker(target):
    services = []
    url = "https://nuclearleaks.com"
    soup = BeautifulSoup(get(url).text,'html.parser')
    table = soup.find('table')
    for row in table.find_all('tr'):
            data = row.get_text(separator=':').split(":")
            if target in data[1].lower():
                site = {"entries":data[0],"database":data[1],
                "hashing-algorithm":data[2],"category":data[3],
                "dump-date":data[4] if len(data) == 5 else None,
                "acknowledgement":row.find('a')['href'] if len(data) == 6 else "No"
                }
                services.append(site.copy())
    return services

#this function just prints the results properly
def print_results(data):
    print("-----{} Result-----".format(data['database']))
    print("Entries: {}".format(data['entries']))
    print("Database: {}".format(data['database']))
    print("Hashing Algorithm: {}".format(data['hashing-algorithm']))
    print("Category: {}".format(data['category']))
    print("Dump date: {}".format(data['dump-date']))
    print("Acknlowledged?: {}".format(data['acknowledgement']))

if __name__ == "__main__":
    
    #checking if argument was provided
    if len(argv) < 2:
        print("Usage: {} *argument* *target*".format(argv[0]))
        print("arguments:")
        print("all - optional argument,you can")
        print("use it to display all results at once")
        exit(1)
    elif len(argv) == 3 and str(argv[1]) == "all":
        NL = NuclearLeaker(str(argv[2]))
        for i in range(len(NL)):
            print_results(NL[i])
    else:
        #spawning a menu and printing stuff
        NL = NuclearLeaker(argv[1])
        print("There are {} leaks related to {}".format(len(NL),str(argv[1])))
        if len(NL) == 0:
            exit(0)
        for i in range(len(NL)):
            print("[{}] {}".format(i,NL[i]["database"]))
        choice = input("which one to check? >")
        if len(NL) > int(choice):
            print_results(NL[int(choice)])
        else:
            print("invalid argument provided")
