#!/bin/bash

#Analysis
python -m analogs_finder.main database.sdf substructre_1.sdf  --analysis --dim_type pca --test

#Nmost similar structs
python -m analogs_finder.main database.sdf substructre_1.sdf  --sb --n 20 --output most_similars.sdf

#Tanimoto search
python -m analogs_finder.main database.sdf  substructre_1.sdf --output most_similars.sdf --tresh 0.7

#Search substructure
python -m analogs_finder.main database.sdf substructre_1.sdf --output most_similars.sdf --substructure

#Search for at least one substructure in each sdf file
python -m analogs_finder.main database.sdf substructre_*.sdf --output most_similars.sdf --combi_subsearch

#Hybrid
python -m analogs_finder.main database.sdf substructre_2.sdf --output most_similars.sdf --hybrid substructure_1.sdf

#Types fp
python -m analogs_finder.main database.sdf substructre_2.sdf --output most_similars.sdf --hybrid substructure_1.sdf --fp_type circular

#Use all fingerprints one job
python -m analogs_finder.main database.sdf substructre_1.sdf --tresh 0.7 0.4 0.7 0.27 --fp_type DL circular torsions MACCS

#Turbo Search
python -m analogs_finder.main database.sdf substructre_1.sdf --turbo --neighbours 5 --tresh 0.7 --fp_type circular


