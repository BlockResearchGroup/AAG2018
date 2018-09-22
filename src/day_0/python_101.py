from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas.datastructures import Mesh

mesh = Mesh.from_obj(compas.get('faces.obj'))

xyz = mesh.get_vertices_attributes('xyz')


# flatten the list of nested xyz coordinates
# [[x, y, z], [x, y, z], ...] => [x, y, z, x, y, z, x, y, z, ...]


# get the x, y, z column vectors of the nx3 matrix xyz
# [[x, y, z], [x, y, z], ...] => [x, x, x, ...], [y, y, y, ...], [z, z, z, ...]


# count the number of unique x, y, z coordinates up to 3-digit precision
