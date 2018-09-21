import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.helpers import mesh_from_guid 

from compas_rhino.helpers import mesh_select_edges

def delete_edges(mesh,joint_lines):
    
    for u, v in joint_lines:
        # get neigboring faces
        fkey_1 = mesh.halfedge[u][v]
        fkey_2 = mesh.halfedge[v][u]
        
        # check if edge is not at the boundary
        if fkey_1 and fkey_2:
            
            # find vertices of new face (union of faces fkey_1 and fkey_2)
            vertices_1 = mesh.face_vertices(fkey_1)
            vertices_2 = mesh.face_vertices(fkey_2)
            
            lines_1 = mesh.face_halfedges(fkey_1)
            lines_2 = mesh.face_halfedges(fkey_2)
            
            dup_key_1, dup_key_2 = list(set(vertices_1) & set(vertices_2))
            dup_lines = set([(dup_key_1, dup_key_2), (dup_key_2, dup_key_1)])
            
            # lines/halfedges without edge to be deleted
            lines = list(dup_lines ^ set(lines_1 + lines_2))
            
            # sort halfedges to continous polyline (new face)
            new_vertices = list(lines[0])
            lines.pop(0)
            while True:
                new_key = None
                for i,uv in enumerate(lines):
                    if new_vertices[-1] == uv[0]:
                        new_key = uv[1]
                        lines.pop(i)
                        break
                
                if not new_key:
                    break
                    
                new_vertices.append(new_key)
           
           # delete old faces
            mesh.delete_face(fkey_1)
            mesh.delete_face(fkey_2)
            
            # create new face
            mesh.add_face(new_vertices, fkey=fkey_1)


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
    
    
    guid = rs.GetObject("Select mesh", 32)
    mesh = mesh_from_guid(Mesh,guid)

    # draw edges for selection
    artist = MeshArtist(mesh, layer='edges')
    artist.draw_edges()
    artist.redraw()
    
    # select edge
    edges = mesh_select_edges(mesh)
    
    # clear edges
    artist.clear_edges()
        
    # find "every second" edge (joint lines)
    joint_lines = []
    for i, uv in enumerate(edges):
        para_edges = get_parallel_edges(mesh,uv)
        for u, v in para_edges[i%2::2]:
            joint_lines.append((u,v))
            
    # delete edges from mesh
    delete_edges(mesh,joint_lines)
            
    # draw joint lines
    artist.draw_edges()
    artist.redraw()
