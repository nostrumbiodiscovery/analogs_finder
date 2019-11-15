#Clean after build
pip uninstall analogs_finder --yes
pip uninstall -r requirements.txt --yes
pip install analogs_finder
cd tests
python -m pytest test_analysis.py test_fingerprints.py test_fusions.py test_methods.py test_helpers.py
