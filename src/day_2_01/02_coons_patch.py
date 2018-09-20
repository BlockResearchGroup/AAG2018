import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist


def sort_pts(sets_pts):
    # sorts point sets for coons patch

    # sort point sets in a "continous chain"
    start_pt = sets_pts[0][-1]
    new_sets_pts = [sets_pts[0]]
    sets_pts.pop(0)
    
    while sets_pts:
        for i, set_pts in enumerate(sets_pts):
            #alternative for a more "forgiving" point comparison
            #geometric_key(set_pts[0]) == geometric_key(start_pt)
            if set_pts[0] == start_pt:
                start_pt = set_pts[-1]
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
            elif set_pts[-1] == start_pt:
                start_pt = set_pts[0]
                set_pts.reverse()
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
                
    #coons patch sorting
    new_sets_pts[2].reverse()
    new_sets_pts[3].reverse()
                
    return new_sets_pts


if __name__ == '__main__':
    
    
    div = 15
    
    crvs = rs.GetObjects("Select four curves", 4)

    sets_pts = [rs.DivideCurve(crv, div) for crv in crvs]

    sets_pts = sort_pts(sets_pts)

    ab, bc, dc, ad = sets_pts
    points, faces = discrete_coons_patch(ab, bc, dc, ad)

    mesh = Mesh.from_vertices_and_faces(points, faces)
    
    artist = MeshArtist(mesh, layer='coons_mesh')
    artist.draw()

