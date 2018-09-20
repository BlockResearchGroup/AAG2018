import rhinoscriptsyntax as rs

from compas.geometry import discrete_coons_patch

from compas.utilities import geometric_key

from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist

if __name__ == '__main__':
    
    
    div = 15
    
    crvs = rs.GetObjects("Select four curves (in order)", 4)

    sets_pts = [rs.DivideCurve(crv, div) for crv in crvs]

    ab, bc, dc, ad = sets_pts
    points, faces = discrete_coons_patch(ab, bc, dc, ad)

    mesh = Mesh.from_vertices_and_faces(points, faces)
    
    artist = MeshArtist(mesh, layer='coons_mesh')
    artist.draw()

