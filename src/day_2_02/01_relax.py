import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas.geometry import mesh_smooth_area
from compas.geometry import mesh_smooth_centroid

from compas_rhino.helpers import mesh_from_guid 
from compas_rhino.artists.meshartist import MeshArtist

if __name__ == '__main__':
    
    guid = rs.GetObject("Select mesh", 32)
    
    mesh = mesh_from_guid(Mesh,guid)
    
    fixed = set(mesh.vertices_on_boundary())
    
    mesh_smooth_centroid(mesh, fixed=fixed, kmax=100, damping=0.5, callback=None, callback_args=None) 
    artist = MeshArtist(mesh, layer='relaxed_mesh_laplacian')
    artist.draw()
    
#    mesh_smooth_area(mesh, fixed=fixed, kmax=100, damping=0.5, callback=None, callback_args=None)
#    artist = MeshArtist(mesh, layer='relaxed_mesh_area')
#    artist.draw()
