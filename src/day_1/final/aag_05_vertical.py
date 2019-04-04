from __future__ import print_function

import os
import compas
import compas_rhino
import compas_tna

compas_tna.TEMP = os.path.join(os.path.dirname(__file__), 'tmp')

from compas.utilities import i_to_green

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist
from compas_tna.rhino import DiagramHelper

from compas_tna.equilibrium import vertical_from_zmax_rhino as vertical


# create diagrams from serialised files

form = FormDiagram.from_json('aag_04_horizontal_formdiagram.json')
force = ForceDiagram.from_json('aag_04_horizontal_forcediagram.json')


# compute the scale of the force diagram
# such that the highest vertex of the form diagram is at a prescribed value

zmax = 3

scale = vertical(form, zmax, kmax=100)

force.attributes['scale'] = scale

print(scale)

# draw the result

form.draw(layer='AAG::FormDiagram')

artist = FormArtist(form, layer='AAG::FormDiagram')

artist.clear_reactions()
artist.draw_reactions(scale=0.25)
artist.draw_forces(scale=0.01)

artist.redraw()


# serialise the data

form.to_json('aag_05_vertical_formdiagram.json')
force.to_json('aag_05_vertical_forcediagram.json')
