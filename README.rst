Analogs Finder
##############

.. image:: https://travis-ci.com/danielSoler93/analogs_finder.svg?branch=master
       :target: https://travis-ci.com/danielSoler93/analogs_finder

.. image:: https://anaconda.org/nostrumbiodiscovery/analogs_finder/badges/version.svg
       :target: https://anaconda.org/nostrumbiodiscovery/analogs_finder


Description
##############
This script is intended to retrieve analogs given a query molecule (sdf) and a database (sdf).

Installation
##############

1) pip install analogs_finder

2) export SCHRODINGER=/opt/schrodinger2019-1/

3) Use it freely!


Functionalities
################


Command for n most similar structures:
---------------------------------------

    - **Explanation**

     Given a database.sdf and a molecule.sdf will output the n most similar structures to the query molecule (--n_structs to specify the number of outputted structures)

    - **Example**

     python -m analogs_finder.mainpy <database (sdf)> <query_molecule (sdf)> --sb --n <number of output structs> --output <outputname>

     python -m analogs_finder.main analogs_finder/examples/database.py analogs_finder/examples/substructre_1.sdf  --most_similars --n 20 --output most_similars.sdf



Command for Tanimoto similarity higher than treshold
------------------------------------------------------

    - **Explanation**

     Will retrieve all molecules on the database.sdf that has a tanimoto similarity higher than treshold in respect to the query molecule (0.7 by default, you can specify by --tresh 0.6)

    - **Example**

       python -m analogs_finder.main <database (sdf)> <query_molecule (sdf)> --treshold tanimoto_treshold --output <outputname>

       python -m analogs_finder.main analogs_finder/examples/actives_final.sdf  analogs_finder/examples/substructre_1.sdf --output most_similars.sdf --tresh 0.7



Command to search for  one or more substructure
--------------------------------------------------

    - **Explanation**

       For each entry in database.py search for the substructure/s present in the query_molecule.sdf

    - **Example**

       python -m analogs_finder.main <database (sdf)> <substructure_moleculeS (sdf with several entries (substructures)> --substructure --output <outputname>

       python analogs_finder.main analogs_finder/examples/actives_final.sdf analogs_finder/examples/substructre_1.sdf --output most_similars.sdf --substructure



Command to search for at least one of the substructures in each sdf file
-------------------------------------------------------------------------



    - **Explanation**

       If sdfile_1 (n molecules inside) and sdfile_2 (n molecules inside) will retrieve all molecules inside database.sdf that match at least one substructure inside EACH sdf file.

    - **Example**

        python -m analogs_finder.main <database (sdf)> <substructure_moleculeS (several sdfs with several entries> --combi_search --output <outputname>


         python -m analogs_finder.main  analogs_finder/examples/active.sdf analogs_finder.main/examples/substructre_* --output most_similars.sdf --combi_subsearch


Phase Screening
--------------------


    - **Explanation**

       Given a query molecule and a database, build pharmacophore hypotesis from the query molecule and screen the database to match this hypotesis.

    - **Example**

        python -m analogs_finder.rank_method.phase --database <database (sdf)> --query_molec <1 sdf molecule> --nominimization --match 4 (match 4 out of total pharmacophores)


        python -m analogs_finder.rank_method.phase --database analogs_finder/examples/active.sdf --query_molec analogs_finder.main/examples/substructre_1.py
