# AAG2018 Workshop 3

*Architectural Geometry and Structural Design with COMPAS*

![Armadillo workflow](images/aag2018_ws3_BRG.jpg)


## Schedule


### Day 1

*Structural design of a thrust network with **compas_tna***

0. Form diagram from lines
1. Form diagram from mesh
2. Form diagram smoothing
3. Force diagram from form diagram
4. Horizontal equilibrium
5. Vertical equilibrium
6. Force distribution


### Day 2

*Fabrication design of a discrete vault*

Details coming soon...


## Getting started


**Install COMPAS**

* https://compas-dev.github.io/main/gettingstarted.html
* https://compas-dev.github.io/main/environments/rhino.html

*Note*

To update use:

```bash

$ pip install COMPAS --upgrade

```

**Install compas_tna**

1. Clone the repo:

```bash

$ git clone https://github.com/BlockResearchGroup/compas_tna.git

```

The folder `compas_tna` will contain the following:

* data
* docs
* docsource
* examples
* src
* temp

And a bunch of other files...

2. Install **compas_tna** from source:

```bash

$ cd compas_tna
$ pip install -e .

```

**Configure Rhino**

1. In Rhino go to:

```

Tools > PythonScript > Edit > Tools > Options

```

2. Add the path to `compas_tna/src` (see above) to the *Module Search Paths*.

3. Restart Rhino...

4. Test, by making a script with the following two lines and running it in Rhino. If there are no errors, all is well :)

```python

import compas
import compas_tna

```


## Interactive drawings

[eQUILIBRIUM](http://block.arch.ethz.ch/eq)

* [Single panel truss](http://block.arch.ethz.ch/eq/drawing/view/36)
* [Funicular line through two points](http://block.arch.ethz.ch/eq/drawing/view/5)
* [Minimum and maximum thrust in a masonry arch](http://block.arch.ethz.ch/eq/drawing/view/16)


## Reading

* [Geometry-based Understanding of Structures](http://block.arch.ethz.ch/brg/publications/399)
* [Algebraic Graph Statics](http://block.arch.ethz.ch/brg/publications/413)
* [Thrust Network Analysis: A new methodology for three-dimensional equilibrium](http://block.arch.ethz.ch/brg/publications/355)
* [Form Finding to Fabrication: A digital design process for masonry vaults](http://block.arch.ethz.ch/brg/publications/368)
* [Armadillo Vault - An extreme discrete stone shell](http://block.arch.ethz.ch/brg/publications/646)


## Questions

> Q: `conda` commands don't work.

Try running them from the *Conda Prompt*.
Depending on how you installed Anaconda, it might not be available by default on the normal Windows command prompt.

> Q: When trying to install the framework in Rhino, it fails indicating the lib folder of IronPython does not exist.

Make sure you have opened Rhino 6 and Grasshopper at least once, so that it finishes setting up all its internal folder structure.

> Q: It fails when trying to install on Rhino.

Try starting the command prompt as administrator.
Depending on the version of Python, it might be required or not.

> Q: I have no administrator access to my computer.

First, install COMPAS from source following the instructions described in the [DevGuide](https://compas-dev.github.io/main/devguide.html).
Then, manually add `path/to/COMPAS/src` to the Rhino Python search paths.
