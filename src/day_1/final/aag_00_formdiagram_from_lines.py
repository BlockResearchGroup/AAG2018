from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas_tna.diagrams import FormDiagram
from compas_tna.rhino import DiagramHelper


# create a form diagram from a set of lines

guids = compas_rhino.select_lines()
lines = compas_rhino.get_line_coordinates(guids)
form  = FormDiagram.from_lines(lines)


# identify the supports
# as the vertices that lie on the support curves

guids = compas_rhino.select_curves()
keys  = DiagramHelper.identify_vertices_on_curves(form, guids)

form.set_vertices_attribute('is_anchor', True, keys)


# update the boundaries to include the horizontal reaction forces

form.update_boundaries()


# serialise the result

form.to_json('aag_00_formdiagram_from_lines.json')


# draw the result in the layer AAG > FormDiagram

form.draw(layer='AAG::FormDiagram')
