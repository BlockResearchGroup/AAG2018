import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas.geometry import mesh_smooth_area
from compas.geometry import mesh_smooth_centroid

from compas_rhino.helpers import mesh_from_guid 
from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.conduits import MeshConduit

# callback function executed inside the smoothing loop
def callback(k, args):
    if k%10 == 0:
        rs.Prompt(str(k))
        
    conduit.redraw()


if __name__ == '__main__':
    
    # select rhino mesh
    guid = rs.GetObject("Select mesh", 32)
    # create compas mesh object from rhino mesh
    mesh = mesh_from_guid(Mesh,guid)
    
    # set vertices on boundary as fixed
    fixed = set(mesh.vertices_on_boundary())

    # initialize conduit
    conduit = MeshConduit(mesh, refreshrate=1)

    # run smoothing with conduit
    with conduit.enabled():
        mesh_smooth_centroid(mesh, 
                            fixed=fixed, 
                            kmax=100, 
                            damping=0.5, 
                            callback=callback)
    # draw mesh
    artist = MeshArtist(mesh, layer='relaxed_mesh_laplacian')
    artist.draw()
    
