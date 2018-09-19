
import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas.geometry import is_point_in_polygon_xy

from compas.geometry import mesh_cull_duplicate_vertices

from compas.topology import delaunay_from_points
from compas.topology import trimesh_remesh

from compas.utilities import geometric_key

from compas_rhino.utilities import xdraw_mesh

from compas_rhino import get_line_coordinates
from compas_rhino.artists.meshartist import MeshArtist


__author__    = 'Matthias Rippmann'
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'rippmann@ethz.ch'


def join_meshes(meshes, cull_duplicates=False, precision='3f'):
    """Join multiple meshes.

    Parameters
    ----------
    meshes : Meshes
        A list of mesh objects.
    cull_duplicates: Boolean
        True if resulting duplicate vertices should be deleted
        False otherwise
    """
    
    count = 0
    mesh_all = Mesh()
    map = {}
    for mesh in meshes:
        faces = list(mesh.faces())
        vertices = list(mesh.faces())
                        
        for key, attr in mesh.vertices(True):
            mesh_all.add_vertex(count, x=attr['x'], y=attr['y'], z=attr['z'], attr_dict=attr)
            map[key] = count
            count += 1
            
        for fkey,attr in mesh.faces(True):
            vertices = mesh.face_vertices(fkey)
            new_vertices = [map[key] for key in vertices]
            mesh_all.add_face(new_vertices)
    
    if cull_duplicates:
        mesh_cull_duplicate_vertices(mesh_all, precision)

    return mesh_all
    

if __name__ == '__main__':
    
    #user inputs
    #----------------------------------------
    #----------------------------------------
    precision = '3f'
    trg_length = .75

    #select all boundaries and internal crease curves
    crvs = rs.GetObjects("Select boundary and crease curves", 4, group=True, preselect=False, select=False, objects=None, minimum_count=3, maximum_count=0)
    #select optional openings
    crvs_openings = rs.GetObjects("Select optional openings (must be closed curves)", 4, group=True, preselect=False, select=False, objects=None)
    
    #----------------------------------------
    #----------------------------------------
    
    #create a inital mesh from the boundary and crease curves
    lines = get_line_coordinates(crvs)
    geo_lines = [(geometric_key(pt_u,precision), geometric_key(pt_v,precision)) for pt_u, pt_v in lines]
    mesh = Mesh.from_lines(lines, delete_boundary_face=True, precision=precision)
    
    #assign curve guids to mesh edges
    for u,v, attr in mesh.edges(True):
        pt_u, pt_v = mesh.edge_coordinates(u,v)
        geo_u, geo_v = geometric_key(pt_u,precision), geometric_key(pt_v,precision)
        for i, geo_l_uv in enumerate(geo_lines):
            geo_l_u, geo_l_v = geo_l_uv[0], geo_l_uv[1]
            if (geo_l_u == geo_u) and (geo_l_v == geo_v) or (geo_l_u == geo_v) and (geo_l_v == geo_u):
                attr['guid'] = str(crvs[i])
                break
                
    #compute ordered polygons per face
    for fkey, attr in mesh.faces(True):
        
        #divide curves per edge based on target length
        edges = mesh.face_halfedges(fkey)
        edge_crvs = [mesh.get_edge_attribute((u,v),'guid') for u,v in edges]
        edge_crvs_pts = [rs.DivideCurve(crv, max(rs.CurveLength(crv) / trg_length, 1)) for crv in edge_crvs]
        
        #check and adjust ordering of points per edge
        pt_geo = geometric_key(mesh.vertex_coordinates(edges[0][0]),precision)
        for i in range(len(edge_crvs_pts)):
            if geometric_key(edge_crvs_pts[i][-1],precision) == pt_geo:
                edge_crvs_pts[i].reverse()
            pt_geo = geometric_key(edge_crvs_pts[i][-1],precision)
            
        #delete duplicates / form polygons per face
        polygon = []
        for edge_crv_pts in edge_crvs_pts:
             polygon += edge_crv_pts[1:]
        attr['polygon'] = polygon
        
    #process holes/openings
    if not crvs_openings: crvs_openings = []
        
    #divide curves per hole based on target length
    crvs_openings_pts = [rs.DivideCurve(crv, max(rs.CurveLength(crv) / trg_length, 3)) for crv in crvs_openings]
    
    #check which holes are inside which face / assign holes to faces
    for fkey, attr in mesh.faces(True):
        polygon = attr['polygon']
        holes = []
        for crvs_opening_pts in crvs_openings_pts:
            if is_point_in_polygon_xy(crvs_opening_pts[0], polygon):
                holes.append(crvs_opening_pts)
                # could be more efficient since holes already 
                # assigned to another face are checked again
        attr['hole_polygons'] = holes
    
    #create triangular mesh for each face
    delaunay_meshes = []
    count = 1
    for fkey, attr in mesh.faces(True):
        polygon = attr['polygon']
        holes = attr['hole_polygons']
        #create flat list of all points
        points = polygon + [item for hole in holes for item in hole]
        
        #compute initial delaunay mesh based on all points for the current face
        faces = delaunay_from_points(points, boundary=polygon, holes=holes)
        delaunay = Mesh.from_vertices_and_faces(points, faces)
    
        rs.Prompt('Computing triangular mesh for face {} of {}'.format(count, mesh.number_of_faces()))
        
        #compute the remeshed delaunay for the current face
        trimesh_remesh(
            delaunay,
            target=trg_length,
            tol=0.05,
            kmax=300,
            allow_boundary_split=False,
            allow_boundary_swap=True,
            verbose=False
        )
        
        delaunay_meshes.append(delaunay)
        count += 1
        
    #join all meshes created per face
    mesh_diagram = join_meshes(delaunay_meshes, cull_duplicates=True, precision=precision)
    
    artist = MeshArtist(mesh_diagram, layer='form_tri')
    artist.draw_faces()
    artist.draw_vertices()
    artist.redraw()
                

