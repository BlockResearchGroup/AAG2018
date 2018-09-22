import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh
from compas.datastructures.mesh.operations import meshes_join 

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino import get_line_coordinates


if __name__ == '__main__':
    
    precision = '3f'
    
    # target length
    trg_len = 0.7
    
    crvs = rs.GetObjects("Select curves", 4)
    lines = get_line_coordinates(crvs)
    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    # start and end points of all curves
    geo_lines = [(geometric_key(pt_u,precision), geometric_key(pt_v,precision)) for pt_u, pt_v in lines]

    coons_meshes = []
    # looping over all face keys
    for fkey in mesh.faces():
        sets_crvs = []
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
                    crv_data = (crvs[i], rs.CurveLength(crvs[i]), True) 
                elif (geo_l_u == geo_v) and (geo_l_v == geo_u): # not aligned with edge
                    crv_data = (crvs[i], rs.CurveLength(crvs[i]), False) 
                    
            sets_crvs.append(crv_data)
            
        # find division based on the average length of curves opposite one another
        div_u = int(((sets_crvs[0][1] + sets_crvs[2][1]) / 2) / trg_len)
        div_v = int(((sets_crvs[1][1] + sets_crvs[3][1]) / 2) / trg_len)
        
        sets_pts = []
        for i, crv_data in enumerate(sets_crvs):
            if i%2==0: # use u/v division for even and odd edges
                div = div_u
            else:
                div = div_v
            # divide curve and reverse point if not aligned with edge
            pts = rs.DivideCurve(crv_data[0],div)
            if not crv_data[2]: pts.reverse()
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

