import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas_rhino.artists.meshartist import MeshArtist

from compas_rhino.utilities import get_line_coordinates
from compas.geometry import mesh_smooth_centroid


if __name__ == '__main__':
    
    
    edge_crvs = rs.GetObjects("Select edges", 4)
    lines = get_line_coordinates(edge_crvs)
    
    mesh = Mesh.from_lines(lines, delete_boundary_face=True)
    
    fixed = set(mesh.vertices_on_boundary())
    mesh_smooth_centroid(mesh, fixed=fixed, kmax=1, damping=0.5)
    
    # draw edges for selection
    artist = MeshArtist(mesh, layer='edges_hex')
    artist.draw_edges()
    artist.redraw()
    
 
