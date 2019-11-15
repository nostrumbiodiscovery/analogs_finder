#Clean and reinstall requirements
rm -r dist
pip uninstall -r requirements.txt --yes
pip uninstall analogs_finder --yes
pip install cython numpy setuptools
pip install .

#Clean and build
rm -r dist build analogs_finder.egg*
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
~                     
