import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.helpers import mesh_from_guid 
from compas_rhino.helpers import mesh_select_edges
from compas_rhino import get_line_coordinates

def get_parallel_edges(mesh, uv):
    # fist parallel edge is the one selected
    edges = [uv]

    u, v = uv
    # process from edge uv in both directions
    for a,b in [(u, v) ,(v, u)]:
        
        # search until a boundary or the starting edge is reached
        while True:
            # face on one side of the edge
            fkey = mesh.halfedge[a][b]
            
            # check for boundary
            if fkey is None:
                break
                
            # get all vertices of the face
            vertices = mesh.face_vertices(fkey)
            
            # for a quad mesh we know exactly the opposite face edge
            i = vertices.index(a)
            a = vertices[i - 1]
            b = vertices[i - 2]
            
            # check if the starting edge is reached
            if (a, b) in edges or (b, a) in edges:
                break

            edges.append((a, b))
            
    # check for the right uv tuples. Ordered as in mesh.edges()
    edgeset = set(list(mesh.edges()))
    return [(u, v) if (u, v) in edgeset else (v, u) for u, v in edges]

if __name__ == '__main__':
    
    edge_crvs = rs.GetObjects("Select tessellation edges", 4)
    lines = get_line_coordinates(edge_crvs)
    
    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    # draw edges for selection
    artist = MeshArtist(mesh, layer='joint_lines')
    artist.draw_edges()
    artist.redraw()
    
    # select edge
    rs.HideObjects(edge_crvs)
    edges = mesh_select_edges(mesh)
    rs.ShowObjects(edge_crvs)
    
    # clear edges
    artist.clear_edges()
        
    # find "every second" edge (joint lines)
    joint_lines = []
    for i, uv in enumerate(edges):
        para_edges = get_parallel_edges(mesh,uv)
        for u, v in para_edges[i%2::2]:
            joint_lines.append((u,v))
            
    # draw joint lines
    artist.draw_edges(keys=joint_lines, color=(255,0,0))
    artist.redraw()
