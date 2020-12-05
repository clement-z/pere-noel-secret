#! python3

import random
import csv

with open('coords.csv') as f:
    coords_rdr = csv.reader(f, delimiter='|')
    coords = []
    for row in coords_rdr:
        coords.append(row)

n = len(coords)
id_from = list(range(n))
id_to = list(range(n))

while True:
    random.shuffle(id_to)
    if all([a != b for (a,b) in zip(id_from, id_to)]):
        break

for (i,j) in zip(id_from, id_to):
    print(f'{coords[i][0]} → {coords[j][0]} ({", ".join(coords[j]).strip(" ")})')

with open('out.csv', 'w') as f:
    f.write(f'Père Noël|Enfant\n')
    f.write('-|Nom|Adresse|Tel.\n')
    for (i,j) in zip(id_from, id_to):
        f.write(f'{coords[i][0]}|{"|".join(coords[j]).strip(" ")}\n')

print('')
print('Display saved output with: `cat out.csv | column -t -s"|"`')
