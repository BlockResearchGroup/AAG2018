# AAG2018

## Getting started

**Install COMPAS**

* https://compas-dev.github.io/main/gettingstarted.html
* https://compas-dev.github.io/main/environments/rhino.html

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

2. Install compas_tna from source:

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

4. Test:

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

*We will list here the answers to recurring questions that come up during the workshop...*
