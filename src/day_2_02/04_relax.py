import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas.geometry import mesh_smooth_area
from compas.geometry import mesh_smooth_centroid
from compas.utilities import geometric_key

from compas_rhino.helpers import mesh_from_guid 
from compas_rhino.utilities import get_point_coordinates
from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.conduits import MeshConduit

# callback function executed inside the smoothing loop
def callback(k, args):
    if k%10 == 0:
        rs.Prompt(str(k))
    
    # constrain all non-fixed to a surface
    for key, attr in mesh.vertices(data=True):
        if attr['fixed']:
            continue
            
        if attr['srf']:
            srf = attr['srf']
            x, y, z = rs.BrepClosestPoint(srf,mesh.vertex_coordinates(key))[0]
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
        elif attr['crv']:
            crv = attr['crv']
            x, y, z = rs.PointClosestObject(mesh.vertex_coordinates(key),[crv])[1]
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z

    conduit.redraw()

if __name__ == '__main__':
    
    
    guid = rs.GetObject("Select mesh", 32)
    srf = rs.GetObject("Select nurbs srf", 8)
    
    guid_pts = rs.ObjectsByLayer("fixed")
    pts_fixed = get_point_coordinates(guid_pts)
    guid_crvs = rs.ObjectsByLayer("edge_crvs")
    
    precision = '3f'
    
    pts_fixed_geo = set([geometric_key(pt,precision=precision) for pt in pts_fixed])
    
    mesh = mesh_from_guid(Mesh,guid)
    bound = set(mesh.vertices_on_boundary())

    fixed = []
    for key in mesh.vertices():
        # set initial vertex attribute
        mesh.set_vertex_attribute(key, 'fixed',False)
        mesh.set_vertex_attribute(key, 'srf',None)
        mesh.set_vertex_attribute(key, 'crv',None)
        
        if key in bound:
            pt = mesh.vertex_coordinates(key)
            pt_geo = geometric_key(pt, precision)
            if pt_geo in pts_fixed_geo:
                mesh.set_vertex_attribute(key, 'fixed', True)
                fixed.append(key)
            else:
                mesh.set_vertex_attribute(key, 'crv', rs.PointClosestObject(pt,guid_crvs)[0])
        else:
            mesh.set_vertex_attribute(key, 'srf', srf)
    

    # initialize conduit
    conduit = MeshConduit(mesh)

    # run smoothing with conduit
    with conduit.enabled():
        mesh_smooth_area(mesh, 
                            fixed=fixed, 
                            kmax=200, 
                            damping=0.5, 
                            callback=callback)
        
    artist = MeshArtist(mesh, layer='relaxed_mesh_on_surface')
    artist.draw()
    
