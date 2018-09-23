from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas.datastructures import Mesh
from compas.utilities import flatten

from numpy import array


mesh = Mesh.from_obj(compas.get('faces.obj'))

xyz = mesh.get_vertices_attributes('xyz')


# flatten the list of nested xyz coordinates
# [[x, y, z], [x, y, z], ...] => [x, y, z, x, y, z, ...]

xyz_1 = []

for x, y, z in xyz:
    xyz_1.append(x)
    xyz_1.append(y)
    xyz_1.append(z)

xyz_2 = []

for point in xyz:
    xyz_2.extend(point)  # xyz_2 += point

xyz_3 = [axis for point in xyz for axis in point]

xyz_4 = list(flatten(xyz))

xyz_5 = array(xyz).flatten().tolist()


print(xyz_1[0:3])
print(xyz_2[0:3])
print(xyz_3[0:3])
print(xyz_4[0:3])
print(xyz_5[0:3])


# get the x, y, z column vectors of the nx3 matrix xyz
# [[x, y, z], [x, y, z], ...] => [x, x, ...], [y, y, ...], [z, z, ...]

X_1 = []
Y_1 = []
Z_1 = []

for x, y, z in xyz:
    X_1.append(x)
    Y_1.append(y)
    Z_1.append(z)

X_2 = [x for x, _, _ in xyz]
Y_2 = [y for _, y, _ in xyz]
Z_2 = [z for _, _, z in xyz]

X_3, Y_3, Z_3 = list(zip(*xyz))

X_4, Y_4, Z_4 = array(xyz).T.tolist()

print(X_1[0:3], Y_1[0:3], Z_1[0:3])
print(X_2[0:3], Y_2[0:3], Z_2[0:3])
print(X_3[0:3], Y_3[0:3], Z_3[0:3])
print(X_4[0:3], Y_4[0:3], Z_4[0:3])


# count the number of unique x, y, z coordinates up to 3-digit precision



