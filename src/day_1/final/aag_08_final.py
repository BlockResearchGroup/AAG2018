from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas.utilities import i_to_green

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist


# create diagrams from serialised files

form = FormDiagram.from_json('aag_08_final_formdiagram.json')
force = ForceDiagram.from_json('aag_08_final_forcediagram.json')


# draw the result

form.draw(layer='AAG::FormDiagram')
force.draw(layer='AAG::ForceDiagram')

artist = FormArtist(form, layer='AAG::FormDiagram')

artist.clear_reactions()
artist.draw_reactions(scale=0.25)
artist.draw_forces(scale=0.01)

artist.redraw()
