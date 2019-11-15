import setuptools


setuptools.setup(name='analogs_finder',
      version="1.2.0",
      url = "https://github.com/nostrumbiodiscovery/analogs_finder", 
      description='Retrieve analogs given a query molecule and a database.',
      author='Daniel Soler',
      author_email='daniel.soler@nostrumbiodiscovery.com',
      packages=setuptools.find_packages(),
      install_requieres=["numpy", "matplotlib", "jinja2", "umap", "mpld3", "sklearn", "tqdm"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )
