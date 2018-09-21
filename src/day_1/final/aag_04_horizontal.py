from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas.utilities import i_to_green

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist
from compas_tna.rhino import DiagramHelper

from compas_tna.equilibrium import horizontal_nodal_rhino as horizontal


# create diagrams from serialised files

form = FormDiagram.from_json('aag_02_formdiagram_smooth_area.json')
force = ForceDiagram.from_json('aag_03_forcediagram.json')


# draw the diagrams

form.draw(layer='AAG::FormDiagram')
force.draw(layer='AAG::ForceDiagram')


# compute horizontal equilibrium

# form.set_edges_attribute('lmin', 0.2)
form.set_edges_attribute('fmin', 0.2)
form.set_edges_attribute('fmax', 5.0)

horizontal(form, force, alpha=100, kmax=1000)


# draw the diagrams

form.draw(layer='AAG::FormDiagram')
force.draw(layer='AAG::ForceDiagram')


# visualise angle deviations

angles = form.get_edges_attribute('a')
amin = min(angles)
amax = max(angles)
adif = amax - amin

text = {}
color = {}

for u, v, attr in form.edges_where({'is_edge': True}, True):
    a = attr['a']
    if a > 5:
        text[u, v] = "{:.1f}".format(a)
        color[u, v] = i_to_green((a - amin) / adif)

artist = FormArtist(form, layer='AAG::FormDiagram')

artist.clear_edgelabels()
artist.draw_edgelabels(text=text, color=color)

artist.redraw()

# serialise the result

form.to_json('aag_04_formdiagram_horizontal.json')
force.to_json('aag_04_forcediagram_horizontal.json')
