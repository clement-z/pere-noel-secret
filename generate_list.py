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

    n = len(coords)
    id_from = list(range(n))
    id_to = list(range(n))

    print(f'[INFO] Found {n} valid entries in {coords_file}:')
    print('\n'.join(['[INFO]\t- ' + str(person) for person in persons]))

    rules = []
    if os.path.exists(blacklist_file):
        with open(blacklist_file, 'r') as f:
            for line in f:
                line = line.rstrip()
                try:
                    ids = [int(x) for x in line.split(' ')]
                except ValueError:
                    # rule contains something not convertivle to an integer
                    print(f'[ERROR] invalid rule found (need two different integers separated by spaces): {line!r}')
                    return 1

                # same numbers
                if ids[0] == ids[1]:
                    print(f'[ERROR] invalid rule found (need different numbers): {line!r}')
                    return 1

                # not 2 numbers
                if len(ids) != 2:
                    print(f'[ERROR] invalid rule found (need exactly two numbers but found {len(ids)}): {line!r}')
                    return 1

                # numbers higher than total head count
                if ids[0] >= len(persons) or ids[1] >= len(persons):
                    print(f'[ERROR] rule refers to persons #{ids[0]} and #{ids[1]} but only {len(persons)} specified in coords file: {line!r}')
                    return 1
                rules.append(set(ids))

        print(f'[INFO] Found {len(rules)} rules in {blacklist_file}:')
        for rule in rules:
            print(f'[INFO]\t- {persons[list(rule)[0]].name} will not be matched with {persons[list(rule)[1]].name}')

    valid_output = False
    while not valid_output:
        random.shuffle(id_to)
        valid_output = True
        for (a,b) in zip(id_from, id_to):
            rule_broken = set((a,b)) in rules
            if rule_broken or a == b:
                valid_output = False
                break

    print('[INFO] List generated')

    if verbose:
        print('[DEBUG] Results:')
        for (i,j) in zip(id_from, id_to):
            print(f'[DEBUG]\t- {persons[i].name} → {persons[j].name} ({", ".join([persons[j].address, persons[j].tel]).strip(" ")})')

    results = []
    for (i,j) in zip(id_from, id_to):
        results.append((persons[i], persons[j]))

    with open(results_file, 'wb') as f:
        pickle.dump(results, f)

    print(f'[INFO] Results saved in: {results_file}')

if __name__ == '__main__':
    main()
    #main(verbose=True)
