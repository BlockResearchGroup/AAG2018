import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh
from compas.datastructures.mesh.operations import meshes_join 

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino import get_line_coordinates


if __name__ == '__main__':
    
    precision = '3f'
    
    crvs = rs.GetObjects("Select curves", 4)
    lines = get_line_coordinates(crvs)
    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    # start and end points of all curves
    geo_lines = [(geometric_key(pt_u,precision), geometric_key(pt_v,precision)) for pt_u, pt_v in lines]

    coons_meshes = []
    # looping over all face keys
    for fkey in mesh.faces():
        sets_pts = []
        # checking if the edge direction u->v matches with the curve object
        # divide curve based on division given
        # loop over edges per face
        for uv in mesh.face_halfedges(fkey): 
            pt_u, pt_v = mesh.edge_coordinates(uv[0],uv[1])
            geo_u, geo_v = geometric_key(pt_u,precision), geometric_key(pt_v,precision)
            # loop over all start and end points of the guid crvs
            for i, geo_l_uv in enumerate(geo_lines):
                geo_l_u, geo_l_v = geo_l_uv[0], geo_l_uv[1]
                if (geo_l_u == geo_u) and (geo_l_v == geo_v): # aligned with edge
                    div = int(rs.ObjectName(crvs[i])) # division by name
                    pts = rs.DivideCurve(crvs[i], div)
                elif (geo_l_u == geo_v) and (geo_l_v == geo_u): # not aligned with edge
                    div = int(rs.ObjectName(crvs[i])) # division by name
                    pts = rs.DivideCurve(crvs[i], div)
                    # reverse direction of point list
                    pts.reverse()
            sets_pts.append(pts)

        #coons patch sorting
        sets_pts[2].reverse()
        sets_pts[3].reverse()
        ab, bc, dc, ad = sets_pts
        points, faces = discrete_coons_patch(ab, bc, dc, ad)
    
        coons_meshes.append(Mesh.from_vertices_and_faces(points, faces))

    # join individual coons meshes
    coons_mesh = meshes_join(coons_meshes, cull_duplicates=True, precision=precision)
    
    # draw mesh
    artist = MeshArtist(coons_mesh, layer='coons_mesh')
    artist.draw()

