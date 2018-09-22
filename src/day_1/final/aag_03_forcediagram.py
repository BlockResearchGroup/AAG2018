from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import DiagramHelper


# create a form diagram from a serialised file

form = FormDiagram.from_json('aag_02_formdiagram.json')


# create a force diagram from the form diagram

force = ForceDiagram.from_formdiagram(form)


# visualise the result

force.draw(layer='AAG::ForceDiagram')


# move the force diagram to a different location

DiagramHelper.move(force)

force.draw(layer='AAG::ForceDiagram')


# fix one of the force diagram vertices to keep it there in the future

key = DiagramHelper.select_vertex(force)

if key is not None:
    DiagramHelper.update_vertex_attributes(force, [key])


# redraw the force diagram

force.draw(layer='AAG::ForceDiagram')


# and serialise the result

force.to_json('aag_03_forcediagram.json')
