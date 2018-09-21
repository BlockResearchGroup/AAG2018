from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas.geometry import mesh_smooth_area

from compas_tna.diagrams import FormDiagram


# create a form diagram from a serialised file

form = FormDiagram.from_json('aag_01_formdiagram_from_mesh.json')


# smooth the diagram keeping some of the vertices fixed

fixed  = list(form.vertices_where({'is_anchor': True}))
fixed += list(form.vertices_where({'is_fixed': True}))
fixed += [key for fkey in form.faces_where({'is_loaded': False}) for key in form.face_vertices(fkey)]

fixed[:] = list(set(fixed))

mesh_smooth_area(form, fixed=fixed, kmax=50)


# serialise the result

form.to_json('aag_02_formdiagram.json')


# draw the result in the layer AAG > FormDiagram

form.draw(layer='AAG::FormDiagram')
