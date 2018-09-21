from __future__ import print_function

import compas
import compas_rhino
import compas_tna

from compas.utilities import i_to_green

from compas_tna.diagrams import FormDiagram
from compas_tna.diagrams import ForceDiagram

from compas_tna.rhino import FormArtist
from compas_tna.rhino import DiagramHelper

from compas_tna.equilibrium import horizontal_nodal_rhino as horizontal
from compas_tna.equilibrium import vertical_from_zmax_rhino as vertical


# create diagrams from serialised files


# visualise the diagrams


# update the force bounds on the edges of the form diagram


# update the horizontal equilibrium


# compute the scale of the force diagram
# such that the highest vertex of the form diagram is at a prescribed value


# draw the result


# serialise the data

