import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist


def sort_pts(sets_pts):
    # sorts point sets for coons patch

    # sort point sets in a "continous chain"
    end_pt = sets_pts[0][-1]
    new_sets_pts = [sets_pts[0]]
    sets_pts.pop(0)
    
    while True:
        flag = True
        for i, set_pts in enumerate(sets_pts):
            if geometric_key(set_pts[0]) == geometric_key(end_pt):
                end_pt = set_pts[-1]
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
                flag = False
            elif geometric_key(set_pts[-1]) == geometric_key(end_pt):
                end_pt = set_pts[0]
                set_pts.reverse()
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
                flag = False
                
        if flag: break
        
                
    #coons patch sorting
    new_sets_pts[2].reverse()
    new_sets_pts[3].reverse()
                
    return new_sets_pts

if __name__ == '__main__':
    
    # division in both directions
    div = 15
    
    # select curves
    crvs = rs.GetObjects("Select four curves (in cw order)", 4)
    
    # divide curves
    sets_pts = [rs.DivideCurve(crv, div) for crv in crvs]

    # sort points
    sets_pts = sort_pts(sets_pts)

    # create coons patch
    ab, bc, dc, ad = sets_pts
    points, faces = discrete_coons_patch(ab, bc, dc, ad)

    # create mesh object from points and faces
    mesh = Mesh.from_vertices_and_faces(points, faces)
    
    # draw coons mesh
    artist = MeshArtist(mesh, layer='coons_mesh')
    artist.draw()


