from compas.datastructures import Mesh

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.helpers import mesh_select_face


if __name__ == '__main__':
    
    # get mesh from json
    mesh = Mesh.from_json('tessellation_mesh.json')

    # draw tessellation mesh
    artist = MeshArtist(mesh, layer='tessellation_mesh')  
    artist.draw_edges()
    artist.draw_facelabels()
    artist.redraw()
   
    # select a face
    fkey = mesh_select_face(mesh, message='Select face.')
    
    artist.clear_facelabels()
    
    # find neighboring faces
    fkeys = list(mesh.face_neighbors(fkey)) + [fkey]
    for fkey in fkeys:
        # get voussoir meshes stored as face attribute
        data = mesh.get_face_attribute(fkey, 'voussoir')
        voussoir_mesh = Mesh.from_data(data)
        # draw neighboring voussoir mesh
        artist = MeshArtist(voussoir_mesh, layer='voussoir_meshes')
        artist.draw_faces(join_faces=True)
    