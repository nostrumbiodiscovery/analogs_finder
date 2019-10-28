import setuptools


setuptools.setup(name='analogs_finder',
      version="1.1.0",
      url = "https://github.com/nostrumbiodiscovery/analogs_finder", 
      description='Retrieve analogs given a query molecule and a database.',
      author='Daniel Soler',
      author_email='daniel.soler@nostrumbiodiscovery.com',
      packages=setuptools.find_packages(),
      install_requires=["mpld3", "tqdm"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )
