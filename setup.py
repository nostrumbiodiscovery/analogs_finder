import setuptools


setuptools.setup(name='analogs_finder',
      version="1.0.0",
      url = "https//www.github.com/danielSoler93/analogs_finder", 
      description='Retrieve analogs given a query molecule and a database. \
               Several Methods (Tanimoto similarity, \
               substructure search, multi substructure search',
      author='Daniel Soler',
      author_email='daniel.soler@nostrumbiodiscovery.com',
      install_requires=[],
      packages=setuptools.find_packages(),
      classifiers=[
         "Programming Language :: Python3",
         "License :: OSI Approved :: MIT"
         "Operating System :: Linux" ]
     )
