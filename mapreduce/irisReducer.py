#!/usr/bin/env python3
import sys

current_species = None
species_count = 0
petalLengthCm_species_total = 0.0

# read tab-delimited key-value pairs from stdin
for row in sys.stdin:
    row = row.strip()
    if not row:
        continue

    species, petalLengthCm = [x.strip() for x in row.split('\t')]
    petalLengthCm = float(petalLengthCm)
    
    # if species is same as previous row
    if species == current_species:
        petalLengthCm_species_total += petalLengthCm
        species_count += 1
    else:
        # if species is different from previous row
        if current_species:
            avg = petalLengthCm_species_total / species_count
            print(f"{current_species}\t{avg:.2f}")
        current_species = species
        petalLengthCm_species_total = petalLengthCm
        species_count = 1

# print last species after loop ends
if current_species:
    avg = petalLengthCm_species_total / species_count
    print(f"{current_species}\t{avg:.2f}")