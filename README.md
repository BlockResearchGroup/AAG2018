# AAG2018

## Getting started

**Install COMPAS**

* https://compas-dev.github.io/main/gettingstarted.html
* https://compas-dev.github.io/main/environments/rhino.html

**Install compas_tna**

Clone the repo:

	$ git clone https://github.com/BlockResearchGroup/compas_tna.git

The folder `compas_tna` will contain the following:

* data
* docs
* docsource
* examples
* src
* temp

And a bunch of other files...

Install compas_tna from source:

	$ cd compas_tna
	$ pip install -e .


**Configure Rhino**

In Rhino go to:

	Tools > PythonScript > Edit > Tools > Options

Add the path to `compas_tna/src` (see above) to the *Module Search Paths*.

Restart Rhino...
