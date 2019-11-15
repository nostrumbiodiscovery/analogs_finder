#Clean and build
rm -r dist build analogs_finder.egg*
python setup.py sdist
twine upload dist/*
~                     
