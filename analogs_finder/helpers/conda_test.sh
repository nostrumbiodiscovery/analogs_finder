conda uninstall analogs_finder
conda install -c conda-forge -c rdkit -c nostrumbiodiscovery analogs_finder --yes
cd tests
python -m pytest test_analysis.py test_fingerprints.py test_fusions.py test_methods.py test_helpers.py

