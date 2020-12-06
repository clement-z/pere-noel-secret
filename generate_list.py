#!/usr/bin/env python3

"""
Generate list for secret santa from a (well-formed) CSV file

* Read people info from CSV file (see example provided)
* Assign to each another person at random
* Write the output as pairs of SimplePersons to results.pkl

By default, nothing is printed to stdout, only the pickled results are saved to
disk, to be reused with a script to send emails to the participants.
"""

import os
import csv
import random
import pickle

"""
Simple person class to hold name, email...
This is not really needed, but improves readability
"""
class SimplePerson():
    def __init__(self, name='', email='', address='', tel='', gender=''):
        self.name = name
        self.email = email
        self.address = address
        self.tel = tel
        self.gender = gender

    def __str__(self):
        return '[' + ' | '.join([self.name, self.email, self.address, self.tel, self.gender]) + ']'

"""
Read CSV → Shuffle order → Save results
"""
def main(coords_file='coords.csv', results_file='results.pkl', blacklist_file='blacklist.txt', verbose=False):
    with open(coords_file) as f:
        coords_rdr = csv.reader(f, delimiter='|')
        coords = []
        persons = []
        for row in coords_rdr:
            if row[0] == 'Nom':
                # Skip header if present
                continue
            coords.append(row)
            persons.append(SimplePerson(*row))

    rules = []
    if os.path.exists(blacklist_file):
        with open(blacklist_file, 'r') as f:
            for line in f:
                ids = [int(x) for x in line.split(' ')]
                print(f'{persons[ids[0]].name} will not be matched with {persons[ids[1]].name}')
                if len(ids) != 2:
                    print('invalid rule found')
                    return 1
                rules.append(set(ids))

    n = len(coords)
    id_from = list(range(n))
    id_to = list(range(n))

    if verbose:
        print(f'Found {n} persons:')
        print("\n".join(['\t' + str(person) for person in persons]))

    valid_output = False
    while not valid_output:
        random.shuffle(id_to)
        valid_output = True
        for (a,b) in zip(id_from, id_to):
            rule_broken = set((a,b)) in rules
            if rule_broken or a == b:
                valid_output = False
                break

    if verbose:
        print('Results:')
        for (i,j) in zip(id_from, id_to):
            print(f'{persons[i].name} → {persons[j].name} ({", ".join([persons[j].address, persons[j].tel]).strip(" ")})')

    results = []
    for (i,j) in zip(id_from, id_to):
        results.append((persons[i], persons[j]))

    with open(results_file, 'wb') as f:
        pickle.dump(results, f)

if __name__ == '__main__':
    main()
    #main(verbose=True)
