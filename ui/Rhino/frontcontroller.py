from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import compas
import compas_rhino
import compas_tna

from compas.utilities import i_to_red
from compas.utilities import i_to_green
from compas.utilities import i_to_blue
from compas.utilities import i_to_rgb

from compas.geometry import mesh_smooth_area

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist
from compas_tna.rhino import DiagramHelper

from compas_tna.equilibrium import horizontal_nodal_rhino as horizontal
from compas_tna.equilibrium import vertical_from_zmax_rhino as vertical


HERE = os.path.abspath(os.path.dirname(__file__))

try:
    import rhinoscriptsyntax as rs
except ImportError:
    pass


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['TNAFrontController']


class TNAFrontController(object):

    instancename = 'tna'

    def __init__(self):
        self.form = None
        self.force = None
        self.settings = {
            'form.layer'       : 'AAG::FormDiagram',
            'force.layer'      : 'AAG::ForceDiagram',
            'horizontal.alpha' : 100,
            'horizontal.kmax'  : 200,
            'vertical.zmax'    : 3,
        }

    def init(self):
        pass

    def update_settings(self):
        compas_rhino.update_settings(self.settings)

    # ==========================================================================
    # form diagram
    # ==========================================================================

    def form_update_attributes(self):
        compas_rhino.update_settings(self.form.attributes)

    def form_from_mesh(self):
        guid = compas_rhino.select_mesh()
        if not guid:
            return
        self.form = FormDiagram.from_rhinomesh(guid)
        guids = compas_rhino.select_curves()
        if guids:
            keys = DiagramHelper.identify_vertices_on_curves(self.form, guids)
            self.form.set_vertices_attribute('is_anchor', True, keys)
            self.form.update_boundaries()
        self.form.draw(layer=self.settings['form.layer'])

    def form_to_mesh(self):
        raise NotImplementedError

    def form_from_json(self):
        path = compas_rhino.select_file(folder=HERE, filter='JSON files (*.json)|*.json||')
        if not path:
            return
        self.form = FormDiagram.from_json(path)
        self.form.draw(layer=self.settings['form.layer'])

    def form_to_json(self):
        folder = compas_rhino.select_folder(default=HERE)
        if not folder:
            return
        name = rs.GetString('Name of the formdiagram', 'formdiagram.json')
        if not name:
            return
        parts = name.split('.')
        if parts[-1] != 'json':
            parts.append('json')
            name = ".".join(parts)
        path = os.path.join(folder, name)
        if not path:
            return
        self.form.to_json(path)

    # def form_from_obj(self):
    #     path = compas_rhino.select_file(folder=HERE, filter='OBJ files (*.obj)|*.obj||')
    #     if not path:
    #         return
    #     self.form = FormDiagram.from_obj(path)
    #     self.form.draw(layer=self.settings['form.layer'])

    # def form_to_obj(self):
    #     raise NotImplementedError

    def form_update_vertex_attr(self):
        keys = DiagramHelper.select_vertices(self.form)
        if not keys:
            return
        if DiagramHelper.update_vertex_attributes(self.form, keys):
            self.form.draw(layer=self.settings['form.layer'])

    def form_update_edge_attr(self):
        keys = DiagramHelper.select_edges(self.form)
        if not keys:
            return
        if DiagramHelper.update_edge_attributes(self.form, keys):
            self.form.draw(layer=self.settings['form.layer'])

    def form_update_face_attr(self):
        keys = DiagramHelper.select_faces(self.form)
        if not keys:
            return
        if DiagramHelper.update_face_attributes(self.form, keys):
            self.form.draw(layer=self.settings['form.layer'])

    def form_smooth_area(self):
        fixed  = list(self.form.vertices_where({'is_anchor': True}))
        fixed += list(self.form.vertices_where({'is_fixed': True}))
        fixed += [key for fkey in self.form.faces_where({'is_loaded': False}) for key in self.form.face_vertices(fkey)]
        mesh_smooth_area(self.form, fixed=list(set(fixed)), kmax=50)
        self.form.draw(layer=self.settings['form.layer'])

    def form_select_vertices(self):
        raise NotImplementedError

    def form_select_edges(self):
        DiagramHelper.select_continuous_edges(self.form)

    # ==========================================================================
    # force diagram
    # ==========================================================================

    def force_update_attributes(self):
        compas_rhino.update_settings(self.force.attributes)

    def force_from_form(self):
        self.force = ForceDiagram.from_formdiagram(self.form)
        self.force.draw(layer=self.settings['force.layer'])

    def force_update_vertex_attr(self):
        keys = DiagramHelper.select_vertices(self.force)
        if not keys:
            return
        if DiagramHelper.update_vertex_attributes(self.force, keys):
            self.force.draw(layer=self.settings['force.layer'])

    def force_update_edge_attr(self):
        keys = DiagramHelper.select_edges(self.force)
        if not keys:
            return
        if DiagramHelper.update_edge_attributes(self.force, keys):
            self.force.draw(layer=self.settings['force.layer'])

    def force_move(self):
        if DiagramHelper.move(self.force):
            self.force.draw(layer=self.settings['force.layer'])

    # ==========================================================================
    # equilibrium
    # ==========================================================================

    def update_horizontal(self):
        horizontal(self.form, self.force, alpha=self.settings['horizontal.alpha'], kmax=self.settings['horizontal.kmax'])
        self.form.draw(layer=self.settings['form.layer'])
        self.force.draw(layer=self.settings['force.layer'])

    def update_vertical(self):
        vertical(self.form, self.settings['vertical.zmax'])
        self.form.draw(layer=self.settings['form.layer'])
        self.force.draw(layer=self.settings['force.layer'])

    # ==========================================================================
    # visualisation
    # ==========================================================================

    def show_forces(self):
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_forces()
        artist.draw_forces()
        artist.redraw()

    def hide_forces(self):
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_forces()
        artist.redraw()

    def show_reactions(self):
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_reactions()
        artist.draw_reactions()
        artist.redraw()

    def hide_reactions(self):
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_reactions()
        artist.redraw()

    def show_angles(self):
        angles = self.form.get_edges_attribute('a')
        amin = min(angles)
        amax = max(angles)
        adif = amax - amin
        text = {}
        color = {}
        for u, v, attr in self.form.edges_where({'is_edge': True}, True):
            a = attr['a']
            if a > 5:
                text[u, v] = "{:.1f}".format(a)
                color[u, v] = i_to_green((a - amin) / adif)
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_edgelabels()
        artist.draw_edgelabels(text=text, color=color)
        artist.redraw()

    def hide_angles(self):
        artist = FormArtist(self.form, layer=self.settings['form.layer'])
        artist.clear_edgelabels()
        artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
