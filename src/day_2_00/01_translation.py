import rhinoscriptsyntax as rs

from compas.geometry import subtract_vectors
from compas.geometry import project_points_plane
from compas.geometry import add_vectors
from compas.geometry import scale_vector

from compas.datastructures import Mesh
from compas_rhino.artists.meshartist import MeshArtist

# Get inputs
crv_p = rs.GetObject("Select profile", 4)
crv_a = rs.GetObject("Select rail 1",4)

div_p = 20
div_r = 40

# divide profile and rail curve
pts_p = rs.DivideCurve(crv_p, div_p)
pts_a = rs.DivideCurve(crv_a, div_r)


# ------------------------------
# compas geometry function

# create planes along the rail curve
planes = []
for i in range(div_r):
    vec = subtract_vectors(pts_a[i + 1], pts_a[i])
    planes.append([pts_a[i], vec])

# subsequentely project profile curve to all planes
pts_uv = []
pts = pts_p
for i in range(div_r - 1):
    pts = project_points_plane(pts, planes[i])
    pts_uv.append(pts)

# create mesh object
trans_mesh = Mesh()

# add vertices
for u in xrange(len(pts_uv)):
    for v in xrange(len(pts_uv[u])):
        x, y, z = pts_uv[u][v]
        trans_mesh.add_vertex((u, v), x = x, y = y, z = z)

# add faces
for u in xrange(len(pts_uv)-1):
    for v in xrange(len(pts_uv[u])-1):
        trans_mesh.add_face([(u, v),(u + 1, v), (u + 1, v + 1), (u, v + 1)])

artist = MeshArtist(trans_mesh, layer='voussoir_hex')
artist.draw_faces(join_faces=True)

# create fins
#dis = 0.5
#for u, v in trans_mesh.edges():
#    normal_u = trans_mesh.vertex_normal(u)
#    normal_v = trans_mesh.vertex_normal(v)
#    pt1 = trans_mesh.vertex_coordinates(u)
#    pt2 = trans_mesh.vertex_coordinates(v)
#    pt3 = add_vectors(pt2, scale_vector(normal_v, dis))
#    pt4 = add_vectors(pt1, scale_vector(normal_u, dis))
#    rs.AddSrfPt([pt1, pt2, pt3, pt4])
    
