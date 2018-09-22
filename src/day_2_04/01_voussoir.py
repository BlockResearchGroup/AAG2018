import copy

import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas_rhino.artists.meshartist import MeshArtist

from compas_rhino.utilities import get_line_coordinates
from compas.geometry import mesh_smooth_centroid

from compas.geometry import scale_vector
from compas.geometry import add_vectors


from compas.utilities import geometric_key 

if __name__ == '__main__':
    
    thickness = 0.2
    
    edge_crvs = rs.GetObjects("Select edges", 4)
    lines = get_line_coordinates(edge_crvs)
    
    mesh = Mesh.from_lines(lines, delete_boundary_face=True)
    
    # compute offset points 
    for key in mesh.vertices():
        pt = mesh.vertex_coordinates(key)
        normal = mesh.vertex_normal(key)
        pt_a = add_vectors(pt, scale_vector(normal, thickness * .5))
        pt_b = add_vectors(pt, scale_vector(normal, thickness * -.5))
        mesh.set_vertex_attribute(key, 'point_a', pt_a)
        mesh.set_vertex_attribute(key, 'point_b', pt_b)
    
    for fkey in mesh.faces():
        vertices = mesh.face_vertices(fkey)
        pts_a = [mesh.get_vertex_attribute(key, 'point_a') for key in vertices]
        pts_b = [mesh.get_vertex_attribute(key, 'point_b') for key in vertices]
        
        # initialize mesh for voussoir
        mesh_v = Mesh()
        # vertices for voussoir
        for pt in pts_a + pts_b:
            x,y,z = pt
            mesh_v.add_vertex(key=geometric_key(pt), x=x, y=y, z=z)
        
        # side surfaces
        for i, _ in enumerate(pts_a):
            face = [geometric_key(pts_a[i - 1]),
                        geometric_key(pts_b[i - 1]),
                        geometric_key(pts_b[i]),
                        geometric_key(pts_a[i])]
            mesh_v.add_face(face)
        
        # top and bottom surface
        face = [geometric_key(pt) for pt in pts_a]
        mesh_v.add_face(face)
        face = [geometric_key(pt) for pt in pts_b[::-1]]
        mesh_v.add_face(face)
        
        artist = MeshArtist(mesh_v, layer='voussoir_hex')
        artist.draw_faces(join_faces=True)
        
    artist.redraw()

            
 
