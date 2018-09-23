import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas.geometry import add_vectors
from compas.geometry import centroid_points
from compas.geometry import subtract_vectors

from compas.geometry import mesh_smooth_area
from compas.geometry import mesh_smooth_centroid

from compas_rhino.helpers import mesh_from_guid 
from compas_rhino.artists.meshartist import MeshArtist

if __name__ == '__main__':
    
    # select rhino mesh
    guid = rs.GetObject("Select mesh", 32)
    # create compas mesh object from rhino mesh
    mesh = mesh_from_guid(Mesh,guid)
    
    # set vertices on boundary as fixed
    fixed = set(mesh.vertices_on_boundary())
    
    # number of iterations
    kmax = 20
    for k in range(kmax):
        updated = {}
        # loop over all vertices
        for key in mesh.vertices():
            pt = mesh.vertex_coordinates(key)
            if key in fixed:
                # don't alter pt coordinates if fixed
                updated[key] = pt
            else:
                # get neighboring keys
                nbrs = mesh.vertex_neighbors(key)
                # get neighboring points
                pts_nbrs = [mesh.vertex_coordinates(nbr) for nbr in nbrs]
                # compute barycenter for neighboring points
                cent = centroid_points(pts_nbrs)
                # store new coordinates
                updated[key] = cent
                
        # update coordinates of all mesh vertices
        for key, attr in mesh.vertices(True):
            x, y, z = updated[key]
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
  
    # draw mesh
    artist = MeshArtist(mesh, layer='relaxed_mesh_laplacian')
    artist.draw()
    
