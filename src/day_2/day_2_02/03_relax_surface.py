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
    
    # constrain all non-fixed to a surface
    for key, attr in mesh.vertices(data=True):
        if key in fixed:
            continue
        srf = attr['srf']
        x, y, z = rs.BrepClosestPoint(srf,mesh.vertex_coordinates(key))[0]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z
        
    conduit.redraw()

if __name__ == '__main__':
    
    guid = rs.GetObject("Select mesh", 32)
    srf = rs.GetObject("Select nurbs srf", 8)
    
    mesh = mesh_from_guid(Mesh,guid)
    fixed = set(mesh.vertices_on_boundary())

    # assign srf guid to all vertex attributes 
    mesh.update_default_vertex_attributes({'srf': srf})

    # initialize conduit
    conduit = MeshConduit(mesh, refreshrate=1)

    # run smoothing with conduit
    with conduit.enabled():
        mesh_smooth_centroid(mesh, 
                            fixed=fixed, 
                            kmax=100, 
                            damping=0.5, 
                            callback=callback)
        
    artist = MeshArtist(mesh, layer='relaxed_mesh_on_surface')
    artist.draw()
    
