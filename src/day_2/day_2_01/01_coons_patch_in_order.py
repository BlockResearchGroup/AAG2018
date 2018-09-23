import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist

if __name__ == '__main__':
    
    # division in both directions
    div = 15
    
    # select curves
    crvs = rs.GetObjects("Select four curves (in cw order)", 4)
    
    # divide curves
    sets_pts = [rs.DivideCurve(crv, div) for crv in crvs]

    # create coons patch
    ab, bc, dc, ad = sets_pts
    points, faces = discrete_coons_patch(ab, bc, dc, ad)

    # create mesh object from points and faces
    mesh = Mesh.from_vertices_and_faces(points, faces)
    
    # draw coons mesh
    artist = MeshArtist(mesh, layer='coons_mesh')
    artist.draw()

